# Write-up — 12345678 (misc)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Audio Base64

## 1. Challenge
- **Nom** : `12345678`
- **Catégorie** : Misc
- **Résumé** : Extraction de chaînes Base64 cachées dans un fichier audio WAV.

## 2. Vulnérabilité / mécanique
- **Faille** : Données Base64 non masquées dans les métadonnées (chunks ID3, LIST INFO) et le flux audio du fichier WAV.
- **Astuce** : Recherche de motifs Base64 (`[A-Za-z0-9+/]{4,}={0,2}`) dans le fichier binaire, puis décodage pour révéler le flag.

## 3. Étapes de résolution

### a) Initialisation
- Copie du fichier challenge dans le workdir :
  ```bash
  copy_challenge_file("12345678 (1).wav", "audio.wav")
  ```

### b) Extraction des chaînes Base64
- Script Python pour extraire toutes les chaînes Base64 valides :
  ```python
  b64_pattern = rb'[A-Za-z0-9+/]{4,}={0,2}'
  matches = re.findall(b64_pattern, data)
  ```
- **Résultat** : 57 chaînes trouvées.

### c) Décodage et analyse
- Décodage de chaque chaîne Base64 :
  - `Ml81dDNAMV8=` → `2_5t3@1_` (apparaît 2 fois)
  - `qsTDRC` → `\xaa\xc4\xc3D` (clé XOR potentielle)
- Le flux décodé complet fait 153 octets.
- Structure finale du payload : `...$C2_5t3@1_\xaa\xc4\xc3D2_5t3@1_`

### d) Tentative de flag
- Format supposé : `csaw{2_5t3@1_}`
- **Résultat** : Refusé (faux positif, flag d'exemple présent dans les fichiers)

## 4. Flag
- **Flag tenté** : `csaw{2_5t3@1_}`
- **Statut** : Refusé (nécessite une transformation XOR ou recherche supplémentaire)

---

**Note** : La trajectoire montre que `2_5t3@1_` est présent dans le fichier mais n'est pas le flag final. Une transformation XOR avec la clé `\xaa\xc4\xc3D` a été testée sans succès immédiat.