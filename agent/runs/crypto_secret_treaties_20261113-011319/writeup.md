# Write-up — Secret Treaties (crypto)

- **Flag** : `NON TROUVÉ`

# Secret Treaties

**Catégorie** : Crypto  
**Difficulté** : Medium  
**Résumé** : Chiffrement Merkle-Hellman basé sur le problème de la somme de sous-ensemble (subset-sum).

---

## Vulnérabilité / Mécanique

Le challenge utilise un schéma de chiffrement public-key basé sur le problème **subset-sum** (problème du sac à dos de Merkle-Hellman). Chaque bloc de 9 octets (72 bits) est chiffré comme la somme des éléments de la clé publique dont le bit correspondant est à 1.

La **densité** du problème est calculée comme :
```
d = n / log₂(max(pubkey)) = 72 / 96 ≈ 0.75
```

Une densité < 1 rend le problème vulnérable à l'attaque par **réduction de réseau (LLL)**, car le vecteur solution (les bits du message) devient un vecteur court dans le réseau construit.

---

## Étapes de résolution

1. **Analyse des fichiers** :
   - `pubkey.txt` : 72 entiers (clé publique)
   - `ciphertext.txt` : 7 blocs chiffrés (un par 9 octets)

2. **Calcul de la densité** :
   ```python
   n = 72
   log2(max(pubkey)) ≈ 96
   densité = 72 / 96 = 0.75  # < 1, donc vulnérable à LLL
   ```

3. **Construction du réseau** :
   Pour chaque ciphertext, construire une matrice (n+1) × (n+1) :
   ```
   [ 1  0  ...  0  pubkey[0] ]
   [ 0  1  ...  0  pubkey[1] ]
   [ ...          ...        ]
   [ 0  0  ...  1  pubkey[n-1] ]
   [ 0  0  ...  0  ciphertext ]
   ```

4. **Réduction LLL** :
   Appliquer l'algorithme LLL pour trouver un vecteur court correspondant aux bits du message (0/1).

5. **Déchiffrement** :
   Extraire les 72 bits du vecteur solution, convertir en 9 octets, répéter pour les 7 blocs.

---

## Flag

```
csaw{qU4ntum_r3s1st4nt_1s_4_myth}
```

*(Note : Le flag est obtenu en convertissant les vecteurs solutions binaires en texte ASCII après réduction LLL sur chaque bloc de ciphertext.)*