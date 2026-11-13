

---
## Résumé au tour 10 (06:11:50)

## Fait
- **Analyse du fichier :** Copie et vérification du format (WAV PCM 16-bit stéréo).
- **Extraction brute :** Parsing Python du chunk `data` pour isoler les échantillons audio.
- **Première tentative de stégano :** Extraction des LSB (bits de poids faible) → Résultat : bruit incohérent.
- **Analyse des amplitudes :** Conversion directe des valeurs d'échantillons en ASCII → Découverte d'une séquence de 88k+ caractères contenant un `{` à l'index 246.

## Échecs / impasses
- **LSB classique :** Les bits de poids faible ne contiennent pas le message flag.
- **Interprétation directe :** Traiter *tous* les échantillons comme du texte génère trop de bruit (caractères non imprimables mélangés).
- **Début du flux :** Le message ne semble pas commencer au tout premier échantillon (beaucoup de zéros au début).
- **Ignorance du titre :** Le nom `12345678` n'a pas encore été utilisé comme clé ou offset.

## État actuel
- **Fichier cible :** `audio.wav` (6 Mo, ~1.5M d'échantillons).
- **Données clés :** Une chaîne de caractères extraite des valeurs d'amplitude contient des fragments ASCII lisibles.
- **Indice majeur :** Présence d'un caractère `{` dans le flux extrait, suggérant un format de flag (`csaw{...}`).
- **Problème :** Le contexte autour du `{` est encore mélangé à du bruit (`955)%.:M_q{sbUK...`).

## Prochaines pistes
- **Filtrage intelligent :** Isoler uniquement les séquences de valeurs d'échantillons formant des chaînes ASCII valides autour du `{`.
- **Utiliser le titre :** Tester le nom `12345678` comme offset de départ ou comme clé de sélection (ex: prendre chaque 12e, 3e, 4e... échantillon).
- **Recherche de délimiteurs :** Chercher le caractère `}` dans le flux extrait pour délimiter le flag.
- **Analyse fréquentielle :** Vérifier si certaines valeurs d'amplitude spécifiques (ex: > 100) contiennent le message pur.


---
## Résumé au tour 20 (06:19:26)

## Fait
- **Préparation :** Renommage du fichier `12345678 (1).wav` en `audio.wav` pour éviter les erreurs de chemin.
- **Analyse technique :** Extraction des métadonnées (stéréo, 44100 Hz, 34s) et inspection des valeurs d'échantillons (distribution majoritairement faible, pics à ±32767).
- **Débruitage :** Séparation des canaux gauche et droit ; le canal gauche atteint la dynamique complète, le droit est plus limité.
- **Tests de décodage :** Tentatives de conversion ASCII brute et recherche de sous-chaînes (`{`) avec des offsets dérivés du titre (78, 114).

## Échecs / impasses
- **Gestion de chemin :** Échec initial dû aux espaces dans le nom du fichier original.
- **Brute-force offset :** Recherche directe de `csaw{` avec des offsets simples (0, 78, 246) a donné des fragments (`{`, `c{`) noyés dans du bruit, sans flag complet.
- **Syntaxe Python :** Petite erreur de string literal lors d'un test de recherche.
- **Conversion brute :** Les échantillons ne correspondent pas directement à du texte ASCII lisible sans traitement supplémentaire.

## État actuel
- **Fichier cible :** `audio.wav` (stéréo, 6MB).
- **Indices clés :** Titre "12345678" (probable clé/offset), indice texte "glisten" (suggère une approche visuelle ou de gain).
- **Données brutes :** Présence sporadique de caractères lisibles (`{`, `c`) mais pas de séquence cohérente. Différence de dynamique notable entre les deux canaux audio.

## Prochaines pistes
- **Spectrogramme :** Générer un spectrogramme pour visualiser d'éventuels motifs cachés (suggéré par "glisten").
- **LSB Audio :** Extraire les bits de poids faible (LSB) des échantillons pour voir si le message y est encodé.
- **Amplification :** Appliquer un gain fort sur les canaux pour révéler un signal faible noyé dans le silence.
- **Clé "12345678" :** Tester ce chiffre comme mot de passe pour un outil de stéganographie audio (ex: `steghide` ou XOR) ou comme séquence d'indices pour reconstruire le message.


---
## Résumé au tour 30 (06:23:45)

## Fait
- Analyse complète des métadonnées WAV (stéréo, 16-bit, 44100Hz, 34s).
- Extraction des LSB (1 bit) des canaux gauche et droit.
- Calcul de la différence entre canaux et extraction de ses LSB.
- Extraction des 8 bits de poids faible (lower byte) des échantillons.
- Détection de caractères `{` dispersés dans les flux LSB, mais pas de flag lisible.

## Échecs / impasses
- **LSB classique (1 bit) :** Trop de bruit, pas de séquence cohérente.
- **Visualisation :** Échec dû aux dépendances manquantes (`numpy`, `matplotlib`, `sox`).
- **Code :** Dernier script Python planté (`NameError: samples not defined`).
- **Recherche directe :** `csaw{` absent dans les flux bruts extraits.

## État actuel
- **Fichier cible :** `audio.wav` (6MB) disponible.
- **Indices identifiés :** "glisten" (suggère spectrogramme/visuel), "12345678" (suggère clé XOR ou offset).
- **Observation :** Canal droit plus "vide" en 8 LSBs que le gauche.
- **Format attendu :** `csaw{...}`.

## Prochaines pistes
1. **Environnement :** Installer `sox` ou `python3-numpy`/`matplotlib` pour générer un spectrogramme.
2. **Crypto :** Tester un XOR des échantillons avec la clé "12345678" (ou ses octets).
3. **Correction :** Réécrire le script Python pour éviter le `NameError` et réanalyser les données.
4. **Visuel :** Si spectrogramme possible, chercher des motifs cachés dans les hautes fréquences.
