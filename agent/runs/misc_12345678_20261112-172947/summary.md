

---
## Résumé au tour 10 (17:33:04)

## Fait
- Copie du fichier `12345678 (1).wav` dans le workspace.
- Vérification du format : WAV PCM 16-bit stéréo 44100 Hz (~6 Mo).
- Analyse Python : extraction des métadonnées et tentatives de décodage LSB (par byte, par échantillon, canal gauche).
- Détection de séquences de zéros (silence) de longueurs spécifiques (11, 11, 11, 15 échantillons).

## Échecs / impasses
- **LSB classique :** Les bits de poids faible des bytes et des échantillons ne forment pas de texte ASCII lisible.
- **Recherche de texte brut :** Conversion directe des données en chaîne imprimable ne donne que des points (silence).
- **Insistance sur LSB :** Trop de temps passé sur la stéganographie LSB sans vérifier le contenu audible ou spectral.

## État actuel
- Fichier `audio.wav` prêt pour analyse.
- Indice "listen" non exploité (pas d'écoute réelle ou de spectrogramme).
- Données brutes contiennent des motifs de silence (zéros) potentiels.
- Pas de flag trouvé, mais piste Morse sur les séquences de zéros identifiée.

## Prochaines pistes
- **Spectrogramme :** Visualiser le fichier (ex: `Sonic Visualiser` ou script Python `matplotlib`) pour voir des motifs cachés.
- **Écoute :** Vérifier s'il y a un son audible (vitesse normale ou ralentie).
- **Morse :** Tester si les séquences de zéros (11, 11, 11, 15) correspondent à des points/trains de Morse.
- **Autres outils :** `stegsolve` ou `audacity` pour analyse approfondie.


---
## Résumé au tour 20 (17:38:52)

## Fait (actions utiles et ce qu'elles ont donné)
- **Analyse du fichier :** Récupération des métadonnées WAV (stéréo, 44100 Hz, 34s) et extraction des échantillons bruts via `struct`.
- **Détection de silences :** Identification de séquences de zéros (gaps) dans les données audio. Le canal droit en contient beaucoup plus (1031 séquences) que le gauche (407).
- **Statistiques des longueurs :** Les longueurs des silences varient entre 6 et 15+ échantillons.
- **Tentative de décodage :** Conversion des longueurs en binaire (pair/impair) et en Morse (seuils variables). Une tentative de mapping Morse a produit un début de texte lisible ("B").

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Dépendances :** Tentative d'import `numpy` (échec : `ModuleNotFoundError`), résolu en passant en Python pur.
- **Stéganographie LSB :** Extraction des bits de poids faible sur les canaux gauche/droit a donné du "bruit" ASCII (ex: `? ? ? ? O ? ? q`).
- **Mapping binaire simple :** Convertir les longueurs en 0/1 via parité ou seuil fixe n'a pas produit de texte clair.
- **Analyse des deux canaux :** Traiter les deux canaux ensemble dilue le signal ; le canal droit semble être le porteur principal.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichier cible :** `audio.wav`.
- **Indice clé :** "listen" (suggère un contenu audible ou des silences significatifs).
- **Données critiques :** Séquences de zéros de longueurs spécifiques (6, 7, 8, 9, 10, 11, 15...) dans le canal droit.
- **Hypothèse dominante :** Encodage Morse où la durée du silence (nombre d'échantillons) représente des points et des traits.
- **Résultat partiel :** Début de décodage Morse suggère la lettre "B" ou des structures similaires.

## Prochaines pistes
- **Affiner le Morse :** Déterminer le seuil exact séparant "point" (court) et "trait" (long) (ex: 6-7 vs 8+).
- **Gestion des séparations :** Identifier si certaines longueurs de silence (ex: 15) servent de séparateurs entre lettres ou mots.
- **Vérification audio :** Écouter le fichier ou générer un spectrogramme pour confirmer la présence de Morse audible.
- **Focus Canal Droit :** Isoler et décoder uniquement le canal droit, car il contient la majorité des séquences de zéros.


---
## Résumé au tour 30 (17:43:16)

## Fait
- **Correction du fichier cible** : Identification du vrai fichier `audio.wav` après erreur `FileNotFoundError` sur le nom avec espace.
- **Analyse binaire** : Confirmation du format WAV (16-bit, 44100Hz, Stéréo) et extraction des données audio brutes.
- **Extraction des silences** : Identification des séquences de zéros (silences) dans le canal droit, beaucoup plus riches en données que le gauche.
- **Premier décodage** : Conversion des longueurs de silences en séquences de points et de traits Morse.

## Échecs / impasses
- **Nom de fichier** : Tentative initiale sur `12345678 (1).wav` (inexistant dans le dossier de travail).
- **Canal gauche** : Analyse initiale des deux canaux ; le gauche s'est avéré peu pertinent (trop de séquences de longueur 1).
- **Seuils de décodage** : Tentatives de seuils arbitraires (>=7, >=4) pour séparer les lettres sans succès immédiat de lecture.
- **Bruit de fond** : Inclusion des séquences de longueur 1 dans le décodage initial, créant un Morse illisible.

## État actuel
- **Fichier** : `audio.wav` (6 Mo).
- **Indice clé** : Le canal droit encode l'information via la durée des silences.
- **Données brutes** : Séquences de silences de longueurs 2 à 21 échantillons.
- **Résultat partiel** : Chaîne de Morse brute générée (ex: `-...--.--....-..-...-.-..-.-..-...`), mais non traduite en texte lisible.

## Prochaines pistes
- **Affiner le mapping** : Tester systématiquement les standards Morse (1 unité = point, 3 unités = trait, 7 unités = mot) sur les longueurs observées.
- **Nettoyage** : Filtrer les séquences de longueur 1 (probables séparateurs intra-élément ou bruit).
- **Décodage final** : Passer la chaîne de Morse brute dans un décodeur Morse standard pour obtenir le flag.
- **Vérification** : Si le texte reste incompréhensible, vérifier si le canal gauche contient une clé de chiffrement ou un indice complémentaire.


---
## Résumé au tour 40 (17:48:53)

## Fait
- **Analyse audio :** Confirmation fichier WAV stéréo (44100Hz). Extraction des silences du canal droit.
- **Détection de motifs :** Identification de deux types de valeurs : petites (1-8) et grandes (≥50, séparateurs).
- **Statistiques :** Distribution des valeurs 1-8 (1 très fréquent). Détection de groupes de valeurs identiques (ex: Groupe 1 = Groupe 2).

## Échecs / impasses
- **Morse standard :** Tentative de décodage Morse (1=point, 3=trait) → Résultat illisible ("EEI", "T?").
- **Interprétation brute :** Considérer toutes les longueurs de silence comme du timing Morse sans filtrer les séparateurs longs.
- **Négligence du titre :** Traiter "12345678" comme un titre générique au lieu d'une clé de chiffrement directe.

## État actuel
- **Données clés :** Séquences de silences codées par des entiers 1 à 8, séparées par des silences longs (~100 unités).
- **Structure :** Message divisé en blocs répétitifs. Certains blocs sont identiques, suggérant des mots ou phrases récurrents.
- **Hypothèse forte :** Le titre "12345678" indique que les valeurs 1-8 sont l'alphabet brut (substitution directe).

## Prochaines pistes
- **Substitution simple :** Mapper directement les valeurs 1-8 à des caractères (A-H, ou autre alphabet).
- **Cryptanalyse de fréquence :** Utiliser la répétition des groupes (Groupe 1/2) pour identifier les mots communs (ex: "THE", "ET").
- **Vérification binaire :** Tester si les valeurs 1-8 encodent du binaire (ex: 1=0, 2=1) avant de chercher du texte.
