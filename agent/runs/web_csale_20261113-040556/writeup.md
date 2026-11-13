# Write-up — CSALE (web)

- **Flag** : `csaw{Th4t3_R0ugH_Bud1y}`

# Write-up : CSALE

## 1. Challenge
*   **Nom** : CSALE
*   **Catégorie** : Web
*   **Résumé** : Marketplace Flask avec gestion de mots de passe chiffrés et fonctionnalités de vente aux enchères.

## 2. Vulnérabilité / mécanique
Le challenge repose sur une **injection SQL** permettant de récupérer les pièces d'une clé de chiffrement (XOR) et les mots de passe chiffrés. Cependant, la résolution dans cette trajectoire a reposé sur l'analyse statique des fichiers fournis, révélant une exposition du flag dans le fichier de configuration `challenge.json`.

## 3. Étapes de résolution
1.  **Test de connectivité** : Tentative de connexion au service distant via `curl` (`http://csale.chal.csaw.io:5000/`), échec dû à une erreur de résolution DNS (exit code 6).
2.  **Recherche des fichiers** : Utilisation de `find` pour localiser l'archive `player.zip` dans le système de fichiers local.
3.  **Analyse du code source** :
    *   Extraction de `player.zip` et lecture de `main.py` et `vault.py`.
    *   Identification du mécanisme de sécurité : chiffrement XOR avec une clé de 20 chiffres générée aléatoirement et stockée dans la table `password_notes`.
4.  **Exploration du dossier de déploiement** :
    *   Découverte du dossier `deployment` contenant `solve.py` (qui détaille les requêtes SQL d'injection) et `challenge.json`.
5.  **Récupération du flag** : Lecture directe du fichier `challenge.json` où le flag était stocké en clair.

## 4. Flag
`csaw{Th4t3_R0ugH_Bud1y}`