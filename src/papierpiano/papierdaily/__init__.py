import os
import random
from datetime import datetime
from zoneinfo import ZoneInfo

import httpx
from escpos.printer import Network
from PIL import Image

PRINTER_HOST = os.environ["PRINTER_HOST"]
PRINTER_PORT = os.environ["PRINTER_PORT"]
API_KEY = os.environ["METEOBLUE_API_KEY"]

LAT = "43.6142"
LON = "1.42508"
ASL = "134"

GRAPHICS_PATH = "assets/monochrome_daily/"


def main():
    printer = Network(
        PRINTER_HOST,
        int(PRINTER_PORT),
        profile="TM-T20II",
    )

    response = httpx.get(
        f"https://my.meteoblue.com/packages/basic-day?apikey={API_KEY}&lat={LAT}&lon={LON}&asl={ASL}&windspeed=kmh&winddirection=2char"
    )
    response.raise_for_status()
    weather_data = response.json()

    # import json
    # weather_data = json.loads("""
    # {"metadata":{"modelrun_updatetime_utc":"2025-07-06 15:15","name":"","height":134,"timezone_abbrevation":"CEST","latitude":43.6142,"modelrun_utc":"2025-07-06 15:15","longitude":1.42508,"utc_timeoffset":2.0,"generation_time_ms":28.565048},"units":{"predictability":"percent","precipitation":"mm","windspeed":"ms-1","precipitation_probability":"percent","relativehumidity":"percent","time":"YYYY-MM-DD hh:mm","temperature":"C","pressure":"hPa","winddirection":"degree"},"data_day":{"time":["2025-07-06","2025-07-07","2025-07-08","2025-07-09","2025-07-10","2025-07-11","2025-07-12"],"temperature_instant":[24.5,20.01,17.83,17.9,20.2,22.28,24.71],"precipitation":[0.33,0.2,0.0,0.0,0.0,0.1,8.67],"predictability":[69,66,80,81,73,55,35],"temperature_max":[24.17,21.83,24.31,27.68,31.17,33.83,32.52],"sealevelpressure_mean":[1016,1015,1018,1018,1016,1011,1009],"windspeed_mean":[4.75,6.16,4.55,2.46,2.34,3.28,3.87],"precipitation_hours":[3.0,1.0,0.0,0.0,0.0,1.0,17.0],"sealevelpressure_min":[1014,1014,1017,1017,1013,1008,1007],"pictocode":[16,16,2,1,1,8,8],"snowfraction":[0.0,0.0,0.0,0.0,0.0,0.0,0.0],"humiditygreater90_hours":[0.0,0.13,0.17,0.0,0.0,0.0,0.0],"convective_precipitation":[0.0,0.0,0.0,0.0,0.0,0.1,8.67],"relativehumidity_max":[68,91,85,76,68,71,77],"temperature_min":[20.01,17.83,15.82,14.48,15.18,16.67,19.47],"winddirection":["SE",270,315,0,0,90,135],"felttemperature_max":[22.7,19.07,21.57,25.92,30.0,33.02,33.39],"relativehumidity_min":[33,61,37,27,21,23,42],"felttemperature_mean":[19.27,17.34,17.56,19.96,22.22,24.64,26.13],"windspeed_min":[3.71,3.99,2.13,1.29,1.78,2.5,2.74],"felttemperature_min":[17.32,15.3,13.75,13.5,13.67,15.33,19.24],"precipitation_probability":[19,33,0,0,0,25,40],"uvindex":[6,6,7,8,9,8,8],"rainspot":["1112222111111111111111111111111111111111111111111","1111910191991919100009919000909099090900000090000","0000000000000000000000000000000000000000000000099","0000000000000000000000000000000000000000000000000","0000000000000000000000000000000000000000000000000","0000000900000099999009999909000000000000000000000","2223333233333322333333333333333333333333332222233"],"temperature_mean":[22.28,19.83,19.97,21.46,23.76,26.12,26.19],"sealevelpressure_max":[1017,1017,1020,1020,1018,1014,1010],"relativehumidity_mean":[48,75,60,48,41,43,58],"predictability_class":[4.0,4.0,5.0,5.0,4.0,3.0,2.0],"windspeed_max":[5.8,8.33,5.34,3.52,3.05,4.1,4.6]}}
    # """)

    PICTO_CODES = {
        "01": "Ciel dégagé, sans nuages",
        "02": "Ciel dégagé avec quelques nuages",
        "03": "Partiellement nuageux",
        "04": "Couvert",
        "05": "Brouillard",
        "06": "Couvert avec pluie",
        "07": "Variable avec averses",
        "08": "Averses, orages probables",
        "09": "Couvert avec neige",
        "10": "Variable avec averses de neige",
        "11": "Nuageux avec un mélange de neige et pluie",
        "12": "Couvert avec pluie occasionnelle",
        "13": "Couvert avec neige occasionnelle",
        "14": "Nuageux avec pluie",
        "15": "Nuageux avec neige",
        "16": "Nuageux avec pluie occasionnelle",
        "17": "Nuageux avec neige occasionnelle",
    }

    WIND_DIRECTION = {
        "N": "N",
        "NE": "NE",
        "E": "E",
        "SE": "SE",
        "S": "S",
        "SW": "SO",
        "W": "O",
        "NW": "NO",
    }

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

    picto_id = str(weather_data["data_day"]["pictocode"][0]).zfill(2)
    picto = PICTO_CODES[picto_id]

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
        f"{weather_data['data_day']['temperature_min'][0]:.1f}°C min — {weather_data['data_day']['temperature_max'][0]:.1f}°C max",
    )
    printer.ln()

    print_left_and_right(
        "Précipitations:",
        f"{weather_data['data_day']['precipitation'][0]:.0f} mm — {weather_data['data_day']['precipitation_probability'][0]}% prob",
    )
    printer.ln()

    print_left_and_right(
        "Vent:",
        f"{WIND_DIRECTION[weather_data['data_day']['winddirection'][0]]} — {weather_data['data_day']['windspeed_mean'][0]:.0f} km/h moy — {weather_data['data_day']['windspeed_max'][0]:.0f} km/h max",
    )
    printer.ln()

    printer.ln()
    printer.ln()

    tasks = []
    # Arroser calathea tous les 2 jours
    if now.toordinal() % 2 == 0:
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

    citations = [
        "La vie est trop courte pour boire du mauvais vin.",
        "Un ami, c'est quelqu'un qui vous connaît bien et qui vous aime quand même.",
        "Il vaut mieux être seul que mal accompagné.",
        "L'argent ne fait pas le bonheur, mais il y contribue.",
        "Qui ne risque rien n'a rien.",
        "Mieux vaut tard que jamais.",
        "C'est en forgeant qu'on devient forgeron.",
        "Les chiens aboient, la caravane passe.",
        "Petit à petit, l'oiseau fait son nid.",
        "Rome ne s'est pas faite en un jour.",
        "Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce qu'en avant, ils tombent dans le bateau !",
        "Que dit un escargot quand il croise une limace ? Regardez, un nudiste !",
        "Comment appelle-t-on un chat tombé dans un pot de peinture ? Un chat-mallow !",
        "Qu'est-ce qui est jaune et qui attend ? Jonathan !",
        "Que dit un café qui arrive en retard au bureau ? Désolé, j'étais en grain de dormir !",
        "L'échec est le fondement de la réussite.",
        "Qui veut voyager loin ménage sa monture.",
        "Il n'y a que les montagnes qui ne se rencontrent jamais.",
        "Chassez le naturel, il revient au galop.",
        "L'habit ne fait pas le moine.",
        "Tout vient à point à qui sait attendre.",
        "Il faut battre le fer pendant qu'il est chaud.",
        "Les grands esprits se rencontrent.",
        "Qui se ressemble s'assemble.",
        "Le temps, c'est de l'argent.",
        "Que dit un cannibale qui n'a plus faim ? J'ai croké !",
        "Comment dit-on 'se brosser les dents' en chinois ? Chu-ki-ta !",
        "Qu'est-ce qui est transparent et qui court dans la forêt ? Un cerf-volant !",
        "Pourquoi les poissons n'aiment pas jouer au tennis ? Parce qu'ils ont peur du filet !",
        "Que dit un cheveu sur un crâne chauve ? On est seul au monde !",
        "La beauté est dans l'œil de celui qui regarde.",
        "Il vaut mieux prévenir que guérir.",
        "Qui sème le vent récolte la tempête.",
        "Les paroles s'envolent, les écrits restent.",
        "Aide-toi et le ciel t'aidera.",
        "Nécessité fait loi.",
        "Qui trop embrasse mal étreint.",
        "L'union fait la force.",
        "Pierre qui roule n'amasse pas mousse.",
        "Rira bien qui rira le dernier.",
        "Que dit un vampire qui a mal aux dents ? J'ai une carie qui me pique !",
        "Comment appelle-t-on un boomerang qui ne revient pas ? Un bâton !",
        "Qu'est-ce qui est blanc et qui vole ? Une mouette !",
        "Pourquoi les parachutistes sont-ils toujours bronzés ? Parce qu'ils tombent du ciel !",
        "Que dit un crocodile qui surveille la pharmacie ? J'ai l'œil du tigre !",
        "Impossible n'est pas français.",
        "Qui vivra verra.",
        "Loin des yeux, loin du cœur.",
        "Après la pluie, le beau temps.",
        "Tel père, tel fils.",
        "Chat échaudé craint l'eau froide.",
        "Qui ne dit mot consent.",
        "Les goûts et les couleurs ne se discutent pas.",
        "Mieux vaut un tiens que deux tu l'auras.",
        "La nuit porte conseil.",
        "Que dit un escargot qui descend la montagne ? Je bave ma pente !",
        "Comment appelle-t-on un chat qui a bu du citron ? Un chat-grin !",
        "Qu'est-ce qui est rouge et qui danse ? Une tomate qui a le rythme !",
        "Pourquoi les abeilles ont-elles les cheveux collants ? Parce qu'elles ont des miel-lèches !",
        "Que dit un facteur qui n'arrive pas à ouvrir la porte ? J'ai perdu mes clés !",
        "Il faut réfléchir avant d'agir.",
        "Qui dort dîne.",
        "Faute de grives, on mange des merles.",
        "Il n'y a pas de fumée sans feu.",
        "Charité bien ordonnée commence par soi-même.",
        "On ne fait pas d'omelette sans casser des œufs.",
        "Qui cherche trouve.",
        "Les murs ont des oreilles.",
        "Ventre affamé n'a point d'oreilles.",
        "Il n'est pire eau que l'eau qui dort.",
        "Que dit un crocodile qui vend des aspirateurs ? Je suis un rep-tile !",
        "Comment appelle-t-on un pingouin qui mange épicé ? Un pingouin qui a la banquise !",
        "Qu'est-ce qui est vert et qui pousse sous l'eau ? Un chou marin !",
        "Pourquoi les chats préfèrent-ils les souris au fromage ? Parce que c'est plus amusant !",
        "Que dit un pneu fatigué ? Je suis crevé !",
        "Qui ne tente rien n'a rien.",
        "Les actes valent mieux que les paroles.",
        "Il vaut mieux se taire et passer pour un idiot.",
        "Qui court deux lièvres n'en prend aucun.",
        "Bien mal acquis ne profite jamais.",
        "Une hirondelle ne fait pas le printemps.",
        "Qui aime bien châtie bien.",
        "La patience est mère de toutes les vertus.",
        "Bon sang ne peut mentir.",
        "Chacun voit midi à sa porte.",
        "Que dit un canard qui va à la pharmacie ? J'ai besoin de pommade pour mes coins !",
        "Comment appelle-t-on un poisson qui ne partage pas ? Un poisson-sole !",
        "Qu'est-ce qui est violet et qui attend le bus ? Un prunier !",
        "Pourquoi les poules ne portent-elles pas de culotte ? Parce que le coq a des plumes !",
        "Que dit un ordinateur qui a froid ? J'ai un virus !",
        "La vérité sort de la bouche des enfants.",
        "Qui se couche avec les chiens se lève avec des puces.",
        "Il y a un temps pour tout.",
        "Nul n'est prophète en son pays.",
        "Plus on est de fous, plus on rit.",
        "Qui va à la chasse perd sa place.",
        "L'avenir appartient à ceux qui se lèvent tôt.",
        "Comparaison n'est pas raison.",
        "Qui paie ses dettes s'enrichit.",
        "Les cordonniers sont les plus mal chaussés.",
        "Que dit un arbre qui a soif ? J'ai les racines sèches !",
        "Comment appelle-t-on un homme qui a perdu son chien ? Un homme désespéré !",
        "Qu'est-ce qui monte et qui descend mais ne bouge pas ? Un escalier !",
        "Pourquoi les elephants ne peuvent-ils pas faire du vélo ? Parce qu'ils n'ont pas de pouce !",
        "Que dit un escargot sportif ? J'ai le rythme dans la peau !",
        "Qui ne risque rien n'a rien.",
        "Les apparences sont trompeuses.",
        "Il faut tourner sa langue sept fois avant de parler.",
    ]

    printer.set_with_default(bold=True, underline=True)
    printer.textln("Phrase du jour")
    printer.set_with_default(align="center", font="b")
    printer.ln()
    printer.textln(random.choice(citations))
    printer.ln()
    printer.ln()

    expressions_bonne_journee = [
        "Bonne journée !",
        "Passez une excellente journée !",
        "Je vous souhaite une merveilleuse journée !",
        "Profitez bien de votre journée !",
        "Que votre journée soit belle !",
        "Excellente journée à vous !",
        "Bonne continuation !",
        "Passez une journée formidable !",
        "Que cette journée vous soit favorable !",
        "Je vous souhaite une journée radieuse !",
        "Bonne journée et à bientôt !",
        "Profitez pleinement de cette journée !",
        "Que votre journée soit remplie de joie !",
        "Passez une journée magnifique !",
        "Je vous souhaite une journée ensoleillée !",
        "Bonne journée à vous !",
        "Que cette journée vous apporte bonheur !",
        "Passez une journée délicieuse !",
        "Je vous souhaite une journée parfaite !",
        "Bonne journée et prenez soin de vous !",
        "Que votre journée soit douce !",
        "Passez une journée extraordinaire !",
        "Je vous souhaite une journée pleine de surprises !",
        "Bonne journée et à plus tard !",
        "Que cette journée vous sourie !",
        "Passez une journée inoubliable !",
        "Je vous souhaite une journée productive !",
        "Bonne journée et bon courage !",
        "Que votre journée soit lumineuse !",
        "Passez une journée fantastique !",
    ]

    printer.set_with_default(align="center")
    printer.textln(random.choice(expressions_bonne_journee))
    printer.cut()


if __name__ == "__main__":
    main()
