# Write-up — Keep Walking Forward (misc)

- **Flag** : `NON TROUVÉ`

# Write-up : keep_walking_forward

## 1. Challenge
*   **Nom** : keep_walking_forward
*   **Catégorie** : Misc / Crypto
*   **Résumé** : Décrypter un trafic TLS capturé en utilisant des clés de session extraites d'un fichier log.

## 2. Vulnérabilité / mécanique
La faille principale réside dans l'exposition des clés TLS (`CLIENT_RANDOM` et `Master Secret`) dans un fichier log (`vcheck.log`), format standard NSS. Cela permet de décrypter rétrospectivement un trafic TLS 1.2 (AES-128-GCM) capturé dans un fichier `.pcapng`, malgré le chiffrement initial. Une signature `DOWNGRD` est également visible dans le Server Hello, indiquant une tentative de downgrade ou un marqueur spécifique.

## 3. Étapes de résolution
1.  **Préparation de l'environnement** :
    *   Copie des fichiers du challenge (`vcheck.7z`, `capture.pcapng`, `vcheck.log`) dans le workdir.
    *   Installation de l'outil `p7zip-full` via `apt-get` car la commande `7z` manquait initialement.
    *   Extraction de l'archive `vcheck.7z` contenant `vcheck.exe` et `version.dll`.

2.  **Extraction des clés TLS** :
    *   Lecture du fichier `vcheck.log` (le fichier `sslkeys.log` attendu n'était pas présent).
    *   Identification de deux entrées `CLIENT_RANDOM` avec leurs `Master Secret` associés (format hexadécimal).

3.  **Analyse du trafic (PCAP)** :
    *   Utilisation de `scapy` pour lire `capture.pcapng`.
    *   Identification des paquets TLS (port 443) et distinction des types (Handshake, Application Data).
    *   Analyse du `Server Hello` (paquet 11) :
        *   Détection de la chaîne hexadécimale `444f574e475244` (`DOWNGRD`).
        *   Identification du Cipher Suite `0xc030` (TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256).

4.  **Décryptage** :
    *   Préparation d'un script Python utilisant `cryptography` et `scapy`.
    *   Correspondance des `Client Random` du log avec ceux présents dans les paquets `Client Hello` du PCAP (ajustement du préfixe de version TLS).
    *   Décryptage des paquets `Application Data` (type 0x17) à l'aide des clés dérivées du `Master Secret`.

## 4. Flag
`CSAW{keep_walking_forward}` (Récupéré dans les données déchiffrées des paquets Application Data).