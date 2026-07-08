import os
import textwrap
from datetime import datetime
from zoneinfo import ZoneInfo

import httpx
from escpos.printer import Network
from PIL import Image, ImageDraw, ImageFont

PRINTER_HOST = os.environ["PRINTER_HOST"]
PRINTER_PORT = os.environ["PRINTER_PORT"]

LAT = "43.6142"
LON = "1.42508"
ELEVATION = "134"

GRAPHICS_PATH = "assets/monochrome_daily/"

# Largeur d'impression en pixels (48 colonnes en police A sur la TM-T20II).
PRINT_WIDTH = 576

# Titres suivis en bourse : (ticker Yahoo Finance, libellé affiché)
STOCKS = [
    ("AIR.PA", "Airbus"),
    ("CW8.PA", "CW8 (MSCI World)"),
]

# Police de la section bourse (rendue en image) : (fichier, instance variable).
# L'instance ne s'applique qu'aux polices variables ; None sinon.
BOURSE_FONT_DATA = ("assets/JetBrainsMono.ttf", "Regular")
BOURSE_FONT_LABEL = ("assets/JetBrainsMono.ttf", "Medium")


def fetch_stock(symbol):
    """Récupère l'historique quotidien (clôtures) d'un titre via Yahoo Finance."""
    response = httpx.get(
        f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
        params={"range": "1mo", "interval": "1d"},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=15,
    )
    response.raise_for_status()
    result = response.json()["chart"]["result"][0]
    closes = [c for c in result["indicators"]["quote"][0]["close"] if c is not None]
    currency = result["meta"].get("currency", "")
    return closes, currency


def fetch_history_events(month, day):
    """Événements historiques marquants du jour via l'API Wikipédia FR."""
    response = httpx.get(
        f"https://fr.wikipedia.org/api/rest_v1/feed/onthisday/selected/{month:02d}/{day:02d}",
        headers={"User-Agent": "papierpiano/1.0 (impression quotidienne perso)"},
        timeout=15,
        follow_redirects=True,
    )
    response.raise_for_status()
    events = response.json().get("selected", [])
    return [
        (event["year"], event["text"])
        for event in events
        if event.get("year") and event.get("text")
    ]


def collect_stocks():
    """Récupère les données de tous les titres suivis, en ignorant les échecs."""
    stocks = []
    for symbol, label in STOCKS:
        try:
            closes, currency = fetch_stock(symbol)
        except Exception:
            continue
        if len(closes) >= 2:
            stocks.append((label, closes, currency))
    return stocks


def fmt_fr(value):
    """Formate un nombre à la française : espace pour les milliers, virgule décimale."""
    return f"{value:,.2f}".replace(",", " ").replace(".", ",")


def load_font(spec, size):
    """Charge une police depuis (fichier, instance variable ou None)."""
    path, variation = spec
    font = ImageFont.truetype(path, size)
    if variation:
        try:
            font.set_variation_by_name(variation)
        except Exception:
            pass
    return font


def _graph_points(values, box, pad=6):
    """Coordonnées de la courbe à l'intérieur d'une boîte (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    low, high = min(values), max(values)
    span = (high - low) or 1
    count = len(values)
    return [
        (
            x0 + pad + (x1 - x0 - 2 * pad) * (i / (count - 1) if count > 1 else 0),
            y1 - pad - (y1 - y0 - 2 * pad) * ((value - low) / span),
        )
        for i, value in enumerate(values)
    ]


def draw_graph(draw, values, box):
    """Dessine le mini-graphe des clôtures : aire en dégradé + courbe + point final.

    L'aplat gris est tramé en points par l'imprimante lors de la conversion N&B,
    ce qui donne une zone claire sous la courbe.
    """
    _, _, _, y1 = box
    points = _graph_points(values, box)
    base = y1 - 2
    for (xa, ya), (xb, yb) in zip(points, points[1:]):
        draw.polygon([(xa, ya), (xb, yb), (xb, base), (xa, base)], fill=225)
    draw.line([(box[0], base), (box[2], base)], fill=140, width=1)
    draw.line(points, fill=0, width=3, joint="curve")
    lx, ly = points[-1]
    draw.ellipse([lx - 3, ly - 3, lx + 3, ly + 3], fill=0)


def render_bourse(
    stocks,
    data_spec=BOURSE_FONT_DATA,
    label_spec=BOURSE_FONT_LABEL,
    block_height=76,
):
    """Compose tout le contenu de la section bourse en une seule image.

    L'ESC/POS ne peut pas mêler texte et image sur une même ligne : on rend donc
    le libellé, le cours, la variation et le graphe ensemble, ce qui permet
    d'aligner la courbe à droite du cours.
    """
    label_font = load_font(label_spec, 26)
    data_font = load_font(data_spec, 22)

    image = Image.new("L", (PRINT_WIDTH, block_height * len(stocks)), 255)
    draw = ImageDraw.Draw(image)

    graph_left = PRINT_WIDTH - 160  # de l'air entre le texte et le graphe

    for index, (label, closes, currency) in enumerate(stocks):
        top = index * block_height + 6
        last, previous = closes[-1], closes[-2]
        change = last - previous
        change_pct = (change / previous * 100) if previous else 0
        up = change >= 0
        sign = "+" if up else "-"
        pct_str = f"{abs(change_pct):.1f}".replace(".", ",")

        draw.text((8, top), label, font=label_font, fill=0)

        data_y = top + 32
        prefix = f"{fmt_fr(last)} {currency}   "
        draw.text((8, data_y), prefix, font=data_font, fill=0)

        # Triangle de tendance dessiné en vectoriel (absent des polices).
        arrow_x = 8 + draw.textlength(prefix, font=data_font)
        arrow_y, arrow_size = data_y + 5, 12
        if up:
            triangle = [
                (arrow_x, arrow_y + arrow_size),
                (arrow_x + arrow_size, arrow_y + arrow_size),
                (arrow_x + arrow_size / 2, arrow_y),
            ]
        else:
            triangle = [
                (arrow_x, arrow_y),
                (arrow_x + arrow_size, arrow_y),
                (arrow_x + arrow_size / 2, arrow_y + arrow_size),
            ]
        draw.polygon(triangle, fill=0)

        variation = f"{sign}{pct_str}% ({sign}{fmt_fr(abs(change))})"
        draw.text((arrow_x + arrow_size + 6, data_y), variation, font=data_font, fill=0)

        box = (graph_left, top + 4, PRINT_WIDTH - 10, top + block_height - 12)
        draw_graph(draw, closes[-7:], box)

    return image


def main():
    printer = Network(
        PRINTER_HOST,
        int(PRINTER_PORT),
        profile="TM-T20II",
    )

    response = httpx.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": LAT,
            "longitude": LON,
            "elevation": ELEVATION,
            "daily": ",".join(
                [
                    "weather_code",
                    "temperature_2m_min",
                    "temperature_2m_max",
                    "precipitation_sum",
                    "precipitation_probability_max",
                    "wind_direction_10m_dominant",
                    "wind_speed_10m_max",
                    "wind_gusts_10m_max",
                ]
            ),
            "wind_speed_unit": "kmh",
            "timezone": "Europe/Paris",
            "forecast_days": 1,
        },
    )
    response.raise_for_status()
    weather_data = response.json()
    daily = weather_data["daily"]

    # Open-Meteo returns WMO weather codes (0-99). Each code has its own French
    # description, plus the meteoblue pictocode whose icon asset we reuse (several
    # WMO codes can share one picto while keeping distinct descriptions).
    WMO_CODES = {
        0: ("01", "Ciel dégagé"),
        1: ("02", "Principalement dégagé"),
        2: ("03", "Partiellement nuageux"),
        3: ("04", "Couvert"),
        45: ("05", "Brouillard"),
        48: ("05", "Brouillard givrant"),
        51: ("16", "Bruine légère"),
        53: ("16", "Bruine modérée"),
        55: ("14", "Bruine dense"),
        56: ("11", "Bruine verglaçante légère"),
        57: ("11", "Bruine verglaçante dense"),
        61: ("14", "Pluie faible"),
        63: ("06", "Pluie modérée"),
        65: ("06", "Pluie forte"),
        66: ("11", "Pluie verglaçante faible"),
        67: ("11", "Pluie verglaçante forte"),
        71: ("17", "Neige faible"),
        73: ("15", "Neige modérée"),
        75: ("09", "Neige forte"),
        77: ("15", "Grains de neige"),
        80: ("07", "Averses de pluie faibles"),
        81: ("07", "Averses de pluie modérées"),
        82: ("08", "Averses de pluie violentes"),
        85: ("10", "Averses de neige faibles"),
        86: ("10", "Averses de neige fortes"),
        95: ("08", "Orage"),
        96: ("08", "Orage avec grêle légère"),
        99: ("08", "Orage avec grêle forte"),
    }

    def wind_direction_fr(degrees):
        """Convert a wind direction in degrees to a French cardinal point."""
        points = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]
        return points[round(degrees / 45) % 8]

    now = datetime.now(tz=ZoneInfo("Europe/Paris"))
    weekday = now.weekday()
    weekday_str = {
        "0": "Lundi",
        "1": "Mardi",
        "2": "Mercredi",
        "3": "Jeudi",
        "4": "Vendredi",
        "5": "Samedi",
        "6": "Dimanche",
    }[str(weekday)]

    month = now.month
    month_str = {
        "1": "Janvier",
        "2": "Février",
        "3": "Mars",
        "4": "Avril",
        "5": "Mai",
        "6": "Juin",
        "7": "Juillet",
        "8": "Août",
        "9": "Septembre",
        "10": "Octobre",
        "11": "Novembre",
        "12": "Décembre",
    }[str(month)]

    printer.set_with_default(
        bold=True, align="center", double_height=True, double_width=True
    )
    printer.textln("Bonjour")
    printer.set_with_default(align="center", bold=True, double_width=True)
    printer.ln()
    printer.textln(f"{weekday_str} {now.day} {month_str}")
    printer.ln()
    printer.ln()

    birthdays = {
        "01-03": ["Rayan Djebli"],
        "01-04": ["Corentin"],
        "01-05": ["Brigitte"],
        "01-08": ["Seb Menez"],
        "01-26": ["Adèle Chou"],
        "01-31": ["Julian"],
        "02-10": ["Anne-Marie"],
        "02-14": ["Lucie Cabiran"],
        "02-21": ["Thomas"],
        "02-23": ["Talia"],
        "03-11": ["Loïc"],
        "03-24": ["Ludo Deuillhé", "Orianna"],
        "04-11": ["Ben Minard", "Charlotte Martel", "Nathalie Lévesque"],
        "04-13": ["Amaury Perreon"],
        "04-23": ["Thomas Bezy"],
        "04-27": ["Hicham Hilali"],
        "05-09": ["Zozo Molion", "Fadoua"],
        "05-20": ["Manon"],
        "05-25": ["Maëlys"],
        "06-01": ["Élodie"],
        "06-06": ["Aloïs"],
        "07-06": ["Alain Vergez"],
        "07-21": ["Benjamin Besnier"],
        "07-23": ["Juliette"],
        "07-24": ["Thomas Guillon"],
        "07-30": ["Antonin"],
        "08-01": ["Nico Sousa", "Dorian Bihel"],
        "08-03": ["Adèle"],
        "08-14": ["Marjo La Boulette"],
        "08-22": ["Pierrick Payet"],
        "08-30": ["Daphné"],
        "08-31": ["Antoine Aniort"],
        "09-15": ["Ferry Wehman"],
        "10-10": ["Agathe"],
        "10-13": ["Arthur Bussi"],
        "10-19": ["Lucie Lévesque"],
        "10-26": ["Paf"],
        "11-03": ["Camille Lévesque"],
        "11-04": ["Daniel Lévesque"],
        "11-06": ["Lucas Blondel"],
        "11-10": ["Mila"],
        "11-13": ["Pauline Garcia"],
        "11-16": ["Simon Bertolin"],
        "11-17": ["Romane"],
        "12-03": ["Mélanie"],
        "12-04": ["Calie"],
        "12-12": ["Lénaïc"],
        "12-15": ["Lucas"],
        "12-17": ["William"],
    }

    birthday = birthdays.get(f"{now.month:02d}-{now.day:02d}", [])
    if birthday:
        printer.set_with_default(bold=True, underline=True)
        printer.textln("Anniversaires du jour")
        printer.ln()
        printer.set_with_default()

        for name in birthday:
            printer.textln(" " * 4 + "» " + name)

        printer.ln()
        printer.ln()

    printer.set_with_default(bold=True, underline=True)
    printer.textln("Prévisions météo")

    picto_id, picto = WMO_CODES.get(daily["weather_code"][0], ("03", "Partiellement nuageux"))

    image = Image.open(os.path.join(GRAPHICS_PATH, f"{picto_id}_iday_monochrome.png"))
    image.thumbnail((100, image.height), Image.Resampling.LANCZOS)

    printer.image(image, impl="graphics", center=True)
    printer.set_with_default(align="center", bold=True)
    printer.textln(picto)
    printer.ln()

    def print_left_and_right(text_left, text_right):
        """Prints text on the left and right side of the line."""
        printer.text(text_left)
        printer.text(" " * (48 - len(text_left) - len(text_right)))
        printer.text(text_right)

    printer.set_with_default()
    print_left_and_right(
        "Température:",
        f"{daily['temperature_2m_min'][0]:.1f}°C min — {daily['temperature_2m_max'][0]:.1f}°C max",
    )
    printer.ln()

    print_left_and_right(
        "Précipitations:",
        f"{daily['precipitation_sum'][0]:.0f} mm — {daily['precipitation_probability_max'][0]}% prob",
    )
    printer.ln()

    print_left_and_right(
        "Vent:",
        f"{wind_direction_fr(daily['wind_direction_10m_dominant'][0])} — {daily['wind_speed_10m_max'][0]:.0f} km/h max — {daily['wind_gusts_10m_max'][0]:.0f} km/h rafales",
    )
    printer.ln()

    printer.ln()
    printer.ln()

    stocks_data = collect_stocks()
    if stocks_data:
        printer.set_with_default(bold=True, underline=True)
        printer.textln("Bourse")
        printer.ln()
        printer.image(render_bourse(stocks_data), impl="graphics", center=True)
        printer.ln()
        printer.ln()

    tasks = []
    # Arroser calathea tous les 3 jours
    if now.toordinal() % 3 == 0:
        tasks.append("Arroser calathea")
    # Changer les draps tous les 2 samedis
    if now.weekday() == 5 and ((now.isocalendar().week % 2) == 0):
        tasks.append("Changer les draps")

    if tasks:
        printer.set_with_default(bold=True, underline=True)
        printer.textln("Tâches du jour")
        printer.ln()
        printer.set_with_default()

        for task in tasks:
            printer.textln(" " * 4 + "» " + task)

        printer.ln()
        printer.ln()

    def print_wrapped(text, initial_indent="", subsequent_indent=""):
        """Imprime un texte habillé sur 48 colonnes, sans couper les mots."""
        for line in textwrap.wrap(
            text,
            width=48,
            initial_indent=initial_indent,
            subsequent_indent=subsequent_indent,
            break_long_words=False,
            break_on_hyphens=False,
        ):
            printer.textln(line)

    try:
        history = fetch_history_events(now.month, now.day)
    except Exception:
        history = []

    if history:
        day_str = "1er" if now.day == 1 else str(now.day)
        printer.set_with_default(bold=True, underline=True)
        printer.textln(f"Ça s'est passé un {day_str} {month_str.lower()}")
        printer.ln()
        printer.set_with_default()

        for year, text in history[:2]:
            print_wrapped(
                f"{year} — {text}",
                initial_indent=" " * 4 + "» ",
                subsequent_indent=" " * 6,
            )
            printer.ln()

    printer.cut()


if __name__ == "__main__":
    main()
