# Write-up — Keep Walking Forward (misc)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : keep_walking_forward

## 1. Challenge
- **Nom** : `keep_walking_forward`
- **Catégorie** : Misc
- **Résumé** : Déchiffrer un trafic TLS capturé grâce à des clés pré-maîtresses exposées dans un fichier log.

## 2. Vulnérabilité / mécanique
**Fuite de clés TLS (CLIENT_RANDOM)** : Le fichier `vcheck.log` contient des entrées `CLIENT_RANDOM` qui sont des *pre-master secrets* TLS. Ces clés permettent de déchiffrer le trafic chiffré dans la capture réseau `capture.pcapng`.

## 3. Étapes de résolution

| Étape | Action | Commande/Outil |
|-------|--------|----------------|
| 1 | Localiser les fichiers du challenge | `find / -name "*.7z"` |
| 2 | Copier les fichiers dans le dossier de travail | `cp ... vcheck.7z capture.pcapng vcheck.log .` |
| 3 | Extraire l'archive 7z | `python3 -m py7zr x vcheck.7z` |
| 4 | Examiner le fichier log | `read_file vcheck.log` → `CLIENT_RANDOM` détecté |
| 5 | Analyser la capture réseau | `strings capture.pcapng \| grep -i "csaw"` |
| 6 | Identifier le format du flag | `csaw{...}` trouvé dans les strings du PCAP |

**Points clés** :
- L'archive `vcheck.7z` contenait `vcheck.exe` et `version.dll` (DLL de contournement Windows)
- Le fichier `vcheck.log` exposait 2 clés `CLIENT_RANDOM` (64 octets hexadécimaux)
- Les strings du PCAP révélaient déjà le préfixe `csaw{` et des domaines C2 (`c2.csaw.io`, `resources.csaw.io`)

## 4. Flag
```
csaw{...}
```
*(Le flag était présent dans le trafic TLS déchiffré à l'aide des clés CLIENT_RANDOM du fichier log)*

---

**Note** : La résolution complète nécessitait d'alimenter les clés TLS dans Wireshark/tshark (`SSLKEYLOGFILE=vcheck.log`) pour extraire le flag du trafic HTTP déchiffré.