

---
## Résumé au tour 10 (09:47:34)

## Fait (actions utiles et ce qu'elles ont donné)
*   **Copie et identification :** Fichier `audio.wav` récupéré et identifié comme WAV PCM 16-bit stéréo (34s, 44100 Hz).
*   **Extraction brute :** Conversion réussie des données audio en échantillons numériques via `struct` (contournement de l'absence de `numpy`).
*   **Analyse des valeurs :** Détection de valeurs correspondant à des caractères ASCII imprimables au sein des amplitudes (notamment `c`, `s`, `a`, `w`, `{`).
*   **Vérification stéganographique :** Test de l'extraction LSB (Least Significant Bit) effectué, bien que le résultat soit bruité.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
*   **Dépendances :** Tentative d'import `numpy` échouée (`ModuleNotFoundError`), a nécessité une réécriture en `struct`.
*   **LSB classique :** L'extraction des bits de poids faible n'a pas produit de texte lisible (résultat illisible/non-ASCII).
*   **Mapping direct séquentiel :** La conversion simple de chaque échantillon en caractère donne du bruit ; le message n'est pas linéaire.
*   **Recherche aveugle :** Chercher les lettres "csaw" dans les valeurs absolues sans logique de positionnement génère trop de faux positifs.

## État actuel (ce qu'on sait, fichiers/indices clés)
*   **Fichier :** `audio.wav` (6 Mo) disponible dans le dossier de travail.
*   **Indices textuels :** Les caractères constitutifs du flag (`c`, `s`, `a`, `w`, `{`) sont présents dans les valeurs d'échantillons, mais dispersés.
*   **Structure audio :** Deux canaux distincts avec une forte différence de contenu (1.4M de diffs sur 1.5M d'échantillons).
*   **Indice sémantique :** "listen... glisten" suggère une approche visuelle (spectrogramme) ou un jeu de mots sur la lumière/brillance.

## Prochaines pistes
*   **Spectrogramme :** Générer un sonogramme (via `sox` ou `audacity`) pour voir si le texte apparaît visuellement ("glisten").
*   **Différence de canaux :** Soustraire le canal droit du canal gauche pour isoler le message caché.
*   **Pattern d'échantillonnage :** Tester un "stride" (ex: prendre 1 échantillon sur N) pour reconstruire le texte ASCII à partir des valeurs détectées.
*   **Stéganographie audio :** Vérifier si les valeurs sont encodées en base64 ou XORées avec une clé simple.


---
## Résumé au tour 20 (09:51:42)

## Fait (actions utiles et ce qu'elles ont donné)
- **Analyse du fichier :** Confirmé WAV stéréo (44100 Hz, 16-bit, 2 canaux, ~1.5M frames).
- **Comparaison des canaux :** Le canal gauche est fort, le canal droit est quasi-silencieux (valeurs proches de 0), mais présente des variations subtiles.
- **Détection de pics :** Identification de 27 520 pics (>10000) dans le canal gauche et 1724 dans le droit.
- **Extraction brute :** Tentatives de lecture LSB, signes et valeurs absolues en ASCII (résultats bruités).

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Dépendances manquantes :** `matplotlib` et `sox` absents, bloquant la génération de spectrogrammes.
- **Stéganographie classique :** LSB sur les deux canaux et conversion directe en ASCII ont donné du bruit.
- **Analyse des signes :** La séquence positive/négative ne forme pas de binaire lisible.
- **Hypothèse "Canal Droit seul" :** Bien que faible, le canal droit contient encore trop de bruit pour être lu directement sans traitement.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichier :** `audio.wav`.
- **Indice clé :** "listen... glisten" suggère une approche visuelle (spectrogramme) ou un jeu de mots sur la brillance (peut-être les pics).
- **Observation majeure :** La différence entre les canaux ou le canal droit isolé semble porter l'information, mais le signal est noyé.
- **Données critiques :** Positions des pics (ex: 160822) et valeurs des écarts significatifs entre canaux.

## Prochaines pistes
- **Installation :** Installer `matplotlib` ou `scipy` pour visualiser le spectre (répondre au "glisten").
- **Isolation :** Extraire uniquement le canal droit (`stereo2mono` ou script Python) et l'amplifier.
- **Différence :** Calculer `Left - Right` pour isoler le signal caché si c'est une technique de masquage.
- **Spectrogramme :** Générer une image du spectre pour chercher des motifs visuels (lettres cachées).


---
## Résumé au tour 30 (09:56:26)

## Fait (actions utiles et ce qu'elles ont donné)
- **Environnement :** Installation réussie de `Pillow` avec le flag `--break-system-packages` pour contourner la gestion externe.
- **Analyse audio :** Extraction des métadonnées (stéréo, 44100Hz, ~1.5M d'échantillons) et lecture des données brutes des deux canaux.
- **Visualisation :** Génération d'un fichier `spectrogram.png` (11843x128) basé sur les données audio.
- **Extraction de données :** Identification de plages de valeurs ASCII complètes dans le canal droit et de fragments de texte lisibles dans le canal gauche.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Bibliothèques scientifiques :** Tentative d'installation de `scipy`/`matplotlib` (échec d'import dans le script Python malgré l'installation shell).
- **LSB :** Extraction du bit le moins significatif (LSB) sur les échantillons bruts (résultat : bruit incohérent).
- **Visualisation brute :** Lecture directe du spectrogramme généré (image trop large pour être lisible sans redimensionnement).
- **Import direct :** Utilisation de `numpy` sans vérification préalable de l'environnement d'exécution.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichiers :** `audio.wav` (source), `spectrogram.png` (généré).
- **Indices :** Indice "listen... glisten" confirmé comme piste visuelle.
- **Données :** Le canal gauche contient des séquences partiellement lisibles (ex: `vYM)! ...`). Le canal droit contient une large plage de valeurs ASCII (32 à 122+).
- **Hypothèse :** Le message est soit dans le spectre visuel (à zoomer), soit caché dans les données textuelles brutes des canaux.

## Prochaines pistes
- **Traitement d'image :** Redimensionner ou zoomer sur `spectrogram.png` pour révéler d'éventuels motifs ou lettres.
- **Extraction texte :** Tenter de convertir les valeurs ASCII du canal droit en chaîne de caractères brute.
- **Analyse canal gauche :** Isoler et nettoyer les fragments de texte trouvés dans le canal gauche.
- **Différence de canaux :** Vérifier si la soustraction ou la différence entre les canaux gauche et droit révèle un signal caché.


---
## Résumé au tour 40 (10:04:55)

## Fait (actions utiles et ce qu'elles ont donné)
- **Extraction audio :** Séparation des canaux gauche et droit du fichier `audio.wav`.
- **Analyse canal gauche :** Identification de séquences contenant des mots anglais lisibles ('the', 'are', 'had') mélangés à des symboles.
- **Traitement image :** Conversion du spectrogramme en binaire (`spectrogram_binary.png`) pour isoler les pixels non-noirs (0.84% du total).
- **Visualisation :** Redimensionnement de l'image pour repérer les zones denses (lignes 13, 27, 28, etc.).

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Redimensionnement agressif :** Passer la hauteur à 10 pixels a rendu le contenu illisible.
- **Canal droit :** Les valeurs brutes ne correspondent pas directement à la plage ASCII standard.
- **Traitement image lourd :** Conversion complète en niveaux de gris a causé un timeout ; il faut cibler les zones denses.
- **Recherche directe :** Chercher 'flag' ou 'csaw' dans le canal droit n'a rien donné.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichiers clés :** `audio.wav` (source), `spectrogram_binary.png` (version épurée).
- **Indice audio :** Le canal gauche contient un message partiellement déchiffrable avec des mots courants, suggérant un chiffrement simple (décalage, substitution).
- **Indice image :** Le spectrogramme est majoritairement noir, le message doit être caché dans les rares pixels clairs ou les lignes denses.
- **Hypothèse :** Le flag est probablement dans le canal gauche (à décoder) ou visible dans le spectrogramme binaire.

## Prochaines pistes
1. **Déchiffrage audio :** Tester des décalages (Caesar) ou du XOR sur le canal gauche en utilisant les mots connus ('the', 'are') comme clé.
2. **Visualisation ciblée :** Afficher uniquement les lignes denses du spectrogramme binaire pour lire un texte éventuel.
3. **Corrélation :** Vérifier si les séquences audio longues correspondent aux lignes denses du spectrogramme.
4. **Stéganographie :** Vérifier si les valeurs des pixels non-noirs contiennent des données encodées (LSB, etc.).
