#!/usr/bin/env python3
"""Storyboard du Style Visuel : vraies images rendues par la page d'aperçu, mise en page OFFICIELLE (storyboard_hv.py, figée).
Usage : python storyboard.py [planche-de-controle.jpg]"""
import io, json, subprocess, sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ICI = Path(__file__).resolve().parent
R = ICI.parents[3]
sys.path.insert(0, str(R / ".claude/skills/studiohv/motion"))
import storyboard_hv

NOM = "Liste attente MVT visuel"
HTML = R / (".claude/studio/apercu-motion_%s.html" % NOM)
PDF = R / "3. Storyboard/Liste attente MVT visuel_storyboard_V2.pdf"
D = json.loads((ICI / "montages/liste-attente-mvt.json").read_text(encoding="utf-8"))

# un élément par plan : (instant montré, visuel, effet, sons) - mêmes numéros que la version précédente
V = "Voix seule."
INFOS = [
    (2.3, "Publication Haute Visibilité; « MVT » s'écrit en commentaire puis apparaît publié.", "Visible dès la première image.", V),
    (6.2, "Tu filmes, Le montage, Tu publies; puis un grand « Yay ! » avec éclats.", "Les cartes montent une à une; le « Yay ! » rebondit.", "Le « Yay ! » (remis au complet) et la Cloche."),
    (9.4, "Cloche de notification (3), puis « Le lien sous la vidéo ».", "La cloche se balance; la carte monte.", V),
    (10.95, "D'abord Prénom, Nom de famille, Courriel et Envoyer; ensuite les 3 cadeaux (jamais les deux en même temps).", "Le formulaire s'efface vers le haut, puis les cadeaux arrivent.", V),
    (13.8, "« Cadeau exclusif » et un grand 1. Trait 1 sur 3.", "Le chiffre grossit doucement.", V),
    (17.0, "Outil gratuit : 4 étapes cochées.", "Cartes de bas en haut, coches une à une.", V),
    (18.4, "Un grand 2. Trait 2 sur 3.", "Le chiffre grossit doucement.", V),
    (21.9, "File d'attente : « Toi » passe en premier (Priorité), puis Montage Vidéo Turbo.", "La carte « Toi » remonte la file.", V),
    (24.1, "Tarif régulier barré, puis « Ton tarif préférentiel » (aucun prix inventé).", "Cartes de bas en haut.", V),
    (26.0, "Ton produit digital « en création ».", "La barre se remplit.", V),
    (28.9, "Montage qui se fait : coupes, sous-titres, zooms.", "Les passages vides disparaissent.", V),
    (30.8, "Barres Résultats et Temps, « Ton montage ».", "Les barres montent.", V),
    (33.2, "Un téléphone qui montre une page de ce style.", "La barre de lecture avance.", V),
    (34.8, "Un grand 3. Trait 3 sur 3.", "Le chiffre grossit doucement.", V),
    (37.5, "Les idées, le tournage, le montage; « Chaîne privée ».", "Cartes de bas en haut.", V),
    (39.45, "« Le lien sous la vidéo » et une grande flèche.", "La flèche rebondit.", V),
    (41.7, "Prénom, Nom de famille, Courriel et bouton Envoyer.", "Les champs s'écrivent; le bouton s'enfonce.", V),
    (D["outro"]["bouton"]["tTap"] + .12, "Ton Outro, avec le bouton « Clique sur le lien » et la souris.", "Fondu enchaîné; la souris arrive et clique.", "Carillon doux avant la fin; Clic de souris au moment du clic."),
]
P = [dict(t0=p["t0"], t1=min(p["t1"], D["outro"]["t0"]), titre=p["nom"]) for p in D["pleins"]]
P.append(dict(t0=D["outro"]["t0"], t1=D["duree"], titre="Fin : clique sur le lien"))
assert len(P) == len(INFOS)

with sync_playwright() as pw:
    b = pw.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    erreurs = []
    pg.on("pageerror", lambda e: erreurs.append(e.message))
    pg.goto(HTML.as_uri() + "?rendu=1&t=0")
    pg.wait_for_timeout(1500)

    def image(t):
        pg.evaluate("async t=>{window.hvRender(t);await window.hvWait()}", t)
        return Image.open(io.BytesIO(pg.screenshot(omit_background=True))).convert("RGBA")

    for p, (t, visuel, effet, sons) in zip(P, INFOS):
        dit = " ".join(m["w"] for g in D["sousTitres"] if p["t0"] - .05 <= g["t0"] < p["t1"] - .05 for m in g["mots"])
        if "Yay" in visuel:
            dit += " ... Yay !"
        p.update(image=image(t), texte=dit or "(aucune parole)", visuel=visuel, effet=effet, sons=sons)
    # contrôle : la vidéo d'origine n'apparaît à aucune image (calque opaque partout)
    trous = [i / 10 for i in range(0, int(D["duree"] * 10), 3) if image(i / 10).getchannel("A").getextrema()[0] < 250]
    b.close()
print("erreurs", erreurs, "| instants où la vidéo paraît :", trous)

directives = [
    ("Durée et coupes", ["45 secondes. Mêmes coupes qu'avant, plus le « Yay ! » remis au complet après « automatisé » (environ 1 seconde)."]),
    ("Tout est visuel", ["18 pages visuelles. La vidéo filmée n'apparaît jamais : on entend les voix. L'Outro (avec les photos) termine la vidéo."]),
    ("En haut", ["Plans 1 à 4 : HAUTE VISIBILITÉ avec un trait de chaque côté.", "Plans 5 à 17 : le nom sans traits de côté, avec les 3 traits de progression en dessous."]),
    ("Hauteur du texte", ["Tout est descendu : le nom à environ 310 px du haut, les sous-titres à 1435 px au plus bas, dans la zone sûre."]),
    ("Look de la vidéo", ["Background Motion Design, couleurs HV, titres en Instrument Serif, textes en Inter."]),
    ("Sous-titres", ["2 à 3 mots, même hauteur; chaque mot s'allume quand il est dit, les mots importants en brun."]),
    ("Sons", ["Aucun son sur les animations, sauf la Cloche sur le « Yay ! » et le nouveau Clic de souris à la fin.", "Carillon doux avant la fin."]),
    ("Voix", ["Égalisée passage par passage, sans compression; le « Yay ! » reste plus fort que la voix parlée."]),
    ("Pas exporté", ["Aucune vidéo finale. Après ton accord : l'aperçu animé. L'export seulement quand tu le demandes."]),
    ("À confirmer", ["Textes ajoutés à l'écran : plan 2 (« ta vidéo prête »), plan 6 (les 4 étapes), plan 11 (coupes, sous-titres, zooms), plan 15 (idées, tournage, montage, « Chaîne privée »)."]),
]
pages = storyboard_hv.generer(PDF, "Style Visuel", "Liste attente MVT", directives, P)
if len(sys.argv) > 1:
    w, h = 400, 566
    planche = Image.new("RGB", (w * 5, h * 2), "white")
    for i, im in enumerate(pages[:10]):
        planche.paste(im.resize((w, h)), (i % 5 * w, i // 5 * h))
    planche.save(sys.argv[1], quality=88)
for k, n in ((0, "page-commentaire"), (3, "page-cadeaux"), (4, "grand-chiffre"), (17, "fin")):
    P[k]["image"].convert("RGB").resize((540, 960), Image.LANCZOS).save(ICI / "apercus" / (n + ".jpg"), quality=90)
print(PDF, len(pages), "pages")
