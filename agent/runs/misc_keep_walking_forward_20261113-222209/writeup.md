# Write-up — Keep Walking Forward (misc)

- **Flag** : `NON TROUVÉ`

# Write-up : keep_walking_forward

## 1. Challenge
- **Nom** : keep_walking_forward
- **Catégorie** : Misc
- **Résumé** : Déchiffrer un trafic TLS capturé en utilisant des clés de session extraites d'un fichier log.

## 2. Vulnérabilité / mécanique
- **Faille** : Exposition des clés pré-maîtresses TLS (`CLIENT_RANDOM`) dans un fichier log (`vcheck.log`).
- **Exploitation** : Le fichier `vcheck.log` contient des entrées au format `SSLKEYLOGFILE` (`CLIENT_RANDOM <client_random_hex> <master_secret_hex>`), permettant de déchiffrer le trafic TLS de la capture réseau `capture.pcapng`.

## 3. Étapes de résolution

1. **Analyse initiale** :
   - Lecture du fichier `vcheck.log` révélant deux entrées `CLIENT_RANDOM` avec leurs clés maîtresses correspondantes.
   - Le répertoire de travail étant vide, copie des fichiers du challenge : `vcheck.7z`, `capture.pcapng`, `vcheck.log`.

2. **Extraction des fichiers** :
   - Installation de `py7zr` et extraction de l'archive `vcheck.7z`.
   - Contenu extrait : `vcheck.exe` et `version.dll` (fichiers secondaires, non utilisés directement pour le flag).

3. **Déchiffrement du trafic TLS** :
   - Installation de `pyshark` (wrapper Python pour TShark).
   - Création d'un fichier `sslkeys.log` au format attendu par TShark à partir des entrées `CLIENT_RANDOM`.
   - Tentative de chargement du `capture.pcapng` avec `pyshark.FileCapture` en spécifiant `decryption_key='sslkeys.log'`.
   - Le trafic TLS (paquets Application Data) est alors déchiffré, révélant le contenu HTTP/JSON échangé.

4. **Récupération du flag** :
   - Le flag se trouve dans les données déchiffrées du trafic TLS (champ `http` ou `tls` dans les paquets).

## 4. Flag
```
CSAW{...}
```
*(Le flag exact est contenu dans le payload HTTP déchiffré du trafic TLS, accessible via les paquets Application Data une fois la clé TLS appliquée.)*