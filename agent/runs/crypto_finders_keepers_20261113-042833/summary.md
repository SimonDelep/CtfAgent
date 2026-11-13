

---
## Résumé au tour 10 (04:31:40)

## Fait
- Copie et identification du fichier `finderskeepers.mp4` (1.6MB, ISO Media).
- Extraction des métadonnées XMP via la commande `strings`.
- Décodage Base64 trouvé dans le champ `dc:subject` : `ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30=`.
- Récupération de la chaîne déchiffrée : `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.

## Échecs / impasses
- Tentatives de décalage (ROT 0-25) sur la chaîne complète : aucun résultat lisible.
- Analyse XOR sur le préfixe : clés non constantes (6, 0, 15, 7), pas de motif répétitif immédiat.
- Outil `substitution_solver` sans résultat significatif sur le payload complet.

## État actuel
- Le contenu à l'intérieur des accolades (`d0c_@yz@gl_mn0j_pm3z3_g0_o00s`) semble correspondre au format attendu.
- Le préfixe `esnp` est la seule anomalie par rapport au format standard `csaw`.
- L'obfuscation semble se limiter aux 4 premiers caractères.

## Prochaines pistes
- Tester un chiffrement Vigenère ou Affine sur le préfixe `esnp` avec des clés courtes (ex: "CSAW", "KEY").
- Vérifier si les valeurs XOR (06 00 0F 07) correspondent à une clé ASCII lisible ou un mot clé du challenge.
- Examiner le reste du fichier MP4 (stéganographie LSB/audio) si le préfixe reste bloquant.


---
## Résumé au tour 20 (04:38:05)

## Fait
- **Extraction de clé XOR** : Calculé la différence binaire entre `esnp` et `csaw`, obtenant la clé `[6, 0, 15, 7]`.
- **Validation du préfixe** : Confirmé que cette clé transforme parfaitement `esnp` en `csaw`.
- **Élimination de pistes** : Testé ROT et Vigenère avec des mots-clés standards sur le contenu, résultats non concluants.

## Échecs / impasses
- **Vigenère classique** : Tentatives avec les clés `CSAW`, `KEY`, `FLAG`, `SECRET` sur le payload (donne du texte illisible).
- **Base64** : Substitution de `@` par `+` ou `/` et décodage Base64 (résultats binaires/corrompus).
- **XOR complet** : Application de la clé `[6, 0, 15, 7]` sur toute la chaîne (produit `csaw` suivi de bruit).
- **ASCII XOR** : Interprétation directe des valeurs XOR (6, 0, 15, 7) comme caractères ASCII (caractères de contrôle).

## État actuel
- **Préfixe résolu** : Le flag commence par `csaw{`.
- **Payload** : `d0c_@yz@gl_mn0j_pm3z3_g0_o00s`.
- **Clé connue** : `[6, 0, 15, 7]` (valide pour le préfixe).
- **Problème** : Incertitude sur la méthode de décodage du contenu (XOR cyclique, substitution ou déjà en clair).

## Prochaines pistes
- **XOR cyclique** : Appliquer la clé `[6, 0, 15, 7]` de manière répétée sur le contenu entre accolades.
- **Analyse du caractère `@`** : Vérifier si `@` est un espace, un underscore ou un caractère chiffré spécifique.
- **Contexte source** : Si le XOR échoue, réexaminer le fichier MP4 original pour des indices visuels ou audio.


---
## Résumé au tour 30 (04:42:31)

## Fait
(résumé mécanique — appels effectués)
- run_shell ×2
- copy_challenge_file ×1
- run_shell ×1
- run_shell ×1
- run_python ×1
- run_python ×1
- run_python ×1
- substitution_solver ×1
- run_python ×1
- run_python ×1
## Prochaines pistes
Varier l'approche.


---
## Résumé au tour 40 (04:44:24)

## Fait (actions utiles et ce qu'elles ont donné)
- Identification du fichier : `finderskeepers.mp4` (1.6 Mo), format ISO Media standard.
- Analyse de l'en-tête : Vérification hexadécimale des 1000 premiers octets (atomes `ftyp`, `moov`, `tkhd` présents).
- Vérification de l'environnement : Confirmation que Python est disponible et que `Pillow` est installé.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- Outils système manquants : `ffprobe` et `ffmpeg` absents du PATH.
- Bibliothèques Python absentes : `cv2`, `moviepy`, `av` et `imageio` non installés (tentatives d'import échouées).
- Tentative naïve : Ouvrir le `.mp4` directement avec `PIL.Image.open()` (échec logique, nécessite un décodeur).

## État actuel (ce qu'on sait, fichiers/indices clés)
- Le fichier est un conteneur vidéo valide, pas de corruption apparente.
- Aucune donnée cachée visible dans les métadonnées basiques ou le début du fichier.
- Blocage technique : Impossible d'extraire les frames ou l'audio sans outil de décodage.

## Prochaines pistes
- **Installer un décodeur** : Tenter `apt install ffmpeg` ou `pip install av` pour lire la vidéo.
- **Extraction de frames** : Sauvegarder les images séquentiellement pour chercher des stéganogrammes (LSB, texte visible).
- **Analyse audio** : Vérifier le spectre audio (spectrogramme) une fois le fichier décodé.
- **Tail check** : Vérifier s'il y a des données appendées après la fin du conteneur MP4 (`xxd` ou `strings`).
