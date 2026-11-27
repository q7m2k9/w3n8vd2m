#!/usr/bin/env python3
"""Génère la page d'aperçu d'une vidéo montée selon le style « visuel ».
Usage (depuis le dossier du Studio HV) :
  python ".claude/studio/styles/visuel/genere.py" ".claude/studio/styles/visuel/montages/<video>.json"
Le fichier JSON est la chronologie de la vidéo (titres, pages, traits, sous-titres, visages).
La page reprend l'interface du Studio (moteur officiel, lu sans le modifier) et y met les dessins du style."""
import base64, json, subprocess, sys, tempfile, shutil
from pathlib import Path
from urllib.parse import quote

ICI = Path(__file__).resolve().parent
RACINE = ICI.parents[3]
MOTION = RACINE / ".claude/skills/studiohv/motion"
APERCU = RACINE / ".claude/studio/apercu"

D = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
nom = D["sortie"]["base"]
base = APERCU / (nom + "_base.mp4")
s = (MOTION / "apercu-template.html").read_text(encoding="utf-8")


def remplacer(texte, debut, fin, nouveau):
    i, j = texte.index(debut), texte.index(fin)
    return texte[:i] + nouveau + texte[j:]


s = remplacer(s, "/* ---------- construction ---------- */", "/* ---------- zone sûre Facebook", (ICI / "bloc-visuel.js").read_text(encoding="utf-8"))
s = remplacer(s, "const marks=[];", "const debutDe=",
              "const marks=[];\n/* Style Visuel : aucun son sur les animations; Cloche sur le Yay, clic de souris à la fin, Carillon avant la fin */\nSND.souris={f:'clic-souris',g:(D.gains||{})['clic-souris'],lead:.02};\n"
              "if(D.outro.carillonT!=null)marks.push({t:D.outro.carillonT,k:'carillon'});(D.sonsExtra||[]).forEach(m=>marks.push({t:m.t,k:m.k}));\n")
s = remplacer(s, "const items=[];", "items.forEach(it=>it[0]=",
              "const items=[];\n"
              "D.pleins.forEach(P=>items.push([P.t0,'Page visuelle : '+P.nom]));\n"
              "items.push([D.outro.t0,'Page visuelle de fin : bouton et clic de souris']);\n")
s = s.replace("'Corrections sur le Style HV ('+D.nom+') :", "'Corrections sur le Style Visuel ('+D.nom+') :")
s = s.replace("</style>", (ICI / "visuel.css").read_text(encoding="utf-8") + "</style>", 1)
s = s.replace("<title>Aperçu animé - Style HV</title>", "<title>__TITRE__</title>")

polices = APERCU / "polices"
polices.mkdir(parents=True, exist_ok=True)
for f in (ICI / "polices").glob("*.ttf"):
    shutil.copy(f, polices / f.name)


def data(chemin, mime):
    return "data:%s;base64,%s" % (mime, base64.b64encode(Path(chemin).read_bytes()).decode())


with tempfile.TemporaryDirectory() as t:
    bas, voix = Path(t) / "bas.mp4", Path(t) / "voix.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(base), "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "28", "-an", str(bas)], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(base), "-vn", "-c:a", "libmp3lame", "-b:a", "160k", str(voix)], check=True)
    sons = {k: data(MOTION / "sons" / (k + ".mp3"), "audio/mpeg") for k in D["sonsUtilises"]}
    s = s.replace('const VBAS=/*__VBAS__*/""', 'const VBAS="%s"' % data(bas, "video/mp4"))
    s = s.replace('const VOIX=/*__VOIX__*/""', 'const VOIX="%s"' % data(voix, "audio/mpeg"))
s = s.replace("const SONS=/*__SONS__*/{}", "const SONS=" + json.dumps(sons))
s = s.replace("const D=/*__TIMELINE__*/{}", "const D=" + json.dumps(D, ensure_ascii=False))
s = s.replace("__POLICES__", "apercu/polices").replace("__VIDEO__", "apercu/" + quote(base.name)).replace("__ERIKA__", "apercu/Erika.png")
s = s.replace("__TITRE__", "Aperçu animé - Style Visuel")
sortie = RACINE / ".claude/studio" / ("apercu-motion_%s.html" % nom)
sortie.write_text(s, encoding="utf-8")
print("page :", sortie)
