

---
## Résumé au tour 10 (00:25:27)

## Fait
- **Analyse du fichier :** Copie de `12345678 (1).wav` vers le dossier de travail. Vérification des métadonnées (WAV, PCM 16-bit, stéréo, 44100 Hz, ~34s).
- **Extraction de données :** Lecture des samples bruts en Python (3 032 104 samples).
- **Tentatives de stégano :** Extraction des bits LSB (Least Significant Bit) sur le fichier entier et séparément sur les canaux gauche/droit.
- **Recherche de texte :** Utilisation de `strings` et `grep` pour chercher des motifs standards (`csaw`, `{`).

## Échecs / impasses
- **Décodage LSB direct :** La conversion des bits LSB en texte ASCII a produit du "bruit" illisible (caractères non imprimables).
- **Dépendance manquante :** Tentative d'analyse spectrale avec `numpy` échouée (`ModuleNotFoundError`).
- **Recherche naïve :** `strings` a révélé beaucoup de `{` et `&` mais aucun flag formaté clair (`csaw{...}`).
- **Hypothèse stéréo :** Séparer les canaux n'a pas immédiatement révélé de message caché.

## État actuel
- **Fichier cible :** `audio.wav` (6 Mo) disponible localement.
- **Données connues :** Plage de valeurs des samples (-32768 à 32767), présence de motifs répétitifs dans les strings.
- **Indices non exploités :** Le nom du fichier "12345678" (série numérique) n'a pas encore été utilisé comme clé ou indice de fréquence.
- **Environnement :** Python standard fonctionnel, mais bibliothèque scientifique absente.

## Prochaines pistes
- **Analyse fréquentielle :** Installer `numpy` ou utiliser `scipy` pour générer un spectrogramme (stégano dans le spectre).
- **LSB avancé :** Tester des décalages (offsets) sur les bits LSB ou chercher un mot-clé pour XOR.
- **Exploitation du titre :** Vérifier si "12345678" correspond à une fréquence spécifique à isoler ou une séquence de valeurs dans les samples.
- **Outils externes :** Utiliser `audacity` ou `Sonic Visualiser` (si disponible) pour visualiser le son manuellement.


---
## Résumé au tour 20 (00:30:47)

## Fait (actions utiles et ce qu'elles ont donné)
- Analyse technique du fichier WAV (stéréo, 16-bit, 44100Hz).
- Extraction des bits LSB des canaux gauche, droit et combinés.
- Recherche de chaînes imprimables et de motifs dans les données brutes.
- **Découverte clé :** Un caractère `{` détecté à l'index 1121 dans le flux LSB combiné.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- LSB brut sans traitement (donne majoritairement du bruit).
- XOR global avec "12345678" sur l'intégralité du fichier (reste illisible).
- Recherche de métadonnées textuelles dans l'en-tête WAV (standard, pas de flag).
- Séparation stricte des canaux sans combinaison (moins efficace que le flux global).

## État actuel (ce qu'on sait, fichiers/indices clés)
- Fichier cible : `audio.wav`.
- Indice principal : Le titre "12345678" est très probablement la clé XOR ou l'offset.
- Point d'ancrage : Le début du flag se situe probablement à l'index 1121 (dans les données LSB).
- Format attendu : `...{...}` (début de flag standard).

## Prochaines pistes
- Appliquer le XOR avec "12345678" spécifiquement autour de l'index 1121.
- Vérifier si 1121 est un offset binaire ou décimal (ou lié à la fréquence).
- Tester l'extraction des 8 bits LSB (byte extraction) au lieu du seul 1er bit.
- Vérifier l'interleaving (Gauche/Droite) spécifiquement autour de cet index critique.
