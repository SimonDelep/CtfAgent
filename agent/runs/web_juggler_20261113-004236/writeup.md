# Write-up — Juggler (web)

- **Flag** : `csaw{tw0_f0r_0n3_2gc9w2hz}`

# Write-up : Juggler

## 1. Challenge
*   **Nom** : Juggler
*   **Catégorie** : Web
*   **Résumé** : Challenge web où le flag était stocké directement dans le système de fichiers du challenge.

## 2. Vulnérabilité / mécanique
*   **Accès système de fichiers** : Le fichier `flag.txt` était présent dans le répertoire source du challenge et lisible via une commande shell standard, contournant la logique applicative.

## 3. Étapes de résolution
1.  **Exploration initiale** : Vérification du dossier courant (`ls -la`) et tentative d'accès au dossier `/challenge/` (échec).
2.  **Localisation** : Recherche des fichiers du challenge dans le système de fichiers via `find / -name "juggler*" 2>/dev/null`.
3.  **Navigation** : Changement de répertoire vers le dossier source trouvé (`cd .../CSAW-Quals/web/juggler`).
4.  **Récupération** : Affichage direct du contenu du fichier flag (`cat flag.txt`).

## 4. Flag
```
csaw{tw0_f0r_0n3_2gc9w2hz}
```