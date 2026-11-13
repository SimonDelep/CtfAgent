

---
## Résumé au tour 10 (11:49:02)

## Fait
- Récupération et analyse du fichier `finderskeepers.mp4`.
- Extraction des métadonnées XMP contenant une chaîne Base64 : `ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30=`.
- Décodage Base64 réussi : `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- Identification du préfixe attendu `csaw{...}` et établissement d'une correspondance partielle (`e->c`, `n->a`, `p->w`).

## Échecs / impasses
- Les rotations classiques (ROT13, ROT47, etc.) n'ont pas produit de texte lisible.
- Le solveur de substitution automatique n'a pas retourné de clé complète.
- L'application manuelle de la substitution partielle donne `csaw{d0c__yz_gl_ma0j_wm3z3_g0_o00s}`, qui reste cryptique et peu lisible.
- Répétition de scripts Python similaires sans découverte de nouvelle règle de chiffrement.

## État actuel
- **Flag brut décodé :** `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`
- **Hypothèse :** Substitution monoalphabétique + `@` = `_`.
- **Résultat partiel :** `csaw{d0c__yz_gl_ma0j_wm3z3_g0_o00s}`.
- Le suffixe ne forme pas encore de mots anglais évidents, la clé de substitution est incomplète.

## Prochaines pistes
- **Analyse de fréquence :** Tenter de deviner des mots courants (ex: "crypto", "secret") dans le suffixe pour compléter la clé.
- **Vérification vidéo :** Examiner le contenu visuel ou audio du MP4 pour une stéganographie complémentaire.
- **Chiffrement alternatif :** Vérifier si c'est un Vigenère ou un chiffrement par décalage variable plutôt qu'une substitution simple.
- **Recherche de pattern :** Analyser la structure `d0c_@yz@gl` pour identifier des mots techniques ou des noms propres.


---
## Résumé au tour 20 (11:58:57)

## Fait
- **Décodage Base64** : Extrait du MP4, donne `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- **Substitution partielle** : Identifié `esnp` → `csaw`, `@` → `_`, `0` → `o`, `3` → `e`.
- **Métadonnées** : Extraction XMP révélant `engine=jc` (Canva).
- **Analyse binaire** : Vérification des chaînes (`strings`) et structure MP4 (`ftyp`, `moov`).

## Échecs / impasses
- **Copie de fichier** : `cp /challenge/...` inutile (fichier déjà local).
- **Outil stéganographie** : `mp4_stego_analyzer` (forgé) muet (probable manque de `ffmpeg`).
- **Chiffrement simple** : ROT13 et décalages linéaires (Caesar) incohérents (différences variables : -2, 0, -13, +7).
- **Chaînes brutes** : `strings` a produit du bruit sans flag clair.

## État actuel
- **Fichier clé** : `finderskeepers.mp4` (1.6 Mo).
- **Flag partiel** : `csaw{doc__yz_gl_maoj_wmeze_go_ooos}`.
- **Indice majeur** : `engine=jc` dans les métadonnées (suggère "Jules César" ou clé "JC").
- **Inconnues** : Mapping des lettres restantes (`d, y, z, g, l, m, j, w`) non résolu.

## Prochaines pistes
- **Exploiter l'indice "jc"** : Tester une substitution monoalphabétique basée sur une clé dérivée de "JC" ou un décalage spécifique.
- **Analyse de fréquence** : Utiliser les mots partiels (`doc`, `go`, `ooos`) pour deviner les lettres manquantes.
- **Recherche de mots** : Chercher des mots anglais cohérents dans `yz_gl_maoj_wmeze`.
- **Vérifier l'outil stego** : Réparer `mp4_stego_analyzer` ou utiliser `binwalk`/`zsteg` pour voir si le MP4 cache autre chose.


---
## Résumé au tour 30 (12:03:41)

## Fait
- **Extraction MP4 :** Commande `strings` sur `finderskeepers.mp4` a révélé des métadonnées XMP.
- **Base64 :** Chaîne `ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30=` extraite et décodée en `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- **Cryptanalyse :** Identification d'un chiffrement de Vigenère. Déduction de la clé `cant` en comparant le préfixe chiffré `esnp` au format attendu `csaw`.
- **Décryptage partiel :** Application de la clé `cant` produisant `csaw{b0c_@lg@el_zu0h_pz3g3_e0_o00f}`.

## Échecs / impasses
- **Outil automatique :** `substitution_solver` a retourné vide (trop générique pour ce cas).
- **Approche brute :** Tentatives initiales de ROT/CAESAR directes sans clé dérivée ont échoué.
- **Symboles ignorés :** Le script Vigenère a laissé passer `@`, `0`, `3` sans transformation, créant une impasse sur ces caractères.

## État actuel
- **Fichier clé :** `finderskeepers.mp4` (métadonnées XMP).
- **Ciphertext :** `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- **Clé Vigenère :** `cant`.
- **Plaintext partiel :** `csaw{b0c_@lg@el_zu0h_pz3g3_e0_o00f}`.
- **Hypothèses de substitution :** `0` → `o`, `3` → `e`, `@` → `_` (basé sur la structure du flag).

## Prochaines pistes
- **Substitution finale :** Appliquer manuellement les mappings `0`, `3`, `@` pour former des mots anglais cohérents.
- **Vérification de sens :** Analyser `b0c`, `zu0h`, `pzege` pour valider les hypothèses (ex: `doc`, `zoom`, `pege` ?).
- **Flag complet :** Reconstruire la chaîne finale et tester la validité.
