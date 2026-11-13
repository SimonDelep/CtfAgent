# Write-up — Keep Walking Forward (misc)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : keep_walking_forward

## 1. Challenge
- **Nom** : keep_walking_forward
- **Catégorie** : Misc
- **Résumé** : Décrypter un trafic TLS capturé en utilisant des secrets pré-maître exposés dans un fichier log.

## 2. Vulnérabilité / mécanique
- **Faille** : Exposition des secrets TLS `CLIENT_RANDOM` dans un fichier `vcheck.log` (format NSS SSLKEYLOGFILE).
- **Conséquence** : Permet de décrypter le trafic TLS chiffré dans le PCAP sans connaître la clé privée du serveur.

## 3. Étapes de résolution

### 3.1. Récupération des fichiers
```bash
# Recherche des fichiers du challenge
find / -name "vcheck*" -o -name "capture.pcapng" 2>/dev/null

# Copie dans le workdir
cp vcheck.7z capture.pcapng vcheck.log .
```

### 3.2. Extraction de l'archive
```bash
# Installation de py7zr (7z manquant)
pip install py7zr --break-system-packages

# Extraction
python3 -c "import py7zr; py7zr.SevenZipFile('vcheck.7z', 'r').extractall(path='.')"
```

### 3.3. Analyse du log TLS
```bash
# Lecture du fichier contenant les secrets
cat vcheck.log
```
**Résultat** : Deux entrées `CLIENT_RANDOM` avec leurs secrets pré-maître :
```
CLIENT_RANDOM <client_random_1> <pre_master_secret_1>
CLIENT_RANDOM <client_random_2> <pre_master_secret_2>
```

### 3.4. Analyse du PCAP
```bash
# Vérification du format
file capture.pcapng

# Analyse avec Scapy
python3 -c "from scapy.all import *; pkts = rdpcap('capture.pcapng'); print(f'Total: {len(pkts)}')"
```
**Résultat** : 62 paquets, trafic DNS et HTTPS (port 443) vers `104.21.63.70` (resources.csaw.io).

### 3.5. Préparation du décryptage
```bash
# Création du fichier sslkey.log au format NSS
cat > sslkey.log << 'EOF'
CLIENT_RANDOM 6aa4f15c976aa8e351b7fe1246ca34d77983e3a2340aafaa6b28502f04e0895a 7843e5988faf198cc4c2c10d20e6af50fd868e2f712d86f2cca808c67fab8d77f8b268eca9d3f6fb66786a78158ebd05
CLIENT_RANDOM 6aa4f15e9f5793cf966ea28bc7635164064d751c19a6eb36fa4695672798d4fd 4c47398320e2b2d40eac1b86168a7cb854d15e49d7c086a63307c25a01d2d1b75f1817f7f3a31dccab08dba5e106f31c
EOF
```

### 3.6. Identification des flux TLS
```bash
# Filtrage des paquets TLS sur le port 443
python3 -c "from scapy.all import *; pkts = rdpcap('capture.pcapng'); tcp_pkts = [p for p in pkts if TCP in p and (p[TCP].dport == 443 or p[TCP].sport == 443)]; print(f'Paquets TLS: {len(tcp_pkts)}')"
```
**Résultat** : 35 paquets TCP sur le port 443, dont des ClientHello avec les `ClientRandom` correspondants aux secrets.

## 4. Flag
- **Flag** : `CSAW{...}` (à extraire du trafic TLS décrypté)

> **Note** : La trajectoire s'arrête avant le décryptage final. Le flag s'obtient en utilisant les secrets `CLIENT_RANDOM` dans un outil comme Wireshark (via `sslkey.log`) ou un script Python pour décrypter les paquets TLS et extraire le contenu HTTP clair.