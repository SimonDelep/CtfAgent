# Write-up — Breach: Zero Day (forensics)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Breach Zero Day

## 1. Challenge
- **Nom** : `breach_zero_day`
- **Catégorie** : Forensics
- **Résumé** : Analyse de fichiers de compromission (PCAP, logs XML, dump mémoire) pour retrouver les preuves d'une intrusion.

## 2. Vulnérabilité / Mécanique
- **Faille principale** : Service Windows Update mal configuré (`C:\Windows\System32\WindowsUpdate.exe` au lieu d'un service système normal)
- **Vecteur d'attaque** : Connexion RDP depuis l'IP `10.14.22.158` avec le compte `svc_backup`
- **Données sensibles** : Chaînes encodées (Base64-like) dans le dump mémoire contenant potentiellement des clés ou tokens

## 3. Étapes de résolution

### Étape 1 : Récupération des fichiers
```bash
find / -name "fenwick*" 2>/dev/null
# Copie des 3 fichiers dans le workdir :
# - fenwick_capture.pcap
# - fenwick_security.xml  
# - fenwick_memdump.txt
```

### Étape 2 : Identification des fichiers
```bash
file fenwick_capture.pcap fenwick_security.xml fenwick_memdump.txt
# Résultats :
# - pcap capture file (Ethernet, version 2.4)
# - XML 1.0 document, ASCII text
# - ASCII text (dump mémoire)
```

### Étape 3 : Analyse du fichier XML (logs de sécurité)
```bash
cat fenwick_security.xml
```
**Observations clés** :
- Provider : `Microsoft-Windows-PrintService` (EventID 307)
- Service suspect : `C:\Windows\System32\WindowsUpdate.exe`
- Connexions RDP (port 3389) depuis `10.14.22.158`
- Utilisateur : `svc_backup`
- Machine cible : `FNW-WKS047.fenwick.local`

### Étape 4 : Analyse du dump mémoire
```bash
strings fenwick_memdump.txt | grep -E '[A-Za-z0-9+/=_-]{20,}'
```
**Chaînes suspectes identifiées** :
```
PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j
ag2+b2tfU2=A=wO+c7vlO,TDDXG_7QacpvSoNa66Ckif
Fq7zVQSp3cct/Nk-ebjmHW5K62RoJLQNfcRAp/C
```
- Tentative de décodage Base64 → résultats binaires (données chiffrées ou nonces)
- URLs internes : `https://fenwick-intranet.local/api/status`
- Utilisateur : `d.reyes`

### Étape 5 : Analyse du PCAP
```bash
tcpdump -r fenwick_capture.pcap -n | head -50
```
**Observations** :
- Connexions vers `10.14.0.9:8443` (HTTPS)
- Handshake TCP visible (SYN, SYN-ACK, ACK)
- Trafic chiffré (port 8443)

## 4. Flag
> **Note** : La trajectoire s'arrête pendant l'analyse. Le flag n'a pas été extrait dans l'historique fourni. Les chaînes encodées du memdump (`PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j` et similaires) nécessitent un décodage supplémentaire ou une clé de déchiffrement pour révéler le flag final.

---

**Outils utilisés** : `find`, `file`, `strings`, `tcpdump`, Python (base64)  
**Temps estimé** : ~30 minutes d'analyse  
**Difficulté** : Moyen (Forensics multi-fichiers)