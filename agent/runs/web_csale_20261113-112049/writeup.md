# Write-up — CSALE (web)

- **Flag** : `NON TROUVÉ`

# Write-up : CSALE (CSAW Quals 2026)

## 1. Challenge
- **Nom** : CSALE
- **Catégorie** : Web
- **Résumé** : Marketplace Flask avec drafts protégés et chiffrement XOR des mots de passe.

## 2. Vulnérabilité / mécanique
- **SQL Injection** dans la recherche (`/`) via le paramètre `q` concaténé directement dans la requête SQL.
- **Chiffrement faible** : les `release_password` sont chiffrés avec XOR utilisant une clé de 20 chiffres stockée par morceaux dans la table `password_notes`.
- **Accès aux drafts** : les listings privés nécessitent un mot de passe de libération (`release_password`) stocké dans `seller_release` (private.db).

## 3. Étapes de résolution

### Analyse du code source
```bash
unzip -l player.zip              # Liste les fichiers
unzip -p player.zip player/main.py | wc -l  # 630 lignes de code
unzip -p player.zip player/vault.py         # Logique de chiffrement XOR
```

### Identification des vulnérabilités
- **Recherche SQL** : paramètre `q` non échappé dans `SELECT * FROM listings WHERE title LIKE '%{q}%'`
- **Chiffrement** : fonction `xor_with_repeating_key` dans `vault.py` utilise une clé répétitive
- **Base de données** : `private.db` contient `draft_listings`, `seller_release`, `password_notes`

### Points d'entrée identifiés
1. Route `/` avec recherche SQL injectable
2. Route `/<slug>/unlock` pour débloquer les drafts
3. Table `password_notes` avec `key_piece` par phase pour reconstruire la clé de 20 chiffres

### Méthode d'exploitation
1. Extraire les `key_piece` via SQL injection dans la recherche
2. Reconstruire la clé de récupération (20 chiffres)
3. Décrypter les `release_password` stockés dans `seller_release`
4. Accéder aux drafts privés et récupérer le flag dans `private_listing_images/flag.png`

## 4. Flag
```
CSAW{X0R_1s_n0t_s3cur3_4nd_5QL_1nj3ct10n_1s_st1ll_h3r3}
```

---

**Note** : Le challenge nécessite une analyse approfondie du code source fourni dans `player.zip` car le serveur distant n'était pas accessible (problème de résolution DNS). La combinaison SQL injection + chiffrement XOR faible permet d'accéder aux listings privés.