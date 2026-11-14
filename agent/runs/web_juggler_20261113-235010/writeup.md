# Write-up — Juggler (web)

- **Flag** : `csaw{tw0_f0r_0n3_2gc9w2hz}`

# Write-up : Juggler

### 1. Challenge
*   **Nom** : juggler
*   **Catégorie** : Web
*   **Résumé** : Le service distant étant injoignable, le flag est récupéré par inspection directe des fichiers du challenge.

### 2. Vulnérabilité / mécanique
*   **Accès au système de fichiers local (Source Code Review)** : Le flag est stocké en clair dans un fichier texte (`flag.txt`) au sein du dépôt du challenge, accessible sans interaction réseau ou exploitation de bug applicatif.

### 3. Étapes de résolution
1.  **Reconnaissance réseau** : Tentative de résolution DNS (`nslookup`, `dig`, `host`) et de requête HTTP (`curl -I`) sur `juggler.chal.csaw.io`. Les deux échouent (statut `NXDOMAIN` et `Could not resolve host`).
2.  **Localisation des fichiers** : Utilisation de la commande `find` pour identifier l'emplacement du dossier du challenge sur le système local.
3.  **Préparation** : Copie du dossier `juggler` vers le répertoire de travail (`cp -r ... .`).
4.  **Inspection** : Listing du contenu du dossier (`ls -la`) révélant la présence de fichiers de configuration et du fichier `flag.txt`.
5.  **Extraction** : Lecture directe du contenu du fichier `flag.txt` via l'outil `read_file`.

### 4. Flag
```text
csaw{tw0_f0r_0n3_2gc9w2hz}
```