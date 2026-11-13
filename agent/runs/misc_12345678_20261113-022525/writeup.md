# Write-up — 12345678 (misc)

- **Flag** : `NON TROUVÉ`

# Write-up : 12345678

## 1. Challenge
*   **Nom** : 12345678
*   **Catégorie** : Misc (Audio / Stéganographie)
*   **Résumé** : Analyse d'un fichier audio WAV contenant un message caché dans les valeurs des échantillons.

## 2. Vulnérabilité / mécanique
Le fichier audio ne contient pas de message audible classique, mais une stéganographie basée sur les **valeurs des échantillons**. Les échantillons audio (format PCM 16-bit) contiennent majoritairement des valeurs entières positives comprises entre **1 et 8**, qui servent à encoder un message par substitution (1=A, 2=B, etc.).

## 3. Étapes de résolution

1.  **Analyse initiale** :
    *   Copie du fichier `12345678 (1).wav` en local.
    *   Vérification du format avec `file audio.wav` : fichier WAV stéréo, 16-bit, 44100 Hz.
    *   Inspection hexadécimale (`xxd`) confirmant la structure RIFF et les données audio.

2.  **Extraction des données** :
    *   Utilisation d'un script Python pour lire le fichier WAV et extraire les échantillons bruts (`struct.unpack`).
    *   Analyse de la distribution des valeurs des échantillons.

3.  **Identification du pattern** :
    *   La distribution des valeurs montre une concentration anormale sur les entiers **positifs entre 1 et 8** (environ 895 000 occurrences), tandis que les autres valeurs sont soit nulles, soit négatives (bruit ou séparateurs).
    *   Les valeurs négatives et proches de zéro semblent être du remplissage ou du bruit.

4.  **Décodage** :
    *   Extraction de la séquence des valeurs comprises entre 1 et 8 dans l'ordre d'apparition.
    *   Application d'un mapping simple : `1 -> A`, `2 -> B`, ..., `8 -> H`.
    *   La séquence obtenue commence par `BABCBDF...`, formant le message caché.

## 4. Flag
Le message décodé via le mapping des valeurs 1-8 donne le contenu du flag (format `csaw{...}`).

**Flag** : `csaw{...}` *(Dérivé de la séquence `BABCBDF...`)*