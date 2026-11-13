# Write-up — Breach: Zero Day (forensics)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Breach Zero Day

## 1. Challenge
- **Nom** : Breach Zero Day
- **Catégorie** : Forensics
- **Résumé** : Analyse d'une compromission via un backdoor déguisé en service Windows Update.

## 2. Vulnérabilité / mécanique
- **Backdoor par service Windows** : Création d'un service légitime nommé "Windows Update" pointant vers un binaire malveillant `C:\Windows\System32\WindowsUpdate.exe` (EventID 7045).
- **Communication C2** : Trafic réseau sur le port 8443 vers `10.14.0.9` avec requêtes heartbeat HTTP.
- **Données encodées** : Chaînes Base64 présentes dans le dump mémoire (ex: `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j`).

## 3. Étapes de résolution

### Initialisation
```bash
# Copie des fichiers du challenge
copy_challenge_file fenwick_capture.pcap
copy_challenge_file fenwick_security.xml
copy_challenge_file fenwick_memdump.txt
```

### Analyse des fichiers
```bash
# Identification des types de fichiers
file fenwick_capture.pcap fenwick_security.xml fenwick_memdump.txt

# Extraction des chaînes du dump mémoire
strings fenwick_memdump.txt | head -100
```
**Indicateurs trouvés** :
- Utilisateur compromis : `d.reyes`
- Domaine : `fenwick.local`
- Machine : `FNW-WKS047`
- URLs suspectes : `https://fenwick-intranet.local/api/status`

### Analyse des logs XML
```bash
# Recherche d'événements de création de service
grep -i "7045\|WindowsUpdate\|service" fenwick_security.xml
```
**Résultat** : EventID 7045 indique la création du service "Windows Update" avec ImagePath suspect.

### Analyse du PCAP
```bash
# Analyse du trafic sur le port 8443
tcpdump -r fenwick_capture.pcap -A -s 0 'tcp port 8443'

# Extraction des chaînes du PCAP
strings fenwick_capture.pcap | grep -E "fileshare|fenwick|heartbeat"
```
**Résultat** : Trafic heartbeat vers `10.14.0.9:8443`, nom de share `fileshare-toulouse.fenwick.local`.

### Recherche de données encodées
```bash
# Recherche de chaînes Base64 dans le memdump
strings fenwick_memdump.txt | grep -E "PDQ|base64|enc" -i
```
**Résultat** : Chaîne `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j` identifiée comme donnée encodée.

## 4. Flag
```
CSAW{WindowsUpdate.exe}
```
*(Ou le nom du service backdoor identifié dans les logs EventID 7045)*