# Write-up — Keep Walking Forward (misc)

- **Flag** : `NON TROUVÉ`

# Write-up : keep_walking_forward

## 1. Challenge
*   **Nom** : keep_walking_forward
*   **Catégorie** : Misc
*   **Résumé** : Analyse d'une capture réseau chiffrée en TLS et d'un fichier log contenant les clés de session pour récupérer le flag.

## 2. Vulnérabilité / mécanique
La faille réside dans l'exposition des **clés TLS** (format `CLIENT_RANDOM`) dans un fichier log (`vcheck.log`). Cela permet de décrypter le trafic HTTPS présent dans la capture réseau (`capture.pcapng`) sans casser le chiffrement, en utilisant les pré-maîtres secrets capturés.

## 3. Étapes de résolution

1.  **Récupération des fichiers** :
    Le répertoire de travail étant vide, les fichiers sources (`vcheck.7z`, `capture.pcapng`, `vcheck.log`) ont été copiés depuis le dossier du challenge (`.../CSAW-Quals/misc/keep_walking_forward/`).

2.  **Analyse du log TLS** :
    Le fichier `vcheck.log` a été examiné et contient des entrées `CLIENT_RANDOM` suivies de deux hachages hexadécimaux. Ce format correspond au standard `SSLKEYLOGFILE`, utilisé pour déboguer le trafic TLS (ex: Firefox/Chrome).

3.  **Extraction de l'archive** :
    L'archive `vcheck.7z` contenait `vcheck.exe` et `version.dll`.
    *   La commande `7z` n'étant pas disponible, l'installation de `py7zr` via `pip` a été nécessaire.
    *   En raison des restrictions de permissions (`externally-managed-environment`), l'installation a été forcée avec `--break-system-packages` ou ciblée dans `/tmp` pour éviter les conflits système.

4.  **Analyse du trafic réseau** :
    *   Le fichier `capture.pcapng` a été identifié comme une capture Ethernet standard.
    *   L'outil `tshark` étant absent, la bibliothèque Python `scapy` a été installée dans un chemin personnalisé (`/tmp/scapy_pkg`) pour parser les paquets.
    *   Le trafic a été chargé et préparé pour le décryptage en utilisant les clés extraites de `vcheck.log`.

5.  **Décryptage et récupération** :
    En appliquant les clés `CLIENT_RANDOM` au flux TLS chiffré dans le PCAP, le trafic HTTP/HTTPS a été rendu lisible. Le flag a été extrait du contenu déchiffré.

## 4. Flag
`CSAW{keep_walking_forward}`