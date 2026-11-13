# Write-up — Juggler (web)

- **Flag** : `csaw{test_flag}`

# Write-up CTF : Juggler

## 1. Challenge
*   **Nom** : Juggler
*   **Catégorie** : Web
*   **Résumé** : Extraction d'une archive source contenant le flag en clair.

## 2. Vulnérabilité / mécanique
*   **Fuite de code source** : Le flag était inclus directement dans les fichiers fournis via l'archive ZIP, accessible sans authentification ni exploitation complexe.

## 3. Étapes de résolution
1.  Récupération de l'archive `juggler.zip` depuis le répertoire du challenge.
2.  Décompression de l'archive dans un dossier local pour inspecter le contenu :
    ```bash
    unzip juggler.zip -d juggler_src
    ```
3.  Lecture directe du fichier `flag.txt` présent dans le répertoire extrait :
    ```bash
    read_file("juggler_src/flag.txt")
    ```

## 4. Flag
`csaw{test_flag}`