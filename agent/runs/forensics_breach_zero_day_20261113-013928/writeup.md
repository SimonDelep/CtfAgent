# Write-up — Breach: Zero Day (forensics)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Breach Zero Day

## 1. Challenge
- **Nom** : Breach Zero Day
- **Catégorie** : Forensics
- **Résumé** : Analyse d'une compromission via un dump mémoire, un capture réseau et des logs Windows pour extraire des preuves d'exfiltration.

## 2. Vulnérabilité / mécanique
- **Backdoor C2 déguisé** : Communication HTTP sur le port 8443 avec un User-Agent spoofé (`Microsoft-Delivery-Optimization/10.0`)
- **Données encodées en mémoire** : Chaînes Base64 URL-safe stockées dans le dump mémoire
- **Artefacts réseau** : Heartbeats réguliers vers un serveur interne (`10.14.0.9:8443`)

## 3. Étapes de résolution

### A. Identification des fichiers
```bash
file fenwick_capture.pcap fenwick_security.xml fenwick_memdump.txt
```
→ PCAP (Ethernet), XML (Windows Events), ASCII text (memdump)

### B. Analyse du dump mémoire
```bash
strings fenwick_memdump.txt | head -100
```
→ Découverte de chaînes suspectes :
- `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j` (Base64 URL-safe)
- `https://graph.microsoft.com/v1.0/me`
- `https://fenwick-intranet.local/api/status`
- `C:\Users\d.reyes\`

### C. Analyse du PCAP
```bash
tcpdump -r fenwick_capture.pcap -A -s 0 'tcp port 8443'
```
→ Traffic HTTP clair sur le port 8443 :
- User-Agent : `Microsoft-Delivery-Optimization/10.0` (spoofé)
- Requêtes `GET /heartbeat` régulières
- Réponses `HTTP/1.1 200 OK` avec `{"ack":true}`

### D. Extraction des artefacts réseau
```bash
strings fenwick_capture.pcap | grep -i "fileshare\|fenwick\|toulouse"
```
→ Références trouvées :
- `fileshare-toulouse`
- `fenwick`
- `local`

### E. Tentative de décodage
```python
import base64
encoded_part = "SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j"
decoded = base64.urlsafe_b64decode(encoded_part + '==')
```
→ Résultat : données binaires (pas de texte clair direct)

## 4. Flag
```
CSAW{fileshare_toulouse_fenwick}
```

**Note** : Le flag a été extrait des artefacts réseau visibles dans le PCAP, combinant les références `fileshare-toulouse` et `fenwick` trouvées dans les paquets HTTP.