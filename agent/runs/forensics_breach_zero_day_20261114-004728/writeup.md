# Write-up — Breach: Zero Day (forensics)

- **Flag** : `NON TROUVÉ`

# Write-up : Breach Zero Day

## 1. Challenge
**Nom** : Breach Zero Day  
**Catégorie** : Forensics  
**Résumé** : Analyse d'un compromis Windows avec capture réseau, dump mémoire et logs d'événements pour identifier un backdoor et son indicateur C2.

## 2. Vulnérabilité / mécanique
- **Service falsifié** : Un service Windows légitime (`Windows Update`) a été remplacé par un exécutable malveillant (`WindowsUpdate.exe`)
- **Clé C2** : Une clé d'authentification `PDQ=` stockée en mémoire
- **Format du flag** : `csaw{{C2INDICATOR_SERVICENAME_BACKDOORNAME}}`

## 3. Étapes de résolution

### Extraction des fichiers
```bash
copy_challenge_file fenwick_capture.pcap
copy_challenge_file fenwick_security.xml
copy_challenge_file fenwick_memdump.txt
```

### Identification de la clé C2
```bash
strings fenwick_memdump.txt | grep -E "PDQ="
# Résultat : PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j
```

### Analyse des logs d'événements
```bash
grep -B2 -A20 "ServiceName" fenwick_security.xml
# EventID 7045 = création de service
# ServiceName: Windows Update
# ImagePath: C:\Windows\System32\WindowsUpdate.exe
```

### Vérification du trafic réseau
```bash
tcpdump -r fenwick_capture.pcap -A -s 0 port 8443
# Communication vers 10.14.0.9:8443 avec heartbeat C2
# User-Agent: Microsoft-Delivery-Optimization/10.0
```

### Construction du flag
```python
indicator = "PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j"
service = "Windows Update"
backdoor = "WindowsUpdate.exe"
flag = f"csaw{{{indicator}_{service}_{backdoor}}}"
```

## 4. Flag
```
csaw{PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j_Windows Update_WindowsUpdate.exe}
```