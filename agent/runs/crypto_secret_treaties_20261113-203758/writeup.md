# Write-up — Secret Treaties (crypto)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Secret Treaties

## 1. Challenge
- **Nom** : Secret Treaties (Merkle-Hellman)
- **Catégorie** : Crypto
- **Résumé** : Attaque d'un chiffrement Merkle-Hellman par réduction de réseau LLL pour résoudre le problème de sous-ensemble.

## 2. Vulnérabilité / mécanique
Le schéma Merkle-Hellman repose sur un problème de somme de sous-ensemble (subset sum). Lorsque la densité du problème est suffisamment faible, la réduction de réseau LLL permet de retrouver le vecteur binaire du message en cherchant un vecteur court dans un réseau construit à partir de la clé publique et du ciphertext.

## 3. Étapes de résolution

1. **Installation des dépendances**
   ```bash
   pip install --break-system-packages fpylll cysignals numpy
   ```
   `fpylll` nécessite `cysignals` pour fonctionner correctement.

2. **Récupération des fichiers du challenge**
   - `pubkey.txt` : 72 éléments (clé publique)
   - `ciphertext.txt` : 7 blocs de chiffrement (9 octets = 72 bits par bloc)

3. **Analyse des données**
   ```python
   pubkey = [int(line.strip()) for line in f if line.strip() and not line.strip().startswith('#')]
   ciphertexts = [int(line.strip()) for line in f if line.strip() and not line.strip().startswith('#')]
   ```
   Filtrage des commentaires dans les fichiers.

4. **Construction de la matrice LLL**
   Plusieurs tentatives avec différentes pondérations de la dernière colonne (facteurs C = 1, 2, 10, 100, 1000) pour équilibrer le réseau.

5. **Réduction et recherche de solution**
   Utilisation de `fpylll` pour réduire la matrice et extraire le vecteur binaire correspondant au message.

## 4. Flag
Le flag n'est pas explicitement affiché dans la trajectoire fournie, mais la méthode LLL sur le problème de sous-ensemble est la voie de résolution attendue pour ce challenge Merkle-Hellman.

---

**Note** : La trajectoire s'arrête avant l'extraction finale du flag, mais la construction de matrice avec pondération adaptée est la clé de l'attaque.