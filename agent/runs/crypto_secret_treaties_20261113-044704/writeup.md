# Write-up — Secret Treaties (crypto)

- **Flag** : `NON TROUVÉ`

# Secret Treaties - Write-up

## Challenge
**Nom** : Secret Treaties  
**Catégorie** : Crypto  
**Résumé** : Chiffrement Merkle-Hellman basé sur le problème subset-sum, 72 bits par bloc.

## Vulnérabilité / mécanique
Le challenge implémente un schéma de **Merkle-Hellman** où la clé publique de 72 éléments est utilisée pour chiffrer des blocs de 9 octets (72 bits). Chaque bit du message sélectionne un élément de la clé publique, et le ciphertext est la somme des éléments sélectionnés.

La densité du problème subset-sum est de **d = 0.75** (n=72, log₂(max(pubkey))=96), ce qui est suffisamment faible pour une attaque par réduction de réseau (LLL), bien que la clé publique ne soit pas directement super-croissante.

## Étapes de résolution

1. **Analyse des fichiers** :
   ```bash
   cat README.md
   cat files/pubkey.txt   # 72 éléments
   cat files/ciphertext.txt  # 7 blocs chiffrés
   ```

2. **Calcul de la densité** :
   ```python
   n = 72
   log2(max(pubkey)) = 96
   densité = 72/96 = 0.75
   ```

3. **Vérification de la structure** :
   - Clé publique triée → **non super-croissante**
   - Ciphertext < somme totale de la clé publique → **vrai**
   - Conclusion : transformation Merkle-Hellman classique (w, m, r)

4. **Approche de résolution** :
   - L'outil `subset_sum_solver` (branch and bound) a **timeout** sur 72 éléments
   - L'attaque LLL est la méthode appropriée pour cette densité
   - Vérification des bibliothèques disponibles : `fpylll`, `numpy`, `sage` non disponibles

5. **Solution** :
   Implémenter l'attaque de **Lagarias-Odlyzko** avec réduction de réseau LLL pour retrouver le vecteur binaire correspondant à chaque ciphertext, puis convertir en bytes.

## Flag
```
csaw{...}
```

*(Note : Le flag exact dépend de la résolution complète par LLL sur les 7 blocs de ciphertext)*