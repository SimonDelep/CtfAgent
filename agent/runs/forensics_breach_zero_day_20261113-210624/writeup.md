# Write-up — Breach: Zero Day (forensics)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Breach Zero Day

## 1. Challenge
**Nom** : Breach Zero Day  
**Catégorie** : Forensics  
**Résumé** : Analyse d'un incident de compromission avec PCAP, dump mémoire et logs Windows pour identifier un backdoor masqué.

## 2. Vulnérabilité / mécanique
**Masquage de service Windows** : Un backdoor (`WindowsUpdate.exe`) est créé comme service Windows légitime ("Windows Update"), permettant une persistance discrète et un C2 via port 8443.

## 3. Étapes de résolution

### Étape 1 : Récupération des fichiers
Copie des 3 fichiers du challenge dans le workdir :
```bash
copy_challenge_file fenwick_capture.pcap
copy_challenge_file fenwick_security.xml
copy_challenge_file fenwick_memdump.txt
```

### Étape 2 : Analyse du dump mémoire
Extraction des chaînes pour identifier l'indicateur C2 :
```bash
strings fenwick_memdump.txt | grep "PDQ="
```
**Résultat** : `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j`

### Étape 3 : Analyse des logs de services
Examen du fichier XML pour identifier les services suspects créés :
```bash
grep -i "ServiceName\|ImagePath" fenwick_security.xml
```
**Résultat** : Service "Windows Update" avec image `C:\Windows\System32\WindowsUpdate.exe`

### Étape 4 : Analyse du PCAP
Vérification du trafic C2 et des téléchargements :
```bash
tcpdump -r fenwick_capture.pcap -nn 'tcp port 8443'
tcpdump -r fenwick_capture.pcap -nn 'tcp port 80'
```
**Résultat** : Heartbeats vers 10.14.0.9:8443 (C2 interne) et téléchargement de `pkg_6941.cab` depuis 52.38.116.235

### Étape 5 : Construction du flag
Format attendu : `csaw{{C2INDICATOR_SERVICENAME_BACKDOORNAME}}`
- **C2INDICATOR** : `SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j` (valeur PDQ)
- **SERVICENAME** : `Windows Update`
- **BACKDOORNAME** : `WindowsUpdate.exe`

## 4. Flag
```
csaw{{SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j_Windows Update_WindowsUpdate.exe}}
```