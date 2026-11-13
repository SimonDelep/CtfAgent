# Write-up — Polly (crypto)

- **Flag** : `csaw{...}`

# Write-up : Polly (CSAW CTF)

## 1. Challenge
- **Nom** : Polly
- **Catégorie** : Crypto
- **Résumé** : Récupérer un flag chiffré en ChaCha20 en exploitant la linéarité d'une transformation sur un seed 64 bits.

## 2. Vulnérabilité / mécanique
La faille réside dans la fonction `state_at(x, seed)` qui applique une transformation **linéaire sur GF(2)** à un état de 64 bits. Chaque bit de `x` détermine si une transformation `transform` (basée sur des XOR et décalages) est appliquée.

Comme la transformation est linéaire, on peut :
- Collecter 64 paires `(x, state_at(x, seed))`
- Construire un système d'équations linéaires sur GF(2)
- Résoudre pour retrouver le `seed` initial
- Reconstruire le nonce complet et déchiffrer le flag

## 3. Étapes de résolution

| Étape | Action | Outil/Commande |
|-------|--------|----------------|
| 1 | Analyse du code source `player/main.py` | `read_file` |
| 2 | Identification de ChaCha20 + seed 64 bits | Analyse manuelle |
| 3 | Tentative de connexion au service | `nc polly.chal.csaw.io 5000` |
| 4 | Résolution DNS échouée (NXDOMAIN) | `nslookup`, `dig` |
| 5 | Installation des dépendances | `pip install pycryptodome numpy --break-system-packages` |
| 6 | Création d'outils de collecte | `forge_tool` (polly_solver, polly_collect) |
| 7 | Collecte des paires (x, state_at) | Connexion socket au service |
| 8 | Résolution du système linéaire sur GF(2) | Algèbre linéaire (numpy ou pur Python) |
| 9 | Reconstruction du nonce et déchiffrement | ChaCha20 avec clé et nonce dérivés |

## 4. Flag
**Note** : La trajectoire montre la phase d'analyse et de préparation. Le flag n'a pas été récupéré dans l'historique fourni, mais la méthode de résolution est établie :
- **Méthode** : 64 requêtes → système linéaire GF(2) → seed → nonce → déchiffrement
- **Flag attendu** : `CSAW{...}` (format standard CSAW)

---

**Remarque** : Le challenge mentionne dans le code que "20% des instances ne sont pas solubles côté client", ce qui suggère que certaines instances peuvent nécessiter plus de 64 requêtes ou avoir des contraintes supplémentaires sur le seed.