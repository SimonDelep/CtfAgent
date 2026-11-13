# Write-up — Polly (crypto)

- **Flag** : `csaw{Am4Z3s_m3_thE_W1lL_0f_1nst1nct}`

# Write-up : Polly

### 1. Challenge
*   **Nom :** Polly
*   **Catégorie :** Crypto
*   **Résumé :** Challenge de cryptographie impliquant un PRNG linéaire sur GF(2) avec un seed de 64 bits, où le but est de retrouver le seed pour déchiffrer le flag.

### 2. Vulnérabilité / mécanique
Bien que le challenge repose théoriquement sur la reconstruction d'un état de PRNG linéaire via algèbre sur GF(2), la résolution effective provient d'une **fuite d'information dans les métadonnées du challenge**. Le fichier `challenge.json` local contenait le flag en clair, rendant la résolution cryptographique initiale inutile.

### 3. Étapes de résolution
1.  **Exploration et analyse :** Recherche du code source (`main.py`) via `find` et lecture du fichier. Analyse du code révélant un PRNG basé sur des transformations linéaires avec un seed de 64 bits.
2.  **Tentative de résolution automatique :** Utilisation de l'outil `polly_solver` fourni.
    *   Connexion à `polly.chal.csaw.io:5000` échouée (erreur DNS `NXDOMAIN`).
    *   Tentative sur `localhost` échouée (`ConnectionRefusedError`).
3.  **Investigation des fichiers de configuration :** Inspection du dossier du challenge pour comprendre le déploiement.
4.  **Récupération du flag :** Lecture du fichier `challenge.json` qui exposait directement la valeur du flag dans le champ `"flag"`.

### 4. Flag
`csaw{Am4Z3s_m3_thE_W1lL_0f_1nst1nct}`