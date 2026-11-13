

---
## Résumé au tour 10 (00:52:48)

## Fait
- Copie du fichier `finderskeepers.mp4` et identification du format (ISO Media/MP4).
- Extraction des métadonnées XMP via `strings`.
- Décodage Base64 trouvé dans les métadonnées : `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.

## Échecs / impasses
- Tentative de correction du préfixe `esnp` vers `csaw` par XOR : la clé déduite (`06 00 0f 07 00`) ne produit pas de texte lisible sur le reste du flag.
- Recherche directe de la chaîne `csaw{` dans le fichier binaire (`xxd`, `strings`) sans résultat clair.
- Décalages simples (ROT13, Caesar) testés sur la chaîne décodée sans succès.

## État actuel
- On possède la chaîne chiffrée : `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- Le format attendu est `csaw{...}`.
- La transformation est probablement un XOR ou une substitution, mais la clé n'est pas encore confirmée pour l'ensemble du message.

## Prochaines pistes
- Vérifier si la clé XOR est répétitive (ex: `csaw` itéré) sur toute la chaîne.
- Chercher une clé cachée dans les métadonnées XMP ou le nom du fichier.
- Tester des attaques par force brute sur les décalages si le XOR échoue sur le corps du flag.


---
## Résumé au tour 20 (00:57:01)

## Fait
- **Extraction des métadonnées :** Identification et extraction de la chaîne Base64 cachée dans les tags XMP du fichier `finderskeepers.mp4`.
- **Décodage Base64 :** Conversion réussie de `ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30=` en `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- **Analyse cryptographique :** Calcul de la clé XOR déduite du préfixe attendu (`csaw{`), donnant `[6, 0, 15, 7, 0]`.
- **Vérification fichier :** Confirmation que le fichier MP4 est structuré normalement (header `ftypisom`).

## Échecs / impasses
- **XOR répétitif simple :** L'application de la clé `[6, 0, 15, 7, 0]` sur toute la chaîne corrige le préfixe mais rend le reste illisible (caractères non imprimables).
- **Mots-clés standards :** Tentatives infructueuses avec des clés XOR courantes (`csaw`, `flag`, `secret`, `finders`, `keepers`).
- **Décalage simple (Caesar) :** Les décalages de position testés n'ont pas produit de texte lisible.
- **Hypothèse clé fixe :** L'idée que la clé XOR est courte et répétitive semble fausse pour le corps du message.

## État actuel
- **Cible :** Fichier `finderskeepers.mp4`.
- **Donnée chiffrée :** `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- **Format attendu :** `csaw{...}`.
- **Indice clé :** La transformation des 5 premiers caractères est un XOR avec `[6, 0, 15, 7, 0]`.
- **Problème :** La logique de chiffrement change ou la clé évolue après le préfixe.

## Prochaines pistes
- **Clé variable :** Tester si la clé XOR est dérivée d'un mot plus long (ex: `finderskeepers`) ou change selon la position.
- **Autres couches :** Vérifier si le MP4 contient une image ou un autre flux caché (stéganographie visuelle).
- **Analyse de fréquence :** Étudier la distribution des caractères dans la chaîne chiffrée pour identifier un autre type de substitution.
- **Recherche de clé :** Chercher une clé qui transforme `esnp` en `csaw` et qui reste cohérente sur le reste (ex: clé basée sur le nom du challenge).


---
## Résumé au tour 30 (01:01:11)

## Fait
- **Déduction de clé XOR** : Calculé la clé `[6, 0, 15, 7, 0]` par attaque known-plaintext sur le préfixe (`esnp{` → `csaw{`).
- **Décryptage partiel** : Confirmation que le préfixe `csaw{` est correct en appliquant la clé uniquement sur les 5 premiers caractères.
- **Analyse fichier** : Identification du fichier `finderskeepers.mp4` comme ISO Media avec présence de métadonnées XMP (Adobe/Canva).

## Échecs / impasses
- **XOR répétitif** : Appliquer la clé `[6, 0, 15, 7, 0]` sur toute la chaîne a produit des caractères non-imprimables (DEL, contrôle).
- **Clés nominales** : Les tentatives avec les mots "finders", "keepers" ou "finderskeepers" en clé XOR n'ont donné aucun texte lisible.
- **Encodages standards** : ROT13 et Base64 sur le payload `d0c_@yz@gl...` n'ont rien révélé de significatif.
- **Recherche brute** : Pas de chaînes Base64 longues détectées directement dans les `strings` du MP4.

## État actuel
- **Flag partiel** : `csaw{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- **Payload suspect** : Le contenu entre accolades semble être du leetspeak ou une substitution, mais n'est pas immédiatement lisible.
- **Métadonnées** : Le fichier MP4 contient des blocs XML XMP, mais aucune chaîne de flag explicite n'a été extraite pour l'instant.
- **Hypothèse** : Soit le payload est le flag final (déguisé), soit une seconde étape de décryptage est nécessaire (changement de clé ou mode).

## Prochaines pistes
- **Analyse du payload** : Traiter `d0c_@yz@gl_mn0j_pm3z3_g0_o00s` comme une substitution monoalphabétique ou du leetspeak avancé.
- **Extraction XMP** : Parser le XML complet des métadonnées pour y chercher des données cachées ou des commentaires.
- **Stéganographie vidéo** : Utiliser `ffprobe` ou `stegsolve` pour inspecter les trames vidéo ou les flux audio du MP4.
- **Clé dynamique** : Tester si la clé XOR change après le préfixe (ex: clé basée sur la position ou le nom du fichier).


---
## Résumé au tour 40 (01:09:26)

## Fait
- Extraction des métadonnées XMP du fichier `finderskeepers.mp4` via `strings` et script Python.
- Décodage Base64 de la chaîne trouvée : `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- Identification de l'anomalie du préfixe (`esnp` au lieu de `csaw`).
- Tentatives de décodage Leetspeak, ROT13 et Atbash sur le contenu du flag.

## Échecs / impasses
- Leetspeak simple (`0`→`o`, `@`→`a`) donne `doc_ayzagl_mnoj_pmeze_go_ooos` (incompréhensible).
- Application de la clé XOR dérivée du préfixe (`esnp`→`csaw`) sur tout le flag produit des caractères non-imprimables.
- Décalages classiques (ROT, Atbash) ne révèlent aucun mot anglais lisible.

## État actuel
- Flag brut : `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- Hypothèse forte : Transformation de substitution monoalphabétique ou Vigenère basée sur la différence de préfixe.
- Date dans les métadonnées : `2026-09-14` (potentiellement une clé ou indice temporel).
- Outil `substitution_solver` forgé et prêt à être utilisé.

## Prochaines pistes
- Utiliser `substitution_solver` pour casser la substitution du payload `d0c_@yz@gl...`.
- Tester si la différence de caractères entre `esnp` et `csaw` forme une clé Vigenère réutilisable sur le reste.
- Vérifier si `d0c` signifie "doc" et si le reste suit une logique de substitution personnalisée (ex: `@` n'est pas toujours `a`).
