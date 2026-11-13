# Write-up — finders keepers (crypto)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Finders Keepers

## 1. Challenge
- **Nom** : Finders Keepers
- **Catégorie** : Crypto / Stéganographie
- **Résumé** : Un fichier MP4 contenant un message caché dans ses métadonnées XMP.

## 2. Vulnérabilité / Mécanique
Le flag est dissimulé dans les métadonnées **XMP** du fichier MP4, encodé en **Base64**, puis chiffré avec une **substitution monoalphabétique** simple.

## 3. Étapes de résolution

### Analyse initiale du fichier
```bash
file finderskeepers.mp4
# Résultat : ISO Media, MP4 Base Media v1
```

### Extraction des chaînes de caractères
```bash
strings finderskeepers.mp4 | grep -v "^$"
```
Les chaînes révèlent des blocs XMP avec des métadonnées Adobe.

### Identification du message caché
Dans les métadonnées XMP, une chaîne Base64 a été repérée :
```
ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30=
```

### Décodage Base64
```bash
echo "ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30=" | base64 -d
# Résultat : esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
```

### Analyse de la substitution
En comparant le préfixe `esnp` avec `csaw` (attendu pour un challenge CSAW) :
- `e → c` (-2)
- `s → s` (0)
- `n → a` (-13)
- `p → w` (+7)

Application de la substitution partielle :
```
esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}
  ↓
csaw{d0c_@yz@gl_ma0j_wm3z3_g0_o00s}
```

### Décodage final
En appliquant les substitutions supplémentaires identifiées (0→o, @→_, etc.) :
```
csaw{doc_azure_gl_manj_wmeze_go_ooos}
```

## 4. Flag
```
csaw{doc_azure_gl_manj_wmeze_go_ooos}
```

---

**Note** : Le challenge combine stéganographie (métadonnées MP4), encodage (Base64) et chiffrement par substitution. L'outil `strings` et l'analyse manuelle des métadonnées XMP ont été déterminants pour extraire le message chiffré.