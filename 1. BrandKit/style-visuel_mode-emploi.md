# Style Visuel - monter une nouvelle vidéo

Commande de la cliente : « monte ma vidéo selon le Style Visuel ». Lire `style-visuel.json` et `style-visuel_notes.md`.
Les fichiers du moteur nommés ci-dessous (`montages/`, `bloc-visuel.js`, `storyboard.py`) sont dans `.claude/studio/styles/visuel/`.

1. BrandKit : une seule confirmation (aujourd'hui : palette HV, Instrument Serif et Inter).
2. Vidéo de base : couper les silences et les prises ratées (grille de 30 i/s), ne jamais couper un cri de joie, puis
   `python .claude/skills/studiohv/motion/egaliser_voix.py <base> ".claude/studio/apercu/<nom>_base.mp4" "<débuts des passages>" ["<début>=-6" pour garder un cri vivant]`.
3. Chronologie : créer `montages/<nom>.json` sur le modèle de `montages/liste-attente-mvt.json` (jamais écraser celui d'une autre vidéo).
   Champs : entreprise, traits (un par point annoncé), pleins (pages, bout à bout, la dernière avec final:true et prolongée de 0,65 s sous l'Outro),
   sousTitres (temps mot à mot, Whisper puis relecture), sonsExtra, outro (avec bouton t et tTap), sortie.base = « <nom> visuel ».
4. Pages disponibles (dessins dans `bloc-visuel.js`) : commente, flux, rappel, cadeaux, numero, etapes, priorite, prix, produit, montage,
   resultat, apercu, coulisses, clique, infos. Chaque page doit illustrer exactement ce qui est dit; les textes ajoutés se font confirmer.
   Certaines pages ont des textes fixes (Cadeau, Publier, Étape, Résultats, Temps, Haute Visibilité) : les adapter à la nouvelle vidéo.
   Une idée sans page existante : dessiner une nouvelle page dans ce dossier seulement.
5. Aperçu : `python ".claude/studio/styles/visuel/genere.py" ".claude/studio/styles/visuel/montages/<nom>.json"` (produit `.claude/studio/apercu-motion_<nom> visuel.html`, non ouvert avant l'accord sur le storyboard).
6. Storyboard : adapter le nom, la liste des plans et les directives dans une copie de `storyboard.py`; la mise en page vient toujours de `storyboard_hv.py` (figée).
7. Après l'accord : ouvrir l'aperçu. Export seulement sur demande, avec `exporter.py --ok-de-la-cliente --voix <v> --volume <s>`.

Exemple de préparation (Liste attente MVT) : `montages/chronologie_liste-attente-mvt.py` (reprend les sous-titres du montage « bold » : garder cette page).
