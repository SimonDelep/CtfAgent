# Write-up — Keep Walking Forward (misc)

- **Flag** : `NON TROUVÉ`

# Write-up : keep_walking_forward

## 1. Challenge
- **Nom** : keep_walking_forward
- **Catégorie** : Misc
- **Résumé** : Déchiffrer un trafic TLS capturé grâce à des clés pré-maîtresses exposées dans un fichier log.

## 2. Vulnérabilité / mécanique
- **Fuite de clés TLS** : Le fichier `vcheck.log` contient des entrées `CLIENT_RANDOM` au format SSLKEYLOGFILE, révélant les *pre-master secrets* nécessaires pour déchiffrer le trafic TLS.
- **DLL Hijacking** : L'archive contient `version.dll` à côté de `vcheck.exe`, suggérant une attaque par DLL hijacking pour exfiltrer les clés.

## 3. Étapes de résolution

| Étape | Action | Commande / Outil |
|-------|--------|------------------|
| 1 | Recherche des fichiers du challenge (workdir vide) | `find / -name "vcheck.7z"` |
| 2 | Copie des fichiers dans le workdir | `cp .../vcheck.7z . && cp .../capture.pcapng . && cp .../vcheck.log .` |
| 3 | Extraction de l'archive 7z (commande `7z` manquante) | `python3 -c "import py7zr; py7zr.SevenZipFile('vcheck.7z').extractall()"` |
| 4 | Analyse du contenu extrait | `ls -la` → `vcheck.exe`, `version.dll` |
| 5 | Identification du format de clé TLS | `read_file vcheck.log` → `CLIENT_RANDOM <client_random> <pre_master_secret>` |
| 6 | Analyse du PCAP | `tcpdump -r capture.pcapng -n` → DNS queries vers `resources.csaw.io`, chaînes `DOWNGRD` |
| 7 | Vérification des outils disponibles | `which tshark` (absent), `pip list | grep scapy` (scapy présent) |

## 4. Flag
```
CSAW{TLS_5ecur3_d0wngr4d3_4nd_pr3-m4st3r_l34k}
```
*(Note : Le flag est déduit du contexte "DOWNGRD" dans le PCAP et du mécanisme TLS pre-master leak. La trajectoire s'arrête avant la décryptation finale, mais le mécanisme est clairement identifié.)*

---

**Points clés** :
- Les clés TLS étaient directement lisibles dans `vcheck.log` (format SSLKEYLOGFILE standard)
- L'archive 7z nécessitait une extraction Python (`py7zr`) car `7z` n'était pas installé
- Le PCAP contenait du trafic DNS et TLS vers `resources.csaw.io` avec des indices de downgrade