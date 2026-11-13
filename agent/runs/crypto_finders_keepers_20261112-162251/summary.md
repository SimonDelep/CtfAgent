

---
## Résumé au tour 10 (16:26:02)

## Fait (actions utiles et ce qu'elles ont donné)
- Copie du challenge `finderskeepers.mp4` dans le dossier de travail.
- Identification du type de fichier (ISO Media/MP4) via `file`.
- Extraction des chaînes de caractères avec `strings`.
- Découverte d'une chaîne Base64 dans les métadonnées XMP : `ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30=`.
- Décodage Base64 réussi donnant : `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- Calcul de la clé XOR partielle basée sur le préfixe attendu (`csaw` vs `esnp`).

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- Outils manquants : `ffprobe` et `exiftool` absents, forcé d'utiliser `strings`.
- XOR avec clé courte `[6, 0, 15, 7]` : fonctionne sur le préfixe mais corrompt le reste du flag.
- Tentatives de XOR avec des mots-clés standards (`key`, `csaw`, `flag`, `seed`).
- Décalage Caesar simple (shift 26) : aucun résultat lisible.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichier :** `finderskeepers.mp4` (1.6 Mo).
- **Payload brut :** `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- **Problème :** Le format du flag est `csaw{...}`, mais le texte est chiffré. La clé XOR déduite du début ne s'applique pas uniformément au reste.
- **Indice :** La transformation semble être un XOR, mais la clé est probablement plus longue ou dépend de la position.

## Prochaines pistes
- Analyser la séquence XOR complète caractère par caractère pour trouver un motif récurrent (clé plus longue).
- Tester des clés basées sur le nom du challenge (`finderskeepers`) ou la longueur du flag.
- Vérifier si la clé est liée à la position de chaque caractère (XOR avec l'index).
- Explorer si la vidéo contient une autre couche de stéganographie (moins prioritaire vu la métadonnée).
