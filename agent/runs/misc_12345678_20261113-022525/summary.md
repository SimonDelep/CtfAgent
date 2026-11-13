

---
## Résumé au tour 10 (02:29:22)

## Fait (actions utiles et ce qu'elles ont donné)
- Copie et vérification du fichier `audio.wav` (WAV PCM 16-bit stéréo, 44100 Hz).
- Analyse hexadécimale et extraction LSB globale (résultat bruité, mais a permis de lire les données brutes).
- Analyse statistique des valeurs d'échantillons : découverte que la majorité des valeurs sont comprises entre -15 et 15.
- Filtrage des valeurs positives comprises entre 1 et 8, générant une séquence numérique longue (`2, 1, 2, 3...`).

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **LSB classique :** Extraire le bit de poids faible de tous les échantillons ne donne pas de texte lisible.
- **Séparation de canal :** Isoler le canal gauche seul sans filtrage de valeur ne révèle pas de message clair.
- **Recherche de chaînes ASCII :** Aucun texte lisible trouvé dans les données brutes (`xxd`) ou via décodage direct.

## État actuel (ce qu'on sait, fichiers/indices clés)
- Fichier `audio.wav` analysé en mémoire.
- Le "son" est en réalité une séquence de nombres entiers très faibles (quasi-silence).
- Une séquence de valeurs positives (1 à 8) a été extraite avec succès (environ 895k valeurs).
- Hypothèse forte : Le titre "12345678" indique que ces 8 valeurs sont la clé de décodage (Base8 ou mapping alphabétique).

## Prochaines pistes
- Convertir la séquence extraite en texte (essayer Base8, ou mapping 1=A, 2=B...).
- Vérifier si les valeurs négatives servent de séparateurs ou d'indices supplémentaires.
- Tester un décodage direct de la séquence numérique vers ASCII.


---
## Résumé au tour 20 (02:37:40)

## Fait (actions utiles et ce qu'elles ont donné)
*   **Extraction des données :** Récupération des échantillons audio (`<h`) et identification de la plage de valeurs strictes : entiers entre -8 et 8 (excluant 0).
*   **Analyse statistique :** Confirmation d'une distribution symétrique et décroissante pour les valeurs positives (1 à 8) et négatives (-1 à -8).
*   **Substitution par fréquence :** Application d'un mapping basé sur la fréquence des lettres anglaises (1=E, 2=T, 3=A...) produisant un texte partiellement lisible (`TETATONANEA...`).
*   **Analyse des transitions :** Comptage des changements de signe (pos->neg, neg->pos) montrant une équilibre quasi parfait.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
*   **Mapping direct (1=A) :** A produit du charabia (`BABCBDF...`), indiquant que la valeur absolue seule ne suffit pas.
*   **Encodage Octal :** Tentative de conversion par groupes de 2 ou 3 valeurs, résultat majoritairement des caractères non imprimables.
*   **Morse simplifié :** Conversion 1-4=point, 5-8=trait a généré une suite massive de "E" (`EEEEETET...`), trop répétitive pour être du texte clair.
*   **Ignorer le signe :** Traiter uniquement les valeurs positives a masqué la moitié de l'information (les valeurs négatives ont la même distribution).

## État actuel (ce qu'on sait, fichiers/indices clés)
*   **Fichier :** `audio.wav` (séquence de ~1.78M de valeurs).
*   **Structure :** Le signal est une séquence de valeurs discrètes dans `[-8, -1] U [1, 8]`.
*   **Indice clé :** La symétrie des distributions suggère que le signe (`+` ou `-`) est un paramètre actif du chiffrement, pas juste du bruit.
*   **Résultat partiel :** Le texte substitué par fréquence contient des structures de mots possibles ("TON", "ANE"), mais n'est pas un flag exploitable tel quel.

## Prochaines pistes
*   **Utiliser le signe :** Combiner valeur absolue et signe pour former un alphabet de 16 symboles (ex: +1 et -1 sont deux lettres différentes).
*   **Affiner le mapping :** Tester des décalages (ROT) sur le texte substitué ou ajuster le mapping de fréquence (la langue n'est peut-être pas l'anglais standard).
*   **Analyse des transitions :** Vérifier si la séquence de changements de signe (0/1) forme un binaire lisible.
*   **Recherche de mots :** Utiliser le texte partiellement lisible pour trouver des mots-clés communs et recalibrer le dictionnaire de substitution.


---
## Résumé au tour 30 (02:43:13)

## Fait
- Copie et analyse du fichier `audio.wav` (16-bit, 44100Hz).
- Identification du signal utile : les échantillons dont la valeur absolue est comprise entre 1 et 8 représentent 58% des données.
- Confirmation que la distribution des signes (+/-) est parfaitement équilibrée (50/50).
- Extraction de la séquence brute en remplaçant les valeurs 1-8 par des lettres (A-H) pour inspection visuelle.

## Échecs / impasses
- Le mapping direct (1=A, 8=H) produit un texte illisible ("AABABBBC...").
- L'analyse de fréquence des lettres obtenues montre une décroissance géométrique (A=26%, H=3%), atypique pour du texte anglais standard.
- Les tentatives de décryptage par décalage (ROT) et par paires de valeurs n'ont pas révélé de mots intelligibles.
- Le bruit (valeurs > 8 ou 0) semble difficile à filtrer sans perdre des données potentielles.

## État actuel
- **Données :** Une séquence longue de symboles 1 à 8 (et -1 à -8).
- **Indices :** Titre "12345678" confirme un alphabet de 8 symboles. Indice "glisten" suggère un jeu de mot ou une transformation (miroir/inversion).
- **Hypothèse :** Les valeurs 1-8 correspondent probablement à des paquets de 3 bits (001 à 111), le signe étant soit du bruit, soit un bit supplémentaire.

## Prochaines pistes
- Convertir la séquence de valeurs absolues (1-8) en binaire (3 bits par échantillon) et regrouper par octets pour obtenir du texte ASCII.
- Tester l'inversion de la séquence (réflexion liée à "glisten").
- Vérifier si le signe (+/-) encode un bit supplémentaire (base 16 au lieu de base 8).
- Chercher le format `csa{...}` dans les résultats de décodage binaire.
