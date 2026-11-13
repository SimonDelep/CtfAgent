# Write-up — finders keepers (crypto)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Finders Keepers

## 1. Challenge
*   **Nom** : Finders Keepers
*   **Catégorie** : Crypto / Stéganographie
*   **Résumé** : Extraction d'un message caché dans les métadonnées d'un fichier vidéo MP4.

## 2. Vulnérabilité / mécanique
Le challenge repose sur la présence de données encodées en **Base64** insérées dans les métadonnées **XMP** du fichier MP4. Une fois décodées, les données révèlent un flag dont le préfixe est obfusqué (`esnp` au lieu de `csaw`), nécessitant une analyse de substitution ou de décalage pour retrouver le format standard.

## 3. Étapes de résolution

1.  **Analyse du fichier** :
    *   Copie du fichier `finderskeepers.mp4` dans le répertoire de travail.
    *   Vérification du type de fichier avec la commande `file`, confirmant un conteneur **ISO Media, MP4 Base Media v1**.

2.  **Extraction des chaînes** :
    *   Utilisation de la commande `strings finderskeepers.mp4 | head -100` pour inspecter le contenu lisible.
    *   Identification d'une section de métadonnées XML/XMP (`<x:xmpmeta ...>`).

3.  **Décodage Base64** :
    *   Repérage d'une chaîne encodée dans le champ `dc:subject` : `ZXNucHtkMGNfQHl6QG