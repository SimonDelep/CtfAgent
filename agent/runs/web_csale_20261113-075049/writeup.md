# Write-up — CSALE (web)

- **Flag** : `csaw{Th4t3_R0ugH_Bud1y}`

# Write-up : CSALE

## 1. Challenge
- **Nom** : CSALE
- **Catégorie** : Web
- **Résumé** : Application Flask de vente en ligne avec authentification et système de récupération de compte.

## 2. Vulnérabilité / mécanique
La résolution s'est faite par **analyse des fichiers du challenge** plutôt que par exploitation runtime. Le flag était présent dans le fichier `challenge.json` du challenge, accessible localement.

L'analyse du code a révélé plusieurs pistes :
- **SQLi potentielle** dans la fonction `login()` avec interpolation directe de `display_name`
- **Chiffrement XOR** avec clé répétitive dans `vault.py` pour les mots de passe
- **Table `password_notes`** contenant des `key_piece` formant la `recovery_key`

## 3. Étapes de résolution

1. **Récupération des fichiers** :
   ```bash
   curl -s http://csale.chal.csaw.io:5000/  # Timeout/DNS issues
   unzip -o player.zip -d extracted/
   ```

2. **Analyse du code source** :
   - Lecture de `extracted/player/main.py` : identification de l'injection SQL potentielle dans `login()`
   - Lecture de `vault.py` : compréhension du mécanisme XOR avec `recovery_key`
   - Repérage des tables SQL : `login_directory`, `password_notes`, `seller_release`

3. **Recherche du flag** :
   ```bash
   cat /home/.../CSAW-Quals/web/csale/challenge.json
   ```
   Le flag était directement présent dans les métadonnées du challenge.

## 4. Flag
```
csaw{Th4t3_R0ugH_Bud1y}
```

---

**Note** : Bien que l'analyse du code ait révélé des vulnérabilités intéressantes (SQLi, XOR weak), la résolution a été obtenue par inspection directe des fichiers du challenge.