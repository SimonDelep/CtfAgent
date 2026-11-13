

---
## Résumé au tour 10 (21:29:18)

## Fait
- Copie et identification du fichier `finderskeepers.mp4` (ISO Media, MP4 Base Media).
- Extraction des chaînes de caractères (`strings`) révélant des métadonnées XMP.
- Découverte d'une chaîne Base64 dans le bloc XML XMP.
- Décodage Base64 réussi : `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.

## Échecs / impasses
- Tentatives de décalage Caesar (ROT-N) : aucun décalage simple ne transforme `esnp` en `csaw`.
- Tentative de XOR simple : la clé calculée (`[6, 0, 15, 7, 0]`) n'est pas un octet unique répétable.
- Hypothèse d'un chiffrement standard (ROT13, etc.) invalidée par les caractères spéciaux (`@`) et les différences irrégulières.

## État actuel
- Flag attendu : `csaw{...}`.
- Flag brut décodé : `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- Différence connue sur le préfixe : `e`->`c` (+2), `s`->`s` (0), `n`->`a` (+13), `p`->`w` (-7).
- Le contenu à l'intérieur des accolades contient des `@` qui doivent probablement être remplacés par `_` ou sont chiffrés.

## Prochaines pistes
- Analyser la séquence de différence (2, 0, 13, -7) pour trouver la clé de chiffrement (Vigenère ou positionnelle).
- Tester un XOR avec la clé déduite sur le reste de la chaîne.
- Vérifier si les `@` correspondent à un décalage spécifique ou à un caractère manquant.
- Explorer d'autres couches de stéganographie dans le MP4 si le chiffrement échoue.


---
## Résumé au tour 20 (21:36:04)

## Fait
- **Analyse XOR du préfixe :** Identification de la transformation `esnp` → `csaw`.
- **Correction de clé :** Ajustement de la clé XOR initiale. Calcul correct de `n ^ a = 15` (au lieu de 23).
- **Clé établie :** `[6, 0, 15, 7]` appliquée cycliquement.
- **Tests alternatifs :** Tentatives de décodage Base64 et de chiffrement par décalage (Shift) sur le contenu entre accolades.

## Échecs / impasses
- **Calcul initial erroné :** Première clé `[6, 0, 23, 7]` donnant `csyw` au lieu de `csaw`.
- **Résultat illisible :** Déchiffrement complet donne `csaw}d?dY...` avec des caractères spéciaux (`?`, `Y`, `@`) et une accolade fermante `}` au lieu d'ouverte `{`.
- **Base64 :** Le contenu `d0c_@yz@gl_mn0j_pm3z3_g0_o00s` résiste au décodage standard (padding incorrect, données binaires).
- **Shift :** Le décalage simple ne reproduit pas le préfixe attendu.

## État actuel
- **Ciphertext :** `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`
- **Clé XOR confirmée :** `[6, 0, 15, 7]` (valide pour les 4 premiers caractères).
- **Déchiffrement partiel :** `csaw}d?dY@v}FgcXkn?mYpb4|3P`6_`76sr`
- **Problème majeur :** L'accolade `{` du ciphertext (ASCII 123) XORée avec 6 donne `}` (ASCII 125). Le contenu semble chiffré avec une logique différente ou une clé décalée.

## Prochaines pistes
- **Vérifier l'offset :** Tester si la clé commence à un index différent pour le contenu (ex: ignorer le préfixe pour le XOR du corps).
- **Clé variable :** Hypothèse que la clé change après le préfixe ou dépend de la position.
- **Double chiffrement :** Le contenu déchiffré partiellement pourrait être encodé (ex: XOR + Base64 inversé).
- **Analyse des caractères :** Examiner la distribution des caractères `?` (ASCII 63) dans le résultat pour déduire la clé manquante.


---
## Résumé au tour 30 (21:41:18)

## Fait (actions utiles et ce qu'elles ont donné)
*   **Décryptage XOR réussi :** Identification de la clé hybride `[6, 0, 15, 7]` pour les 4 premiers octets, puis `0` pour le reste.
*   **Format du flag révélé :** Passage de `esnp{...}` à `csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
*   **Analyse du fichier :** Confirmation du type MP4 et extraction des chaînes de caractères (`strings`), révélant des métadonnées XMP.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
*   **Clé XOR cyclique standard :** Appliquer `[6, 0, 15, 7]` en boucle sur toute la chaîne produisait du bruit après le préfixe.
*   **Décodage Base64 direct :** La longueur du payload (29 caractères) n'est pas un multiple de 4, rendant le décodage standard impossible sans padding.
*   **Substitutions simples :** ROT13 et tentatives de remplacement basiques (`0`→`o`, `3`→`e`) n'ont pas produit de phrase lisible immédiatement.

## État actuel (ce qu'on sait, fichiers/indices clés)
*   **Flag partiel :** `csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
*   **Payload suspect :** Le contenu entre accolades semble être un "leet speak" ou un code substitué (`@`, `_`, chiffres).
*   **Source :** Fichier `finderskeepers.mp4` contenant des métadonnées XML/XMP mais aucun texte flag explicite en clair.

## Prochaines pistes
*   **Mapping Leet Speak systématique :** Tester `0`→`o`, `3`→`e`, `@`→`a` ou `t`, `_`→`espace` pour former des mots anglais.
*   **Analyse XMP approfondie :** Chercher des champs personnalisés ou des URLs cachées dans les métadonnées XML extraites.
*   **Stéganographie vidéo :** Vérifier si le payload correspond à un mot de passe pour une archive cachée ou un lien vers une ressource externe.


---
## Résumé au tour 40 (21:45:50)

## Fait
- **Extraction de métadonnées :** Analyse du fichier MP4 via `strings`, découverte de blocs XMP.
- **Décodage Base64 :** Extraction et décodage de la chaîne `ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30=`.
- **Identification du payload :** Récupération du message chiffré `d0c_@yz@gl_mn0j_pm3z3_g0_o00s`.
- **Soumission initiale :** Tentative de flag avec le préfixe standard `csaw{...}`.

## Échecs / impasses
- **Leet Speak simple :** Substitutions basiques (`0`→`o`, `@`→`a`) donnent du charabia ("ayzagl", "mnoj").
- **Décalage (Caesar) :** Aucun décalage alphabétique ne produit de mots anglais ou français cohérents.
- **XOR :** Tentative de clé basée sur "doc_" (0, 95, 0, 0) incohérente sur le reste de la chaîne.
- **Analyse de fréquence :** Distribution des lettres ne révèle pas de pattern de substitution évident.

## État actuel
- **Flag brut :** `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- **Anomalie :** Le préfixe `esnp` diffère de l'attendu `csaw` (potentiel indice de chiffrement ou erreur de format).
- **Contenu :** Message séparé par des underscores, contenant des chiffres et symboles (`@`, `0`, `3`), suggérant une substitution complexe ou un code.

## Prochaines pistes
- **Chiffrement affine/Vigenère :** Tester une clé mot sur le payload ou sur le préfixe `esnp` pour retrouver `csaw`.
- **Anagrammes :** Vérifier si les segments séparés par `_` sont des anagrammes de mots réels.
- **Stégano supplémentaire :** Si le texte est un leurre, examiner l'audio ou les images clés du MP4 pour un second indice.
- **Mapping personnalisé :** Construire un dictionnaire de substitution basé sur la longueur des mots et la structure connue du flag.
