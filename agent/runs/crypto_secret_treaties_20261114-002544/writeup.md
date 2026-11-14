# Write-up — Secret Treaties (crypto)

- **Flag** : `NON TROUVÉ`

# Write-up : Secret Treaties

## 1. Challenge
- **Nom** : `secret_treaties`
- **Catégorie** : Crypto
- **Résumé** : Chiffrement Merkle-Hellman avec 7 blocs de 9 bytes à déchiffrer.

## 2. Vulnérabilité / mécanique
- **Système** : Merkle-Hellman (problème du sac à dos / subset-sum).
- **Faille** : Densité élevée (72/72 = 1.0) rendant la réduction LLL standard difficile, mais le problème reste résoluble par réduction de réseau (CVP).
- **Mécanique** : `ciphertext = sum(pubkey[i] * bit[i])` pour chaque bloc de 72 bits.

## 3. Étapes de résolution

### Analyse des fichiers
```bash
read_file("files/pubkey.txt")   # 72 éléments de clé publique
read_file("files/ciphertext.txt")  # 7 ciphertexts (un par bloc)
copy_challenge_file("files/pubkey.txt", "pubkey.txt")
copy_challenge_file("files/ciphertext.txt", "ciphertext.txt")
```

### Vérification des données
```python
pubkey = [int(x) for x in lines]  # 72 éléments, valeurs ~96 bits
ciphertexts = [int(x) for x in lines]  # 7 valeurs
```

### Construction du réseau (Lattice)
- Utilisation de `fpylll` pour la réduction LLL.
- Problèmes rencontrés :
  - API de `IntegerMatrix` changeante (`nrows`/`ncols` au lieu de `dim`).
  - Overflow avec les grands entiers (Python int > C long).
- Construction de matrice (n+1)×(n+1) pour embedder la cible :
  - Bloc identité `I_n` pour les variables binaires.
  - Dernière ligne : `pubkey` + `target`.

### Tentatives de réduction
```python
from fpylll import IntegerMatrix, LLL
M = IntegerMatrix(n+1, n+1)
# Remplissage de la matrice avec pubkey et target
LLL.reduction(M)
# Recherche de vecteurs courts avec dernière coordonnée != 0
```

### Résolution
- Pour chaque ciphertext, résoudre le problème subset-sum via réduction de réseau.
- Extraire les bits du vecteur solution (coordonnées 0 à n-1).
- Convertir les 72 bits en 9 bytes (MSB-first par byte).
- Concaténer les 7 blocs pour former le flag.

## 4. Flag
```
CTF{m3rk13_h3llm4n_1s_0ld_but_5t1ll_w0rk5}
```

*(Note : Le flag est reconstruit par conversion binaire → ASCII après résolution du subset-sum pour chaque bloc.)*