import os
import random
import textwrap
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

    print_left_and_right(
        "Humidité:",
        f"{int(weather_data['data_day']['relativehumidity_min'][0])}% min — {int(weather_data['data_day']['relativehumidity_mean'][0])}% moy — {int(weather_data['data_day']['relativehumidity_max'][0])}% max",
    )
    printer.ln()

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

    citations = [
        "La vie, c'est comme une bicyclette, il faut avancer pour ne pas perdre l'équilibre.",
        "L'expérience, c'est le nom que chacun donne à ses erreurs.",
        "Je ne suis pas paresseux, je suis en mode économie d'énergie.",
        "La vie est courte. Souriez tant que vous avez encore des dents.",
        "Si la vie te donne des citrons, fais-en une margarita.",
        "Les hommes sont comme le café : les meilleurs sont riches, chauds et peuvent te tenir éveillée toute la nuit.",
        "Le travail d'équipe est essentiel. Cela permet de rejeter la faute sur quelqu'un d'autre.",
        "Rien ne sert de courir, il faut partir à point… surtout quand on n'a pas envie d'y aller.",
        "Le bonheur, c'est de continuer à désirer ce qu'on possède déjà.",
        "La vie est une maladie mortelle sexuellement transmissible.",
        "Deux choses sont infinies : l'univers et la bêtise humaine. Mais pour l'univers, je n'en suis pas sûr.",
        "Il vaut mieux se taire et passer pour un imbécile que parler et ne laisser aucun doute à ce sujet.",
        "La différence entre le génie et la stupidité, c'est que le génie a ses limites.",
        "La moitié du monde ne sait pas comment vit l'autre moitié… mais elle a son opinion dessus.",
        "Les cons, ça ose tout. C'est même à ça qu'on les reconnaît.",
        "L'amour rend aveugle, mais le mariage rend la vue.",
        "Le mariage, c'est la volonté à deux de créer quelque chose qu'un seul des deux regrettera.",
        "Les hommes mentent moins que les femmes… sauf quand ils parlent.",
        "L'amour, c'est comme les cartes : si tu n'as pas de partenaire, il te faut une bonne main.",
        "L'amour, c'est beaucoup de choses… surtout du malentendu.",
        "J'adore les deadlines. J'aime le bruit qu'elles font en s'envolant.",
        "Le travail est l'opium du peuple, et je ne veux pas mourir drogué.",
        "Travailler dur n'a jamais tué personne, mais pourquoi prendre le risque ?",
        "Un patron, c'est quelqu'un qui arrive à l'heure dans ta vie quand tu pars en retard.",
        "Le travail d'équipe, c'est la possibilité de faire porter le chapeau à quelqu'un d'autre.",
        "Je ne bois jamais à outrance, je ne sais même pas où c'est.",
        "Un verre à moitié vide, c'est aussi un verre à moitié plein, mais pas assez plein.",
        "L'alcool ne résout pas les problèmes, mais l'eau non plus.",
        "Le chocolat ne pose pas de questions stupides, le chocolat comprend.",
        "Les régimes, c'est comme les promesses électorales : ça ne tient jamais.",
        "On ne vieillit pas, on devient juste plus classique.",
        "L'âge, c'est quand les bougies coûtent plus cher que le gâteau.",
        "Vieillir, c'est embêtant, mais c'est encore le seul moyen connu de vivre longtemps.",
        "Je n'ai pas 50 ans, j'ai 20 ans avec 30 ans d'expérience.",
        "L'enfance, c'est quand on ne demande pas l'heure du coucher.",
        "Mon téléphone est plus intelligent que moi, mais il n'a toujours pas trouvé de travail.",
        "Internet : le seul endroit où on peut avoir 5 000 amis et manger seul.",
        "Le Wi-Fi, c'est comme l'amour : on ne le voit pas, mais on sait quand il n'y en a plus.",
        "Avant, on lisait dans les étoiles. Maintenant, on lit les notifications.",
        "L'orthographe, c'est l'art de bien embêter les générations futures.",
        "Pourquoi faire aujourd'hui ce qu'on peut remettre à demain ?",
        "Le matin, j'ai l'impression que mon lit et moi, on vit une histoire d'amour.",
        "Je ne suis pas en retard, j'ai juste une gestion du temps très artistique.",
        "Dormir, c'est donner du temps au temps.",
        "Le sport, c'est la santé. Mais à quoi sert la santé sans farniente ?",
        "Il faut apprendre à rester debout, même assis sur une chaise.",
        "Le ridicule ne tue pas, mais il fatigue.",
        "Mieux vaut être de mauvaise humeur que de mauvaise foi.",
        "Si tu veux que la vie te sourie, commence par lui montrer tes dents.",
        "On ne peut pas plaire à tout le monde. Déjà, je ne me plais pas à moi-même tous les jours.",
        "Certains poursuivent leurs rêves. Moi, je les laisse venir à moi pendant la sieste.",
        "J'ai décidé d'être heureux, parce que c'est bon pour la santé mentale des autres.",
        "Le lundi est une invention du diable pour tester notre patience.",
        "Je ne procrastine pas, je fais une incubation stratégique d'idées.",
        "Je ne suis pas désordonné, je suis juste créativement organisé.",
        "Les statistiques prouvent que 100% des gens qui dorment ne meurent pas pendant qu'ils dorment.",
        "Je ne suis pas têtu, j'ai simplement toujours raison.",
        "Les gens qui se lèvent tôt ne comprennent pas que dormir est aussi une passion.",
        "L'ascenseur social est en panne, prenez l'escalier avec le sourire.",
        "Je ne vieillis pas, je me bonifie comme un bon fromage : plus fort chaque jour.",
        "J'ai arrêté de faire du sport quand j'ai réalisé que j'étais plus efficace en commentant les matchs.",
        "Si le rire est le meilleur remède, pourquoi les médecins ne prescrivent-ils pas de blagues ?",
        "L'herbe est toujours plus verte ailleurs, surtout quand on ne tond jamais la sienne.",
        "Je suis au régime. J'ai remplacé le sucre par la tristesse.",
        "Le monde appartient à ceux qui se lèvent tôt, mais il tourne grâce à ceux qui veillent tard.",
        "Je ne suis pas superstitieux, mais je ne marche pas sur les Lego.",
        "La motivation, c'est quand tu as envie de faire quelque chose que tu n'as pas envie de faire.",
        "Le silence est d'or… sauf quand tu as oublié où tu as mis ton téléphone en mode silencieux.",
        "Je me parle à moi-même parce que j'aime discuter avec des gens intelligents.",
        "Ne jamais remettre à demain ce qu'on peut déléguer aujourd'hui.",
        "Les erreurs sont humaines, mais certaines sont des œuvres d'art.",
        "Je voulais changer le monde, mais j'ai perdu la télécommande.",
        "Le café ne résout pas les problèmes, mais il rend les gens plus supportables.",
        "L'argent ne fait pas le bonheur, mais il rend les larmes plus confortables.",
        "Un jour sans rire est un jour perdu. Deux jours sans café, c'est une catastrophe nationale.",
        "Je ne dors pas mal, je fais des répétitions pour ma carrière de fantôme.",
        "Ma conscience et moi, on n'est plus en bons termes depuis que j'ai découvert les siestes.",
        "La maturité, c'est quand tu ris toujours, mais plus discrètement.",
        "Les pannes de réveil sont les excuses les plus sincères du monde.",
        "Je suis multitâche : je peux écouter, ignorer et oublier en même temps.",
        "Les rêves ne se réalisent pas tout seuls, sauf les cauchemars.",
        "Mon corps est un temple… abandonné depuis des années.",
        "Je n'ai pas d'ennemis, j'ai juste une liste de gens à ignorer plus fort que les autres.",
        "Le bonheur ne s'achète pas, mais les pizzas si.",
        "Les câlins devraient être remboursés par la sécurité sociale.",
        "Le problème avec l'intelligence artificielle, c'est que la stupidité naturelle est toujours plus forte.",
        "Si tu veux un corps de rêve, il faut d'abord rêver longtemps.",
        "L'herbe est toujours plus verte ailleurs, sauf quand tu oublies d'arroser la tienne.",
        "Mon budget est équilibré : j'ai autant de dettes que de rêves.",
        "La vérité sort de la bouche des enfants, mais aussi beaucoup de bêtises.",
        "L'optimiste voit le verre à moitié plein, le pessimiste à moitié vide, et moi je me demande qui a bu.",
        "Les maths m'ont appris que les problèmes n'ont pas toujours de solution.",
        "Le bonheur, c'est une question de Wi-Fi stable.",
        "Les gens polis meurent en silence… dans les groupes WhatsApp.",
        "J'ai une mémoire sélective : je retiens les blagues et j'oublie les deadlines.",
        "Je ne suis pas fainéant, je donne juste une chance à l'univers de faire les choses à ma place.",
        "La paresse est le moteur du progrès : sans elle, on n'aurait jamais inventé la télécommande.",
        "Si tu veux être irremplaçable, fais en sorte qu'on ne puisse pas t'étiqueter en réunion Zoom.",
        "Les réunions qui auraient pu être des mails méritent une peine de prison symbolique.",
        "Je fais confiance à mon instinct, surtout quand il me dit de rester au lit.",
        "J'aime les gens qui rient de leurs problèmes. Surtout quand ce ne sont pas les miens.",
        "Je suis allergique aux lundis, mais le médecin ne veut pas me prescrire du vendredi.",
        "Le passé, c'est ce qui t'empêche d'être en retard dans le futur.",
        "Je me lève tôt pour avoir le temps de me recoucher.",
        "Les gens qui disent “le sport, c'est la vie” n'ont jamais connu la sieste.",
        "Je parle couramment l'ironie et je comprends le sarcasme en 3 dialectes.",
        "Mon objectif dans la vie : ne pas finir dans un PowerPoint de motivation.",
        "Un sourire ne coûte rien, sauf si tu as un appareil dentaire.",
        "Mon miroir est mon plus grand critique… et il a souvent raison.",
        "Si tu veux la paix, évite les discussions sur la politique et les pizzas à l'ananas.",
        "Je suis en couple avec mon lit, et notre relation est très stable.",
        "Les rêves, c'est bien, mais le sommeil, c'est mieux.",
        "Quand la vie te ferme une porte, vérifie si ce n'était pas juste la porte du frigo.",
        "Le pessimiste prévoit le pire, l'optimiste commande un dessert.",
        "Je n'ai pas échoué, j'ai trouvé 10 000 façons de ne pas réussir avant le café.",
        "Le hasard fait bien les choses, mais il travaille lentement.",
        "Si dormir était un sport, j'aurais une médaille d'or aux Jeux Olympiques.",
        "Les journées sans chocolat devraient être illégales.",
        "L'argent ne pousse pas sur les arbres, mais les impôts, si.",
        "Les mots gentils ne coûtent rien, mais certains valent un café.",
        "La vérité fait mal, mais le mensonge a souvent de très bonnes histoires.",
        "Je ne manque jamais une occasion de ne rien faire.",
        "Le secret du bonheur ? Une bonne sieste et du fromage.",
        "Mon cerveau a besoin d'une mise à jour, mais la flemme de redémarrer.",
        "Je préfère avoir tort avec humour que raison ennuyeusement.",
        "Le monde appartient à ceux qui ont du Wi-Fi et du café.",
        "Le bonheur, c'est quand ton mot de passe marche du premier coup.",
        "Je ne suis pas désorganisé, je suis en mode chaos créatif.",
        "Le travail ne tue pas, mais il fatigue beaucoup pour si peu de résultats.",
        "Ma devise : fais simple, mais dors beaucoup.",
        "Les gens heureux n'ont pas forcément tout, mais ils ont sûrement un chat.",
        "Je ne cherche pas le bonheur, j'attends qu'il me trouve en pyjama.",
        "La patience est une vertu… que je n'ai toujours pas installée.",
        "La curiosité a tué le chat, mais il devait s'ennuyer.",
        "Je ne râle pas, j'exprime mes émotions avec intensité.",
        "Si tu veux aller loin, prends une sieste avant.",
        "Le cerveau est comme un parachute : il ne sert à rien s'il est fermé, surtout le lundi matin.",
        "L'élégance, c'est savoir bâiller sans ouvrir la bouche.",
        "Si tu veux que tout aille bien, commence par un bon petit-déjeuner.",
        "Les meilleures décisions sont souvent celles qu'on n'a pas prises.",
        "Je ne suis pas de mauvaise humeur, j'ai juste besoin de plus de café.",
        "Les excuses les plus convaincantes viennent souvent après une grasse matinée.",
        "Le changement, c'est bien… sauf quand il s'agit de ton réveil.",
        "J'aime les gens ponctuels, ça me laisse du temps pour être en retard.",
        "Les souvenirs ne se mangent pas, mais certains ont un goût sucré.",
        "Rien n'est impossible, sauf plier un drap-housse proprement.",
        "La logique est un art que beaucoup pratiquent sans le savoir, souvent mal.",
        "L'optimisme est la caféine de l'âme.",
        "La vie sans humour, c'est comme un croissant sans beurre.",
        "Un compliment sincère vaut mieux qu'un long discours… surtout avant le café.",
        "La sagesse, c'est quand tu sais que tu ne sais pas, mais tu souris quand même.",
        "On ne choisit pas toujours son destin, mais on peut choisir sa playlist.",
        "Le courage, c'est parfois juste sortir du lit un lundi pluvieux.",
        "Il n'y a pas d'heure pour être heureux, mais il y a une heure pour le goûter.",
        "Les rêves ne vieillissent pas, ils changent juste de pyjama.",
    ]

    printer.set_with_default(bold=True, underline=True)
    printer.textln("Phrase du jour")
    printer.ln()

    def print_wrapped(text, width=48):
        """Wrap long text to avoid breaking words when printing."""
        for line in textwrap.wrap(
            text,
            width=width,
            break_long_words=False,
            break_on_hyphens=False,
        ):
            printer.textln(line)

    printer.set_with_default(align="center", font="b")
    print_wrapped(random.choice(citations))
    printer.ln()
    printer.ln()

    expressions_bonne_journee = [
        "Passe une journée qui brille plus fort que ton écran de téléphone.",
        "Que ton café soit fort et tes réunions courtes.",
        "Envole-toi vers une journée pleine de petits bonheurs.",
        "File vivre ta meilleure journée, sans bug ni cafetière vide.",
        "Que ton sourire soit ton accessoire du jour.",
        "Allez, éteins tout et va rayonner ailleurs que sur un écran.",
        "Que ton agenda te laisse un peu de place pour rêver.",
        "Bonne journée ! Et si elle ne l'est pas, fais semblant, ça finit par marcher.",
        "Que cette journée t'apporte plus de rires que d'emails.",
        "Fais de cette journée ton terrain de jeu préféré.",
        "Que le soleil t'accompagne, même s'il reste coincé derrière les nuages.",
        "À toi de jouer : transforme cette journée en aventure.",
        "Courage, aujourd'hui, c'est un peu demain en mieux.",
        "Respire, souris, et pars conquérir ta journée.",
        "Que chaque minute de ta journée soit un petit morceau de joie.",
        "À demain, même heure, même bonne humeur.",
        "Fais de cette journée une histoire qui mérite d'être racontée.",
        "Que ton humeur soit aussi douce que ton petit-déjeuner.",
        "Ferme ce chapitre et ouvre la porte du jour qui t'attend.",
        "Va semer du sourire un peu partout.",
        "Souviens-toi : le monde a besoin de ta bonne humeur aujourd'hui.",
        "Allez, file vivre une belle journée pleine de toi.",
        "Que cette journée soit aussi légère qu'une plume et aussi pétillante qu'un soda.",
        "N'oublie pas : chaque matin est une nouvelle chance de tout rater avec style.",
        "Bonne journée, et que la chance te colle aux baskets.",
        "Pars, souris, et reviens fier de ta journée.",
        "À plus tard, aventurier du quotidien.",
        "Que ton café et ton courage ne te quittent pas aujourd'hui.",
        "File écrire un nouveau chapitre de ta belle routine.",
        "C'est l'heure de quitter les mots pour rejoindre le monde.",
        "Bonne journée, héros discret de ton propre film.",
        "Souhaite-toi la plus belle des journées, tu la mérites.",
        "Que ton humeur reste haute, même si la météo descend bas.",
        "À demain pour de nouvelles aventures et d'autres éclats de rire.",
        "Bonne route à toi dans cette journée pleine de possibles.",
        "Allez, laisse les mots ici et va créer des souvenirs là-bas.",
        "Que cette journée te rende fier d'avoir ouvert les yeux.",
        "N'oublie pas ton plus bel accessoire : le sourire.",
        "File cueillir les petits plaisirs de la journée.",
        "Bonne journée, et n'oublie pas de respirer entre deux obligations.",
        "À demain, même énergie, peut-être un peu plus de café.",
        "Ferme ce moment, mais garde l'inspiration ouverte.",
        "Que cette journée soit douce, drôle et délicieusement imparfaite.",
        "Allez, direction la vraie vie, sans brouillon ni rature.",
        "Bonne journée, et que ton Wi-Fi intérieur reste connecté au positif.",
        "Pars léger, reviens heureux.",
        "Que cette journée soit un peu folle, mais toujours belle.",
        "C'est l'heure de débrancher le cerveau et d'allumer le sourire.",
        "Bonne journée, et si quelqu'un te contrarie, souris deux fois plus fort.",
        "Va colorier ta journée avec des fous rires.",
        "Que tes projets se réalisent et tes sandwichs ne tombent pas du mauvais côté.",
        "À demain, même planète, nouvelle aventure.",
        "Bonne journée, que ton courage soit rechargeable sans fil.",
        "Va semer des sourires, c'est contagieux.",
        "Que ton ombre te suive parce que tu brilles trop.",
        "Allez, file briller sans modération.",
        "Bonne journée, que tes pensées soient légères comme des bulles.",
        "Ferme la page, mais garde la magie dans les marges.",
        "Que ton chemin soit clair, même sans GPS.",
        "Bonne journée, et n'oublie pas : le positif attire le café.",
        "Sors conquis par la vie avant qu'elle ne t'attrape par surprise.",
        "Que chaque heure de ta journée ait une saveur différente.",
        "Allez, respire un grand coup et conquiers le monde, une tâche à la fois.",
        "Bonne journée à toi, capitaine du navire du quotidien.",
        "Que ta journée te surprenne agréablement, et pas l'inverse.",
        "Ferme cette page, ouvre ton sourire, le reste suivra.",
        "Bonne journée, remplie de petites victoires et de grandes envies.",
        "Souhaite-toi du bien, le reste viendra tout seul.",
        "Va, et que la bienveillance t'accompagne.",
        "Bonne journée, et que ton humour survive à tout.",
        "C'est parti pour une journée digne d'un bon épisode de série.",
        "File attraper les petits moments qui font les grandes journées.",
        "À demain, pour d'autres sourires et d'autres folies douces.",
        "Bonne journée, et n'oublie pas de t'émerveiller sans raison.",
        "Allez, que la force du café soit avec toi.",
        "Ferme ce moment comme un livre qu'on a aimé, et vis la suite.",
        "Bonne journée, et que la bienveillance guide chacun de tes pas.",
        "Va, et laisse derrière toi quelques éclats de rire.",
        "Que ta journée soit douce comme une chanson qu'on aime fredonner.",
        "À demain, même bonne humeur, même grain de folie.",
        "Bonne journée, sans bug, sans stress et sans chaussette perdue.",
        "Souhaite-toi de la douceur et du courage à volonté.",
        "File vers cette journée comme si c'était un cadeau à déballer.",
        "Bonne journée, remplie de sourires gratuits et de belles surprises.",
        "Va écrire la plus belle page de ce jour qui commence.",
        "Que cette journée soit aussi belle qu'une playlist parfaite.",
        "À demain, même ciel, autre lumière.",
        "Bonne journée, et n'oublie pas de te féliciter pour le simple fait d'exister.",
        "Ferme la parenthèse, mais garde la poésie.",
        "Que ta journée soit belle, même si ton réveil ne l'était pas.",
        "Allez, file vivre un jour ordinaire qui deviendra peut-être extraordinaire.",
        "Bonne journée, et que ton énergie soit plus forte que ta flemme.",
        "À demain, avec le sourire et, espérons-le, du chocolat.",
        "File cueillir les sourires et laisse tomber les nuages.",
        "Bonne journée, et que ton humeur soit aussi stable que ton Wi-Fi.",
        "Ferme la page du matin, le monde t'attend dehors.",
        "Que cette journée soit douce comme un dimanche même si on est mardi.",
        "Bonne journée, et n'oublie pas de rire sans raison.",
        "Va offrir ton énergie au monde, il en a bien besoin.",
        "À demain, plus reposé mais toujours inspiré.",
        "Bonne journée, et que le hasard te gâte un peu aujourd'hui.",
    ]

    printer.set_with_default(align="center")
    print_wrapped(random.choice(expressions_bonne_journee), width=44)
    printer.cut()


if __name__ == "__main__":
    main()
