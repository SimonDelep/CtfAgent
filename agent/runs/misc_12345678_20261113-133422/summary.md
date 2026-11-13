

---
## Résumé au tour 10 (13:37:31)

## Fait (actions utiles et ce qu'elles ont donné)
- **Analyse structurelle :** Identification du fichier comme WAV PCM 16-bit stéréo (44100 Hz, ~34s).
- **Extraction de données :** Parsing Python des échantillons audio pour isoler les valeurs numériques.
- **Tentatives de stéganographie :** Extraction des bits de poids faible (LSB) sur les canaux gauche/droit et filtrage des valeurs non nulles (1-127).
- **Vérification initiale :** Commandes `strings` et `xxd` pour repérer des en-têtes ou chaînes lisibles.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Recherche de chaînes (`strings`) :** Résultat trop bruité, aucune séquence flag évidente (`CSAW{...}`).
- **Mapping ASCII direct :** Convertir les valeurs d'échantillons directement en caractères donne du texte illisible (caractères de contrôle + bruit).
- **LSB simple :** L'extraction brute des LSB sur les canaux ne produit pas de message exploitable immédiatement.
- **Hypothèse "silence" :** Le début du fichier est presque silencieux, mais le message ne semble pas être uniquement dans les silences.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichier cible :** `audio.wav` dans le dossier de travail.
- **Données extraites :** Une séquence longue de 2,3M de caractères issue des valeurs d'échantillons non nulles (contient des caractères binaires et imprimables).
- **Indice clé :** "listen... when you find the answer it will glisten" suggère une analyse visuelle ou un jeu de mots sur la brillance (spectrogramme).
- **Problème :** Le message extrait est cryptique, probablement encodé (bytes bruts) ou nécessitant une visualisation.

## Prochaines pistes
- **Spectrogramme :** Générer un spectrogramme (Audacity, `stegsolve`, ou Python `matplotlib`) pour chercher des motifs visuels ("glisten").
- **Décodage des données brutes :** Traiter la séquence de valeurs non nulles comme un flux de bytes (`bytes()`) plutôt que des caractères, puis tester Base64, Hex ou XOR.
- **Écoute attentive :** Écouter le fichier pour détecter des signaux DTMF ou une voix cachée.
- **Analyse des bits de poids fort :** Vérifier si les bits significatifs des échantillons contiennent le message (au-delà du LSB).


---
## Résumé au tour 20 (13:40:57)

## Fait
- Identification du fichier `audio.wav` (WAV PCM 16-bit stéréo 44100 Hz, ~6 Mo).
- Extraction des métadonnées techniques via script Python (taille, nombre d'échantillons).
- Extraction brute des bits LSB (379k bytes récupérés).
- Commande `strings` exécutée sur le fichier binaire.
- Création de l'outil `wav_analyzer` disponible pour les tours suivants.

## Échecs / impasses
- Import `numpy`/`matplotlib` manquant (blocage initial du spectrogramme Python).
- Outils audio externes (`sox`, `ffmpeg`) absents du PATH.
- Analyse LSB directe : données bruitées, pas de flag ASCII lisible immédiatement.
- Outil `wav_analyzer` : exécution silencieuse, sortie non visible dans le log.

## État actuel
- Fichier cible : `audio.wav`.
- Indice "glisten" : oriente vers une visualisation (spectrogramme) ou un jeu de mots sur la brillance (bits).
- Données LSB extraites mais non décodées.
- Strings trouvées : fragments non significatifs (`l o k`, `g&i&`).
- Snippets Python (`_snippet_...`) présents dans le dossier mais non analysés.

## Prochaines pistes
- Vérifier l'installation de `numpy` et régénérer le spectrogramme.
- Analyser la différence entre les canaux gauche/droite (stéréo).
- Examiner le contenu des fichiers `_snippet_...`.
- Tenter un décodage LSB plus avancé (groupes de bits, inversion).
- Si `pip` fonctionne, utiliser `matplotlib` pour visualiser les données brutes.


---
## Résumé au tour 30 (13:43:48)

## Fait (actions utiles et ce qu'elles ont donné)
- **Analyse structurelle** : Identification des métadonnées WAV (2 canaux, 44100 Hz, 16 bits, ~68s).
- **Extraction LSB** : Récupération des bits de poids faible (379k octets), bien que le résultat brut semble être du bruit.
- **Environnement** : Installation réussie de `numpy` et `matplotlib` (via `--break-system-packages`) pour la visualisation.
- **Visualisation** : Génération de spectrogrammes pour les canaux gauche et droit.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **ASCII direct** : Tentative de mapper les échantillons bruts directement en caractères imprimables (32-126) : trop de bruit, message illisible.
- **Installation Python** : `pip install` standard a échoué à cause de l'environnement géré (nécessité du flag `--break-system-packages`).
- **LSB brut** : L'extraction simple des LSB sans décodage supplémentaire (Base64, Hex, etc.) ne donne pas de texte clair immédiatement.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Cible** : `audio.wav` (6 Mo).
- **Indices** : Présence de 8 scripts `_snippet_*.py` suggérant diverses méthodes (LSB, séparation canaux, valeurs absolues).
- **Données** : Spectrogrammes générés (fichiers images créés mais non inspectés visuellement dans le log).
- **Données brutes** : LSB extraites disponibles mais non interprétées sémantiquement.

## Prochaines pistes
- **Inspection visuelle** : Ouvrir les images de spectrogrammes générées pour y chercher des motifs ou du texte caché.
- **Séparation des canaux** : Comparer le canal gauche et droit (différence de phase ou contenu distinct).
- **Décodage LSB** : Appliquer des encodages (Base64, Hex, ROT) sur les 379k octets de LSB extraits.
- **Analyse des snippets** : Revoir les snippets non exécutés pour voir s'ils contiennent une logique de décodage spécifique (modulo, valeurs absolues).


---
## Résumé au tour 40 (13:47:07)

## Fait (actions utiles et ce qu'elles ont donné)
- **Analyse structurelle :** Identification de `audio.wav` (stéréo, ~1.5M d'échantillons/canal) et lecture des snippets de référence.
- **Extraction de données :** Parsing des samples avec `struct` (contournement de l'absence de `numpy`).
- **Tests LSB :** Extraction des bits de poids faible sur les canaux Gauche, Droit et leur différence.
- **Test Modulo :** Application `sample % 128` sur le canal gauche, révélant quelques séquences imprimables (ex: `%%..<>LKXTVPIB3/...`), bien que non cohérentes.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **LSB brut :** Conversion directe des LSB en bytes ou Base64 (résultat : bruit binaire, pas de préfixe `csaw{`).
- **ASCII direct :** Tentative de mapper les valeurs d'échantillons directement en ASCII (plage 32-126), majoritairement du bruit.
- **Dépendances :** Tentative initiale d'importer `numpy` sans vérification préalable de l'environnement.
- **Approche purement textuelle :** Chercher le message uniquement dans les données binaires brutes sans considérer la dimension visuelle suggérée par le titre.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichiers :** `audio.wav` (cible principale), dossier/fichier `spec` (spectrogrammes potentiels), multiples `_snippet_*.py` (guides techniques).
- **Indices :** Titre "SEUL" (Single ? Mono ? Unique ?), indice "glisten" (briller -> visuel/spectrogramme).
- **Données :** Les canaux sont séparables. Le canal gauche contient des séquences partiellement imprimables via modulo, mais pas de flag clair.
- **Hypothèse :** Le message est probablement visuel (spectrogramme) ou nécessite une opération spécifique sur les canaux (XOR, différence).

## Prochaines pistes
- **Investigation visuelle :** Examiner le contenu du fichier/dossier `spec` pour y chercher du texte ou des motifs cachés.
- **Opérations sur canaux :** Tester le XOR entre les canaux Gauche et Droit (`left ^ right`) pour annuler le bruit commun.
- **Mono/SEUL :** Convertir en mono ou isoler un canal spécifique si "SEUL" implique une réduction de complexité.
- **Spectrogramme :** Générer un spectrogramme propre (si `spec` est vide) pour chercher des formes ou du texte caché dans les hautes fréquences.
