

---
## Résumé au tour 10 (23:14:10)

## Fait
- Copie et vérification du fichier `audio.wav` (WAV PCM 16-bit stéréo, 6MB).
- Extraction des bits de poids faible (LSB) via script Python.
- Détection du caractère `{` à l'index 5 dans le flux LSB (indice fort pour `csaw{`).
- Analyse des valeurs d'échantillons (min/max, distribution).

## Échecs / impasses
- SyntaxError initial dans le script Python (f-string mal échappé).
- Données LSB brutes illisibles (binaire mélangé, pas de texte ASCII complet).
- Séparation des canaux gauche/droit n'a pas révélé de message clair.
- Outil `sox` manquant pour analyse audio rapide.

## État actuel
- Fichier audio chargé et parsé.
- Indice confirmé : le flag est probablement encodé dans les LSB.
- Signal contient beaucoup de silences (valeurs proches de 0).
- Structure du flag : `csaw{...}` (commence par `{` détecté).

## Prochaines pistes
- Nettoyer le script LSB pour extraire uniquement les caractères ASCII imprimables.
- Tester l'extraction sur 2 bits LSB ou ordre des bits inversé.
- Générer un spectrogramme (Python `matplotlib`) pour visualiser le signal.
- Vérifier si un canal spécifique porte le message.


---
## Résumé au tour 20 (23:18:05)

## Fait
- **Préparation :** Renommage du fichier `12345678 (1).wav` vers `audio.wav` pour éviter les erreurs de chemin (espaces/parenthèses).
- **Analyse :** Confirmation des spécifications (Stéréo, 16-bit, 44100 Hz, ~34s) via Python `wave`.
- **Extraction :** Récupération des échantillons bruts et conversion en bits LSB.
- **Découverte :** Détection du caractère `{` à l'index 5 dans le flux LSB (ordre bit 0 en premier), confirmant la présence d'un message caché.

## Échecs / impasses
- **Nom de fichier :** Tentative initiale de lecture directe du fichier original échouée.
- **Mélange des canaux :** Extraction LSB sur tous les échantillons combinés (L+R) produisant du bruit.
- **Ordre des bits :** Tentative d'inversion MSB/LSB sans succès immédiat sur le texte complet.
- **Profondeur :** Tentative d'extraction sur 2 bits LSB qui n'a pas amélioré la lisibilité.
- **Syntaxe :** Erreur Python mineure (f-string) ayant ralenti le débogage.

## État actuel
- **Fichier cible :** `audio.wav` dans le workdir.
- **Indice clé :** Le flag semble commencer par `csaw{` (index 5), mais la suite est illisible (`{!.....Hv...`).
- **Données :** 3 032 104 échantillons totaux disponibles pour traitement.
- **Hypothèse :** Le message est présent mais l'interleaving des canaux ou l'alignement des bits n'est pas encore parfaitement résolu.

## Prochaines pistes
- **Isolation :** Extraire uniquement le canal Gauche ou Droit et réessayer l'extraction LSB.
- **Reconstruction :** Tenter de reconstruire les bytes à partir de l'index 5 en ajustant l'ordre des bits.
- **Vérification :** Chercher la séquence `csaw{` complète dans les données brutes des canaux séparés.
- **Outils :** Utiliser un script dédié pour convertir les bits LSB en texte ASCII directement sans afficher les intermédiaires bruités.


---
## Résumé au tour 30 (23:23:45)

## Fait (actions utiles et ce qu'elles ont donné)
- **Analyse des métadonnées :** Confirmation du format WAV (stéréo, 16-bit, 44100 Hz).
- **Extraction des données brutes :** Identification d'un caractère `{` (ASCII 123) à l'offset 5 dans le flux audio.
- **Analyse LSB :** Extraction des bits de poids faible sur les canaux séparés et combinés, révélant du texte partiellement lisible commençant par `{`.
- **Recherche de motifs :** Tentative de correspondance binaire pour `csaw{` et `{` à travers différents plans de bits.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **LSB global simple :** Le texte devient bruité immédiatement après le `{` initial.
- **Recherche binaire directe :** La séquence `csaw{` n'apparaît pas en LSB/MSB standard.
- **Séparation stricte des canaux :** Isoler uniquement le canal gauche ou droit ne donne pas de flag clair.
- **XOR naïf :** La clé déduite sur les 4 premiers bytes (`[99, 101, 121, 253]` soit `c`, `e`, `y`, `ý`) ne forme pas de mot clé évident.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichier :** `audio.wav`.
- **Point d'ancrage :** Byte 5 = `123` (`{`).
- **Données suspectes :** Bytes 0-4 = `[0, 22, 24, 138]`.
- **Contenu LSB :** Fragment de texte visible (`{!.....Hv...`) mais incomplet.
- **Hypothèse :** Le flag commence par `{` ou les 4 premiers bytes sont XORés avec une clé pour former `csaw`.

## Prochaines pistes
- **Déchiffrement XOR :** Tester des clés courantes ou répétitives sur les 4 premiers bytes pour obtenir `csaw`.
- **Changement de perspective :** Accepter que le flag commence par `{` et se concentrer sur le déchiffrage du texte LSB suivant.
- **Autres plans de bits :** Explorer les bits 1, 2 ou 3 (pas seulement le LSB) pour trouver un texte plus propre.
- **Différence de canaux :** Analyser la différence (L - R) ou le XOR des canaux gauche/droite pour éliminer le bruit audio.


---
## Résumé au tour 40 (23:28:27)

## Fait (actions utiles et ce qu'elles ont donné)
*   **Analyse du fichier :** Copié `123456
