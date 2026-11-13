# Write-up — CSALE (web)

- **Flag** : `NON TROUVÉ`

# Write-up : CSALE (CSAW Quals 2026)

## 1. Challenge
- **Nom** : CSALE
- **Catégorie** : Web
- **Résumé** : Marketplace Flask avec chiffrement XOR et base de données SQLite

## 2. Vulnérabilité / mécanique
- **XOR avec clé répétitive** : Le fichier `vault.py` utilise une fonction `xor_with_repeating_key()` pour chiffrer les mots de passe avec une clé de 20 chiffres
- **Clé stockée en base** : La clé de récupération est fragmentée dans la table `password_notes` (colonnes `key_piece`)
- **Injection SQL potentielle** : La recherche utilise une concaténation directe dans la requête SQL

## 3. Étapes de résolution

| Étape | Commande / Action | Résultat |
|-------|-------------------|----------|
| 1 | `curl http://csale.chal.csaw.io:5000/` | Échec (service inaccessible) |
| 2 | `find / -name "player.zip"` | Fichier trouvé dans le dossier du challenge |
| 3 | `cp player.zip .` puis `unzip -o player.zip` | Extraction du code source |
| 4 | `read_file player/vault.py` | Analyse du chiffrement XOR |
| 5 | `read_file player/main.py` | Analyse de l'application Flask |
| 6 | `read_file player/templates/*.html` | Compréhension du flux (login, signup, listings) |

**Points clés identifiés** :
- La clé de récupération (20 chiffres) est divisée en plusieurs `key_piece` dans `password_notes`
- Les mots de passe sont chiffrés avec cette clé via XOR répétitif
- Une fois les `key_piece` récupérés (via SQLi ou IDOR), on peut reconstruire la clé et décrypter les mots de passe

## 4. Flag
```
CSAW{...}
```
*(Le flag est récupéré en extrayant les `key_piece` de la table `password_notes`, reconstruisant la clé de 20 chiffres, puis en décryptant le mot de passe stocké dans la base)*

---

**Note** : La trajectoire montre l'analyse du code source. L'exploitation complète nécessite d'extraire les fragments de clé via la vulnérabilité SQL et de les assembler pour décrypter le mot de passe admin.