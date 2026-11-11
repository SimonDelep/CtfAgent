

---
## Résumé au tour 10 (23:02:56)

## Fait (actions utiles et ce qu'elles ont donné)
- **Extraction et identification :** Copie du fichier `finderskeepers.mp4` et confirmation du type (ISO Media/MP4) via commande `file`.
- **Analyse binaire :** Utilisation de Python pour scanner les chaînes ASCII (les outils `ffprobe` et `exiftool` étant absents).
- **Découverte d'indice :** Identification d'une chaîne Base64 cachée dans les métadonnées XMP du fichier.
- **Décodage :** Conversion réussie de la chaîne Base64 en texte lisible : `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Outils manquants :** Tentatives initiales avec `which ffprobe exiftool` qui ont retourné des résultats vides.
- **Chiffrement simple :** Le ROT13 appliqué sur le texte décodé n'a rien donné de cohérent.
- **XOR statique :** La clé XOR déduite uniquement du préfixe (`[06, 00, 0F, 07]`) a produit un résultat partiellement lisible (`csaw}...`) mais corrompu sur le reste de la chaîne.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichier :** `finderskeepers.mp4` (1.6 Mo).
- **Indice principal :** Base64 `ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30=` extrait des métadonnées.
- **Texte intermédiaire :** `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- **Hypothèse :** Le format attendu est `csaw{...}`. La transformation semble être un XOR avec une clé répétitive, mais la clé exacte ou l'alignement est encore incertain.

## Prochaines pistes
- **Affiner le XOR :** Tester la clé `[06, 00, 0F, 07]` en boucle complète sur toute la chaîne décodée pour voir si le reste devient lisible.
- **Chercher la clé :** Essayer des clés basées sur le nom du challenge (`finderskeepers`) ou le format attendu (`csaw`).
- **Vérifier l'alignement :** S'assurer que le caractère `{` correspond bien au début de la clé XOR (peut-être un décalage d'index).
- **Exploration MP4 :** Si le XOR échoue, inspecter les trames vidéo ou les autres boîtes atomiques du MP4 pour trouver la clé manquante.
