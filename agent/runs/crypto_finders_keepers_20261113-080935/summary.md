

---
## Résumé au tour 10 (08:12:25)

## Fait
- Copie du fichier challenge `finderskeepers.mp4` dans le dossier de travail.
- Identification du format (MP4/ISO Media) via `file` et analyse hexadécimale (`xxd`).
- Extraction des chaînes de caractères (`strings`) et analyse Python pour isoler les métadonnées.
- Découverte d'un bloc XMP contenant une chaîne encodée en Base64.
- Décodage Base64 réussi : `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.

## Échecs / impasses
- Tentative d'analyse vidéo bloquée par l'absence de `ffmpeg`/`ffprobe`.
- Hypothèse de stéganographie LSB (pixels) non confirmée (données brutes bruitées).
- Le résultat du décodage Base64 n'est pas un flag lisible immédiatement (obfuscation résiduelle).

## État actuel
- Payload crypté extrait : `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- Contexte CTF : CSAW (suggère fortement un format `csaw{...}`).
- Fichier source toujours disponible pour analyse plus poussée.

## Prochaines pistes
- Cryptanalyse du préfixe `esnp` pour trouver la clé de substitution (probablement `csaw`).
- Appliquer la logique de déchiffrement trouvée au contenu entre accolades.
- Si échec, réinstaller `ffmpeg` pour inspecter le flux vidéo brut ou les trames.


---
## Résumé au tour 20 (08:23:45)

## Fait
- Décodage Base64 initial réussi : `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- Analyse Python du préfixe : établissement d'une table de substitution partielle (`e`→`c`, `n`→`a`, `p`→`w`, `s`→`s`).
- Création et exécution de l'outil `mp4_analyzer` sur `finderskeepers.mp4`.
- Confirmation que la chaîne chiffrée est stockée dans les métadonnées XMP du fichier vidéo.

## Échecs / impasses
- Outil `substitution_solver` : aucune sortie exploitable.
- Tentatives de ROT13 et décalages simples (Shift +1, +13) sur le contenu interne : résultats illisibles.
- Décodage "Leet" partiel : donne des fragments (`doc`, `go`, `oops`) mais ne résout pas toute la chaîne.
- Hypothèse de substitution monoalphabétique simple non encore totalement validée pour le corps du flag.

## État actuel
- Flag partiel : `csaw{d0c_@yz@gl_ma0j_wm3z3_g0_o00s}`.
- Indices clés : `0` semble correspondre à `o`, `3` pourrait être `e`.
- Structure suspectée : `csaw{doc_azure_..._go_oops}` (basé sur `@yz@gl` → `azure` et `o00s` → `oops`).
- Source confirmée : `finderskeepers.mp4`.

## Prochaines pistes
- Déduire la clé de substitution complète en croisant les indices (`@`→`a`, `y`→`z`, `z`→`u`, `g`→`r`, `l`→`e`).
- Tester un script de dictionnaire utilisant la table de substitution partielle pour valider les mots (`manj` vs `manage` vs `main`).
- Vérifier si la substitution est un chiffrement affine ou basé sur un mot-clé spécifique.
