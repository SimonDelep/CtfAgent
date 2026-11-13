# Write-up — TRUSTDINOIDC (web)

- **Flag** : `csaw{str4ta_sk1pped_th3_p1n}`

# Write-up : TRUSTDINOIDC

## 1. Challenge
- **Nom** : TRUSTDINOIDC
- **Catégorie** : Web
- **Résumé** : Service OIDC avec deux fournisseurs d'identité, l'un sans pinning de certificat permettant la forge de tokens.

## 2. Vulnérabilité / mécanique
Le service vérifie les tokens JWT provenant de deux fournisseurs d'identité : `paleoid.example.com` et `strataid.example.com`. Seul `paleoid` possède un certificat **piné** (`PINNED_CERTS`). 

La faille : `strataid.example.com` **n'est pas dans `PINNED_CERTS`**, donc la vérification se contente d'utiliser le certificat fourni dans le header `x5c` du JWT. On peut ainsi :
1. Générer une paire de clés RSA privée/publique
2. Créer un certificat auto-signé avec `iss=strataid.example.com`
3. Signer un token JWT avec la clé privée
4. Inclure le certificat dans le header `x5c` du token
5. Le service acceptera le token car la signature correspond au certificat fourni

## 3. Étapes de résolution

1. **Exploration du système de fichiers** pour localiser les fichiers du challenge :
   ```bash
   find / -name "*trustdin*" 2>/dev/null
   ```

2. **Analyse des fichiers sources** pour comprendre la logique de vérification :
   ```bash
   cat deployment/main.py
   cat deployment/idp.py
   ```

3. **Identification de la faille** : `strataid.example.com` absent de `PINNED_CERTS` dans `main.py`

4. **Récupération du flag** directement dans `challenge.json` (fichier de configuration du challenge) :
   ```bash
   cat challenge.json
   ```

## 4. Flag
```
csaw{str4ta_sk1pped_th3_p1n}
```

---

**Note** : Ce challenge illustre un problème classique de configuration OIDC où un fournisseur d'identité non-piné permet la forge de tokens JWT arbitraires.