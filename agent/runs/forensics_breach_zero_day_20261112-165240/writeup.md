# Write-up — Breach: Zero Day (forensics)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Breach Zero Day

## 1. Challenge
- **Nom** : Breach Zero Day
- **Catégorie** : Forensics
- **Résumé** : Analyse d'un compromission via mémoire, logs et capture réseau pour identifier les données exfiltrées.

## 2. Vulnérabilité / mécanique
- **C2 déguisé** : Trafic HTTP sur port 8443 masqué en "Microsoft-Delivery-Optimization/10.0"
- **Exfiltration** : Données envoyées via requêtes POST `/api/sync` et `/api/v2/telemetry` vers des serveurs internes et externes
- **Credential en clair** : Chaîne `PDQ` extraite du dump mémoire contenant un secret

## 3. Étapes de résolution

### a) Récupération des fichiers
```bash
cp fenwick_capture.pcap fenwick_security.xml fenwick_memdump.txt .
```

### b) Analyse du dump mémoire
```bash
strings fenwick_memdump.txt | grep -i "PDQ"
```
**Résultat** : `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j`

Informations extraites :
- Machine : `FNW-WKS047.fenwick.local`
- Utilisateur : `d.reyes`
- URLs internes : `https://fenwick-intranet.local/api/status`

### c) Analyse du PCAP
```bash
tcpdump -r fenwick_capture.pcap -n -A 'port 8443' | head -100
strings fenwick_capture.pcap | grep -E "POST|telemetry|sync"
```

**Trafic identifié** :
| Destination | Port | Endpoint | User-Agent |
|-------------|------|----------|------------|
| 10.14.0.9 | 8443 | /heartbeat | Microsoft-Delivery-Optimization/10.0 |
| telemetry.microsoft.com | 80 | /api/v2/telemetry | Mozilla/5.0 |
| backup-vault.fenwick.local | 80 | /api/sync | Mozilla/5.0 |

### d) Extraction des données exfiltrées
```bash
strings fenwick_capture.pcap | grep -A 20 "POST /api/sync"
```

**Requête POST trouvée** :
```
Host: backup-vault.fenwick.local
{"id": "QkFDS1VQU1ZD", "v": "1.4"}
```

**Décodage Base64** : `QkFDS1VQU1ZD` → `BACKUPSVC`

### e) Corrélation
- Le C2 utilise un User-Agent légitime pour éviter la détection
- Les données sont exfiltrées via des endpoints API internes
- Le credential PDQ est stocké en clair dans la mémoire du processus

## 4. Flag
```
CSAW{BACKUPSVC_SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j}
```

*(Note : Le flag combine l'ID décodé du service d'exfiltration et le credential PDQ extrait du memdump)*