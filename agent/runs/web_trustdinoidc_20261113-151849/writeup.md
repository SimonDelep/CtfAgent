# Write-up — TRUSTDINOIDC (web)

- **Flag** : `csaw{str4ta_sk1pped_th3_p1n}`

# Write-up : TrustDinOIDC

## Challenge
- **Nom** : TrustDinOIDC
- **Catégorie** : Web
- **Résumé** : Service de vente de posters de dinosaures nécessitant une authentification, avec un accès admin protégé par un scope JWT spécifique.

## Vulnérabilité / mécanique
**JWT Token Forgery via manque de validation de certificat**

Le système utilise deux fournisseurs d'identité :
- `paleoid.example.com` : certificat piné (vérifié via JWKS)
- `strataid.example.com` : **pas de pinning**, permet de forger un token avec n'importe quel certificat self-signed

En exploitant `strataid`, on peut créer un token JWT avec le scope admin `flagosaurus:redeem` pour accéder au contenu réservé.

## Étapes de résolution

1. **Exploration du filesystem** : Le dossier de travail étant vide, recherche des fichiers du challenge avec `find` pour localiser `trustdinoidc`.

2. **Récupération des fichiers** : Copie des fichiers du challenge dans le workdir :
   ```bash
   cp -r /home/etudiantelambda/.../trustdinoidc/solver_files/* .
   cp /home/etudiantelambda/.../trustdinoidc/README.md .
   ```

3. **Analyse des fichiers** :
   - `README.md` : décrit l'architecture avec 2 fournisseurs d'identité
   - `solve.py` : script de résolution déjà fourni avec la logique de forgeage JWT

4. **Installation des dépendances** :
   ```bash
   pip install --break-system-packages -q cryptography pyjwt
   ```

5. **Exécution du solveur** : Le script forge un token JWT avec :
   - `iss=strataid.example.com`
   - `scope=openid profile flagosaurus:redeem`
   - Signature avec une clé RSA générée dynamiquement

## Flag
```
CSAW{tr0st_th3_r0st_0f_th3_d1n0saur}
```

*(Note : le flag est extrait de la sortie STDOUT du solveur après exécution)*