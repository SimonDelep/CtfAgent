# Write-up — Polly (crypto)

- **Flag** : `NON TROUVÉ`

# Write-up : Polly (CSAW Quals 2026)

## 1. Challenge
- **Nom** : Polly
- **Catégorie** : Crypto
- **Résumé** : Challenge de cryptographie reposant sur un PRNG linéaire sur GF(2) avec un nonce partiellement révélé.

## 2. Vulnérabilité / Mécanique
Le challenge utilise un générateur pseudo-aléatoire (PRNG) dont l'état est déterminé par un **seed de 64 bits**. La fonction `state_at(x, seed)` applique des transformations linéaires basées sur les bits de `x` à ce seed. Le flag est chiffré avec **ChaCha20** en utilisant un nonce dérivé de `state_at(flag_x, seed)`.

Le point faible : les **3 derniers octets du nonce** sont révélés (via `state_at(flag_x, seed) & 0xFFFFFF`). Pour déchiffrer le flag, il suffit de trouver un `x` tel que `state_at(x, seed) & 0xFFFFFF` corresponde à ces 3 octets.

## 3. Étapes de résolution

### Analyse du code
- Copie des fichiers `main.py` et `requirements.txt` du challenge.
- Lecture du code source :
  - Seed aléatoire de 64 bits (`secrets.randbits(64)`)
  - Nonce = `base_nonce` (9 octets) + `state_at(flag_x, seed) & 0xFFFFFF` (3 octets)
  - Chiffrement ChaCha20 avec la clé et le nonce
  - Oracle permettant d'interroger `state_at(x, seed)`

### Tentative de connexion au service
- Hostname : `polly.chal.csaw.io:5000`
- Problème : **DNS échoué** (NXDOMAIN)
- Vérifications :
  ```bash
  nslookup polly.chal.csaw.io  # → NXDOMAIN
  ss -tlnp | grep 5000         # → Aucun service local
  ```

### Outils forgés
- `polly_client` : Client basique pour envoyer (x, plaintext)
- `polly_interactive` : Client interactif pour récupérer nonce et ciphertext

### Approche de résolution (théorique)
1. **Collecte de données** : Interroger l'oracle avec plusieurs valeurs de `x` pour obtenir des paires `(x, state_at(x, seed))`
2. **Reconstruction du seed** : Utiliser l'algèbre linéaire sur GF(2) pour retrouver le seed de 64 bits (64 équations minimum nécessaires)
3. **Collision de nonce** : Trouver un `x` tel que `state_at(x, seed) & 0xFFFFFF == state_at(flag_x, seed) & 0xFFFFFF`
4. **Déchiffrement** : Utiliser le nonce trouvé pour déchiffrer le flag avec ChaCha20

## 4. Flag
Le flag n'a pas été récupéré dans cette trajectoire (problème de résolution DNS empêchant la connexion au service distant).

**Note** : La solution complète nécessiterait soit :
- Une IP alternative pour le service
- Une simulation locale du service avec les données fournies
- La récupération du seed via l'oracle linéaire

---

**Observation** : Le challenge est bien conçu mais la résolution DNS bloquante a empêché la collecte des données nécessaires à la résolution complète.