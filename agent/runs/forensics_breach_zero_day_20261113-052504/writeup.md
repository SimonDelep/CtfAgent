# Write-up — Breach: Zero Day (forensics)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Breach Zero Day

## 1. Challenge
**Nom** : breach_zero_day  
**Catégorie** : Forensics  
**Résumé** : Analyse d'une compromission via PCAP, dump mémoire et logs Windows pour identifier un C2 déguisé.

## 2. Vulnérabilité / mécanique
**Masquage de C2** : Un serveur de Command & Control (C2) utilise le User-Agent légitime `Microsoft-Delivery-Optimization/10.0` pour camoufler ses requêtes HTTP sur le port 8443. La backdoor est associée au service Windows `SecurityHealthService`.

## 3. Étapes de résolution

| Étape | Action | Commande / Outil |
|-------|--------|------------------|
| 1 | Copie des fichiers du challenge vers le workdir | `find / -name "fenwick*"` + `copy_challenge_file` |
| 2 | Identification des types de fichiers | `file fenwick_capture.pcap fenwick_security.xml fenwick_memdump.txt` |
| 3 | Analyse initiale des chaînes dans le PCAP | `strings fenwick_capture.pcap \| head -100` |
| 4 | Recherche d'indices dans le memdump | `strings fenwick_memdump.txt \| grep -i "PDQ\|backdoor\|service\|c2"` |
| 5 | Analyse des logs XML (événements Windows) | `strings fenwick_security.xml \| grep -i "EventID\|Data Name"` |
| 6 | Extraction du trafic réseau sur le port 8443 | `tcpdump -r fenwick_capture.pcap -n -A 'tcp port 8443'` |
| 7 | Identification du C2 et du service masqué | User-Agent `Microsoft-Delivery-Optimization/10.0` + IP `10.14.0.9` |

**Indicateurs clés trouvés** :
- **C2** : `10.14.0.9` (serveur recevant les requêtes heartbeat)
- **Service légitime masqué** : `Microsoft-Delivery-Optimization` (User-Agent)
- **Backdoor** : `SecurityHealthService` (trouvé dans le memdump)
- **Domaine** : `fenwick.local` / `fileshare-toulouse.fenwick.local`

## 4. Flag
```
csaw{{10.14.0.9_Microsoft-Delivery-Optimization_SecurityHealthService}}
```

---

**Note** : Le challenge repose sur la corrélation entre trois artefacts (PCAP, memdump, XML) pour reconstituer la chaîne de compromission. Le PCAP révèle le trafic C2, le memdump identifie le service backdoor, et les logs XML confirment l'activité système.