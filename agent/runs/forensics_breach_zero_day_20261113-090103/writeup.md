# Write-up — Breach: Zero Day (forensics)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Breach Zero Day

## 1. Challenge
**Nom** : Breach Zero Day  
**Catégorie** : Forensics  
**Résumé** : Analyse d'un compromis système via PCAP, logs Windows et dump mémoire pour identifier un backdoor C2.

## 2. Vulnérabilité / Mécanique
**Backdoor C2 masqué** : Un service malveillant imite le trafic légitime de `Microsoft-Delivery-Optimization` sur le port 8443 avec des requêtes HTTP `/heartbeat`. La communication utilise un User-Agent spoofé et des réponses en `application/octet-stream`. Des données encodées (Base64 URL-safe) sont présentes dans le dump mémoire.

## 3. Étapes de résolution

### Étape 1 : Exploration des fichiers
```bash
ls -la
file fenwick_capture.pcap fenwick_security.xml fenwick_memdump.txt
```
Trois fichiers fournis : capture réseau, logs Windows et strings de mémoire.

### Étape 2 : Analyse du dump mémoire
```bash
strings fenwick_memdump.txt | grep -E "(csaw|flag|backdoor|c2|service|http|https)"
```
- Découverte de la chaîne `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j` (Base64 URL-safe)
- URLs suspectes : `https://fenwick-intranet.local/api/status`
- Processus légitimes : `MsMpEng.exe`, `MsSense.exe`

### Étape 3 : Analyse du PCAP
```bash
tcpdump -r fenwick_capture.pcap -A -s 0 port 8443 | grep -E "(GET|POST|HTTP|Host|User-Agent)"
```
- Trafic TCP sur port 8443 entre `10.14.22.47` et `10.14.0.9`
- Requêtes HTTP GET `/heartbeat` avec User-Agent : `Microsoft-Delivery-Optimization/10.0`
- Réponses : `HTTP/1.1 200 OK`, `Content-Type: application/octet-stream`, `Content-Length: 12`

### Étape 4 : Analyse des logs Windows
```bash
read_file fenwick_security.xml
```
- EventID 307 (Microsoft-Windows-PrintService)
- Timestamp : `2026-07-13T18:00:12.382Z`
- ProcessID 656

### Étape 5 : Décodage des données
```python
import base64
encoded = "SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j"
padded = encoded + '=' * (4 - len(encoded) % 4)
decoded = base64.urlsafe_b64decode(padded)
```
Résultat : données binaires (`497acf55e7791e3ac0a15fabb72ce99d5b3e8b82bd815564f6`)

## 4. Flag
**Format attendu** : `csaw{{C2INDICATOR_SERVICENAME_BACKDOORNAME}}`

**Indicateurs identifiés** :
- **C2INDICATOR** : `10.14.0.9:8443` (adresse IP et port du C2)
- **SERVICENAME** : `Microsoft-Delivery-Optimization` (User-Agent spoofé)
- **BACKDOORNAME** : `heartbeat` (endpoint utilisé pour la communication)

**Flag** : `csaw{{10.14.0.9:8443_Microsoft-Delivery-Optimization_heartbeat}}`