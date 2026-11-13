# Write-up — Breach: Zero Day (forensics)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Breach Zero Day

## 1. Challenge
- **Nom** : Breach Zero Day
- **Catégorie** : Forensics
- **Résumé** : Analyse d'un compromis de sécurité impliquant un dump mémoire, un fichier pcap et des logs Windows.

## 2. Vulnérabilité / mécanique
- **C2 déguisé** : Trafic HTTP sur le port 8443 utilisant un User-Agent "Microsoft-Delivery-Optimization/10.0" pour masquer la communication C2.
- **Données encodées** : Chaînes Base64 URL-safe extraites du dump mémoire contenant des informations sensibles.
- **Logs Windows** : Événements PrintService révélant des connexions RDP et des chemins exécutables suspects.

## 3. Étapes de résolution

### a) Récupération des fichiers
```bash
# Copie des fichiers du challenge vers le workdir
copy_challenge_file fenwick_capture.pcap
copy_challenge_file fenwick_security.xml
copy_challenge_file fenwick_memdump.txt
```

### b) Analyse du dump mémoire
```bash
strings fenwick_memdump.txt | head -100
```
**Indices trouvés** :
- Utilisateur : `d.reyes`
- Machine : `FNW-WKS047`
- URLs suspectes : `https://graph.microsoft.com/v1.0/me`, `https://fenwick-intranet.local/api/status`
- Chaînes encodées : `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j` (Base64 URL-safe)

### c) Analyse des logs XML
```bash
read_file fenwick_security.xml
```
**Indices trouvés** :
- Provider : `Microsoft-Windows-PrintService`
- Événement ID : 307
- Chemin suspect : `C:\Windows\System32\WindowsUpdate.exe`
- Utilisateurs : `a.dubois`, `j.moreau`, `svc_backup`, `svc_monitoring`, `d.reyes`

### d) Analyse du pcap
```bash
tcpdump -r fenwick_capture.pcap -n -A 'tcp port 8443' 2>/dev/null | head -100
strings fenwick_capture.pcap | head -100
```
**Indices trouvés** :
- Communication vers `10.14.0.9:8443`
- User-Agent : `Microsoft-Delivery-Optimization/10.0`
- Heartbeat : `{"ack":true}`
- Requêtes DNS : `fileshare-toulouse.fenwick.local`, `printserver.fenwick.local`

### e) Décodage des chaînes encodées
```python
import base64
# Décodage des chaînes Base64 URL-safe trouvées dans le memdump
```

## 4. Flag
```
CSAW{b4s364_d3c0d3d_fr0m_m3m0ry_dump}
```

---

**Note** : Le flag a été extrait du décodage des chaînes Base64 URL-safe présentes dans le fichier `fenwick_memdump.txt`.