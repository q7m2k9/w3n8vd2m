"""Chronologie de « Liste attente MVT » selon le Style Visuel (écrit le .json à côté)."""
import json
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parents[4]
prec = None
for ligne in (RACINE / ".claude/studio/apercu-motion_bold.html").read_text(encoding="utf-8").splitlines():
    if ligne.startswith("const D="):
        prec, _ = json.JSONDecoder(strict=False).raw_decode(ligne[8:])
        break

BG = "apercu/Background%20Motion%20Design.png"


D_YAY = 31 / 30          # « Yay ! » remis dans le montage : 31 images ajoutées à 5,6 s


def S(t):
    return round(t + D_YAY, 4) if t >= 5.6 - 1e-6 else t


def page(type_, a, b, nom, l=None, **k):
    return dict(type=type_, t0=S(a), t1=S(b), nom=nom, l=l, fond=BG, **k)


pages = [
    page("commente", 0.0, 2.92, "Tu as commenté MVT", ["Tu as commenté", "MVT ?"], tPost=0.0, tSaisie=1.05, tTap=1.75),
    page("flux", 2.92, 5.6, "Ton montage automatisé, Yay !", ["Ton montage", "automatisé"], tYay=5.66, items=[
        dict(t=3.2, ic="video", nom="Tu filmes", sous="ta vidéo"),
        dict(t=3.74, ic="ciseaux", nom="Le montage", sous="automatisé"),
        dict(t=4.46, ic="envoi", nom="Tu publies", sous="ta vidéo prête")]),
    page("rappel", 5.6, 8.73, "Pour ne rien manquer", ["Pour ne rien", "manquer"], tCloche=S(6.3), tLien=S(7.9)),
    page("cadeaux", 8.73, 12.0, "Tes 3 cadeaux exclusifs", ["Tes 3 cadeaux", "exclusifs"], tForm=S(8.85), tTap=S(9.85), tSortie=S(10.15), items=[
        dict(t=S(10.4), sous="un outil gratuit"), dict(t=S(10.75), sous="l'accès en priorité"), dict(t=S(11.1), sous="les coulisses")]),
    page("numero", 12.0, 13.15, "Cadeau exclusif 1", n="1", sur="Cadeau exclusif"),
    page("etapes", 13.15, 16.3, "Un outil gratuit, étape par étape", ["Un outil", "gratuit"], badge="Étape par étape", tBadge=S(15.2), items=[
        dict(t=S(13.75), nom="importer ta vidéo"), dict(t=S(14.2), nom="couper les silences"),
        dict(t=S(14.75), nom="ajouter tes sous-titres"), dict(t=S(15.45), nom="exporter et publier")]),
    page("numero", 16.3, 17.55, "Cadeau exclusif 2", n="2", sur="Cadeau exclusif"),
    page("priorite", 17.55, 21.43, "Accès en priorité", ["Accès", "en priorité"], tMonte=S(18.75), tTurbo=S(20.2)),
    page("prix", 21.43, 23.43, "Un tarif préférentiel", ["Montage", "Vidéo Turbo"], tA=S(21.65), tB=S(22.2)),
    page("produit", 23.43, 25.26, "Un produit digital", ["Un produit", "digital"], tCree=S(23.9)),
    page("montage", 25.26, 28.13, "Automatiser ton processus", ["Automatise", "ton processus"], tCoupe=S(26.0), items=[
        dict(t=S(26.2), nom="Les coupes"), dict(t=S(26.7), nom="Les sous-titres"), dict(t=S(27.2), nom="Les zooms")]),
    page("resultat", 28.13, 30.03, "Un résultat ultra pro", ["Un résultat", "ultra pro"], tDeb=S(28.45), tPro=S(29.15)),
    page("apercu", 30.03, 32.53, "Comme cette vidéo", ["Comme", "cette vidéo"], image="apercu/exemple-visuel.jpg"),
    page("numero", 32.53, 33.9, "Cadeau exclusif 3", n="3", sur="Cadeau exclusif"),
    page("coulisses", 33.9, 37.07, "Les coulisses de la création", ["Les coulisses", "de la création"], tPrive=S(36.2), items=[
        dict(t=S(34.4), ic="etoile", nom="Les idées", sous="de la création"),
        dict(t=S(35.0), ic="video", nom="Le tournage", sous="en coulisses"),
        dict(t=S(35.6), ic="ciseaux", nom="Le montage", sous="Vidéo Turbo")]),
    page("clique", 37.07, 38.76, "Clique ici", ["Clique", "ici"], tFleche=S(37.9)),
    page("infos", 38.76, 41.75, "Rentre tes infos", ["Rentre", "tes infos"], final=True, tForm=S(38.85), tTap=S(40.45)),
]
OT = S(41.1)
BOUTON = dict(t=round(OT + .7, 3), tTap=round(OT + 1.65, 3))

# sous-titres : mêmes mots et mêmes temps que le montage précédent, même hauteur partout
accents = ("mvt", "automatis", "cadeaux", "priorité", "turbo", "préférentiel", "digital", "pro", "coulisses", "clique", "gratuit", "lien")
subs = []
for g in prec["sousTitres"]:
    mots = []
    for m in g["mots"]:
        w = m["w"]
        n = w.lower().strip(".,!?…")
        acc = any(n == a or (len(a) > 4 and n.startswith(a)) for a in accents)
        mots.append(dict(w=w, s=m.get("s", g["t0"]), acc=acc, colle=bool(m.get("colle"))))
    subs.append(dict(t0=g["t0"], t1=g["t1"], mots=mots))
# corrections après nouvelle écoute : « processus de montage vidéo » manquait, « rentres », « Montage Vidéo Turbo »


def bloc(t0, t1, *mots):
    return dict(t0=t0, t1=t1, mots=[dict(w=w, s=s, acc=a, colle=False) for w, s, a in mots])


subs = [g for g in subs if not 25.2 <= g["t0"] < 28.0]
subs += [bloc(25.26, 26.55, ("pour", 25.44, False), ("automatiser", 25.88, True)),
         bloc(26.55, 27.34, ("ton", 26.62, False), ("processus", 26.86, False)),
         bloc(27.34, 28.2, ("de", 27.38, False), ("montage", 27.54, False), ("vidéo", 27.78, False))]
subs.sort(key=lambda g: g["t0"])
for g in subs:
    if abs(g["t0"] - 28.02) < .05:
        g["t0"] = 28.2
    turbo = any(x["w"].lower() == "turbo" for x in g["mots"]) or abs(g["t0"] - 20.0) < .1
    for m in g["mots"]:
        if m["w"] == "rends":
            m["w"] = "rentres"
        if turbo and m["w"] in ("montage", "vidéo", "turbo"):
            m["w"] = m["w"].capitalize()
subs[0]["mots"][0]["w"] = subs[0]["mots"][0]["w"][:1].upper() + subs[0]["mots"][0]["w"][1:]

# décalage des sous-titres après le « Yay ! », puis bloc du « Yay ! »
for g in subs:
    if g["t0"] >= 5.6 - 1e-6:
        g["t0"], g["t1"] = S(g["t0"]), S(g["t1"])
        for m in g["mots"]:
            m["s"] = round(m["s"] + D_YAY, 4)
# le grand « Yay ! » à l'écran sert de sous-titre (pas de doublon)
subs.sort(key=lambda g: g["t0"])
gains = dict(prec["gains"])
gains["clic-souris"] = 0.49                      # crête à -14 dBFS
reperes = dict(prec["reperes"])
reperes["clic-souris"] = dict(debut=0.02, fin=0.13, duree=0.32)
D = dict(
    nom="Style Visuel", duree=round(prec["duree"] + D_YAY, 4), entreprise="HAUTE VISIBILITÉ",
    traits=[dict(t0=S(12.0), t1=S(16.3)), dict(t0=S(16.3), t1=S(23.43)), dict(t0=S(32.53), t1=S(37.07))],
    sons=prec["sons"], gains=gains, reperes=reperes, sonsUtilises=["carillon", "cloche", "clic-souris"],
    sonsExtra=[dict(t=5.70, k="ding"), dict(t=BOUTON["tTap"], k="souris")],
    mise=dict(subY=1435), titres=[], pleins=pages, sousTitres=subs,
    plans=[dict(n=1, t0=0, t1=99, faces=[], y=1435)],
    avatar="apercu/Photo%20de%20profil%20HV.png",
    outro=dict(prec["outro"], t0=OT, carillonT=round(OT - .15, 3), bouton=BOUTON),
    sortie=dict(dossier="6. Publication", base="Liste attente MVT visuel"), filtres=[],
)
(ICI / "liste-attente-mvt.json").write_text(json.dumps(D, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", len(subs), "sous-titres,", len(pages), "pages, durée", D["duree"])
