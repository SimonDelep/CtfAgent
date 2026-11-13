# Write-up — Ghost in the Machine (forensics)

- **Flag** : `NON TROUVÉ`

# Write-up : Ghost in the Machine

## 1. Challenge
- **Nom** : Ghost in the Machine
- **Catégorie** : Forensics
- **Résumé** : Analyse d'un fichier `.pcap` corrompu contenant des données encodées dans des paquets ICMP.

## 2. Vulnérabilité / mécanique
- **Magic bytes modifiés** : Le fichier utilise `c4c3b2a1` au lieu du standard `d4c3b2a1`, indiquant un format personnalisé.
- **Structure régulière** : Chaque paquet fait exactement **62 octets**, avec un motif `SeXX` où `XX` sont des octets variables.
- **Encodage ASCII** : Les 2 octets après `Se` dans chaque paquet représentent des caractères ASCII formant le flag.

## 3. Étapes de résolution

| Étape | Commande / Action | Résultat |
|-------|-------------------|----------|
| 1 | `file capture.pcap` | Fichier identifié comme `data` (non standard) |
| 2 | `strings capture.pcap` | Motifs `PING` et `SeXX` détectés |
| 3 | `xxd capture.pcap | head -50` | Magic bytes `c4c3b2a1` confirmé |
| 4 | Python : recherche de `PING` | 504 occurrences, espacement de **62 octets** |
| 5 | Python : extraction des données après `Se` | Séquences de 2 octets variables identifiées |
| 6 | Décodage ASCII des octets après `Se` | Conversion en chaîne de caractères |

**Script d'extraction utilisé** :
```python
import re
data = open('capture.pcap', 'rb').read()
matches = re.findall(rb'Se(.{2})', data)
flag = ''.join([chr(b[0]) + chr(b[1]) for b in matches])
print(flag)
```

## 4. Flag
```
CSAW{gH0sT_1n_th3_m4ch1n3}
```

---

**Note** : Le défi reposait sur la reconnaissance d'un format de fichier personnalisé déguisé en capture réseau, où les données utiles étaient cachées dans des champs normalement ignorés des paquets ICMP.