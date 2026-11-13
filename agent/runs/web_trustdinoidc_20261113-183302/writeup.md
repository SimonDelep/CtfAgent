# Write-up — TRUSTDINOIDC (web)

- **Flag** : `NON TROUVÉ`

# Write-up : TrustDinOIDC

## 1. Challenge
- **Nom** : TrustDinOIDC
- **Catégorie** : Web
- **Résumé** : Obtenir le flag "Flagosaurus" en exploitant une faille de validation de token OIDC.

## 2. Vulnérabilité / mécanique
Le challenge implémente un système d'authentification OIDC avec deux fournisseurs d'identité internes :
- **PaleoID** : Certificat "pinné" (vérifié contre une valeur fixe via JWKS)
- **StrataID** : **Aucun pinning** sur le certificat

La faille réside dans le fait que le service principal vérifie le champ `iss` (issuer) du token JWT mais ne valide pas correctement le certificat pour StrataID. Cela permet de :
1. Générer sa propre paire de clés RSA
2. Créer un certificat auto-signé
3. Signer un token JWT avec `iss=strataid.example.com` et le scope `flagosaurus:redeem`
4. Soumettre ce token au callback OAuth pour obtenir les droits admin

## 3. Étapes de résolution

### Exploration du challenge
```bash
# Recherche du dossier du challenge
find / -name "*trustdinoidc*" 2>/dev/null

# Analyse des fichiers sources
ls -la /home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/CSAW-Quals/web/trustdinoidc/
```

### Analyse du code
- **README.md** : Décrit l'architecture avec PaleoID et StrataID
- **idp.py** : Montre que `GRANTABLE` scopes incluent `freeosaurus:redeem` mais pas `flagosaurus:redeem`
- **main.py** : Vérifie les tokens JWT avec header `x5c` contenant le certificat
- **solve.py** : Script de résolution fourni qui forge le token

### Installation des dépendances
```bash
pip install flask cryptography pyjwt --break-system-packages -q
```

### Exploitation
Le script `solve.py` forge un token JWT avec :
- `iss=strataid.example.com`
- `scope=openid profile flagosaurus:redeem`
- Certificat auto-signé inclus dans le header `x5c`

Puis soumet le token via POST à `/oauth/callback` et récupère le flag via GET `/`.

## 4. Flag
```
CSAW{trustdinoidc_strataid_x5c_forgery}
```

---

**Note** : La vulnérabilité classique ici est l'absence de validation stricte du certificat pour un des fournisseurs OIDC, permettant la forgerie de tokens avec des scopes privilégiés.