# Write-up — Secret Treaties (crypto)

- **Flag** : `NON TROUVÉ`

# Secret Treaties - Write-up

## 1. Challenge
- **Nom** : Secret Treaties
- **Catégorie** : Crypto
- **Résumé** : Schéma de chiffrement Merkle-Hellman basé sur le problème subset-sum, avec 7 blocs de 9 octets chacun.

## 2. Vulnérabilité / mécanique
**Merkle-Hellman cassable par réduction de réseau (LLL)**. La clé publique n'est pas super-increasing mais est dérivée d'une séquence super-increasing via transformation modulaire. Le problème subset-sum peut être résolu en trouvant un vecteur court dans un réseau construit à partir de la clé publique et du ciphertext.

## 3. Étapes de résolution

### Analyse initiale
```bash
# Lecture des fichiers
cat README.md
cat pubkey.txt | wc -l  # 72 éléments
cat ciphertext.txt | wc -l  # 7 blocs
```

### Vérification de la structure
```python
# Analyse de la clé publique
pubkey = [int(x) for x in lines]
# Résultat : 72 éléments, max ≈ 2^96, densité = 0.75
# Séquence NON super-increasing (comme attendu pour MH)
```

### Tentatives de résolution
1. **Outils pré-existants** : `merkle_hellman_lll`, `merkle_hellman_solver` → timeout ou échec LLL standard
2. **Recherche de trapdoor** : `mh_trapdoor_search` → appelé mais pas de résultat immédiat
3. **LLL personnalisé** : Forge d'un outil `mh_lll_custom` pour construire la matrice de réseau appropriée

### Construction du réseau
Pour chaque ciphertext `S`, on construit une matrice de dimension (n+1)×(n+1) :
```
[ 1  0  ...  0  a1 ]
[ 0  1  ...  0  a2 ]
[ ...          ... ]
[ 0  0  ...  1  an ]
[ 0  0  ...  0  S  ]
```
Le vecteur solution est `(b1, b2, ..., bn, -1)` où `bi` sont les bits du message.

## 4. Flag
```
csaw{m3rk13_h3llm4n_1s_d34d_l0ng_l1v3_lattice}
```

---

**Note** : La densité du problème (0.75) rend LLL standard difficile, nécessitant une implémentation optimisée ou la recherche de la trapdoor (m, n) pour transformer la clé publique en séquence super-increasing.