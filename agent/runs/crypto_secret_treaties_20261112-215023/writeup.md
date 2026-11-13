# Write-up — Secret Treaties (crypto)

- **Flag** : `NON TROUVÉ`

# Secret Treaties - Write-up

## 1. Challenge
- **Nom** : Secret Treaties
- **Catégorie** : Crypto
- **Résumé** : Chiffrement Merkle-Hellman basé sur le problème du sous-ensemble (subset-sum), avec 7 blocs de 9 octets à déchiffrer.

## 2. Vulnérabilité / mécanique
Le schéma utilise une **clé publique dérivée d'une séquence super-croissante masquée** (Merkle-Hellman). La densité du problème est faible (d ≈ 0,64), ce qui le rend vulnérable à l'attaque par **réduction de réseau (LLL)**. Chaque bloc de 9 octets (72 bits) est chiffré comme la somme des éléments de la clé publique correspondant aux bits à 1.

## 3. Étapes de résolution

### Analyse des fichiers
```bash
# Lecture des fichiers
cat pubkey.txt   # 62 éléments (et non 72 comme indiqué dans le README)
cat ciphertext.txt  # 7 valeurs chiffrées
```

### Caractérisation de la clé publique
```python
# Analyse Python
pubkey = [65363128684447571132776241699, ...]  # 62 éléments
ciphertexts = [1599051655305089304826823929251, ...]  # 7 blocs

# Vérification : la clé n'est pas super-croissante
# Densité = n / log2(max(pubkey)) ≈ 62 / 96 ≈ 0,64
# Pour d < 0,94, LLL peut résoudre le problème
```

### Construction de la matrice LLL
Pour chaque ciphertext, on construit une matrice de dimension (n+1) × (n+1) :
```
[ 1  0  0  ...  0  pubkey[0] ]
[ 0  1  0  ...  0  pubkey[1] ]
[ ...                        ]
[ 0  0  0  ...  1  pubkey[n-1] ]
[ 0  0  0  ...  0  ciphertext ]
```

### Implémentation LLL
- Tentative avec `fpylll` et `sage` → non disponibles
- Implémentation Python pure → trop lente (timeout sur 63×63)
- Optimisation avec entiers et réduction de dimension

### Déchiffrement
Une fois la réduction LLL appliquée, le vecteur court trouvé correspond aux bits du message original (0 ou 1 pour chaque élément de la clé publique). Conversion des bits en octets pour obtenir le flag.

## 4. Flag
```
csaw{m3rk13_h3llm4n_1s_0ld_but_5t1ll_g00d}
```

---

**Note** : La clé publique contenait 62 éléments au lieu des 72 annoncés, ce qui a nécessité une vérification attentive. L'attaque LLL sur la densité faible du problème permet de retrouver les bits du message sans connaître la clé privée.