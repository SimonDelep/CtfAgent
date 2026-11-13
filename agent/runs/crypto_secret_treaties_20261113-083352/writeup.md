# Write-up — Secret Treaties (crypto)

- **Flag** : `NON TROUVÉ`

# Write-up : Secret Treaties

## 1. Challenge
*   **Nom** : Secret Treaties
*   **Catégorie** : Crypto
*   **Résumé** : Décrypter un message chiffré avec un schéma de clé publique basé sur le problème de la somme de sous-ensemble (Merkle-Hellman).

## 2. Vulnérabilité / mécanique
Le challenge utilise le cryptosystème **Merkle-Hellman**. La clé publique fournie (`pubkey.txt`) est une séquence de 72 entiers, dérivée d'une séquence super-croissante secrète via une transformation modulaire `(s[i] * w) mod m`. La faiblesse réside dans la possibilité de retrouver la **trapdoor** `(w, m)` pour inverser la transformation et obtenir la séquence super-croissante originale, permettant de résoudre le problème de somme de sous-ensemble (subset-sum) de manière triviale pour chaque bloc de 9 octets (72 bits).

## 3. Étapes de résolution
1.  **Analyse des fichiers** :
    *   Lecture du `README.md` : confirmation du format (9 octets par bloc, 72 bits, somme des éléments de la clé publique correspondant aux bits à 1).
    *   Lecture de `pubkey.txt` : 72 éléments entiers.
    *   Lecture de `ciphertext.txt` : 7 valeurs chiffrées (un par bloc).

2.  **Identification du schéma** :
    *   Reconnaissance du problème Merkle-Hellman (Knapsack).
    *   Vérification que la clé publique n'est pas directement super-croissante.

3.  **Tentatives de résolution** :
    *   Utilisation de l'outil `merkle_hellman_solver` : échec avec LLL standard (densité trop élevée ou entiers trop grands pour la réduction de réseau directe).
    *   Tentative avec `merkle_hellman_lll` : timeout (trop lent sur ces grands entiers).

4.  **Recherche de la trapdoor** :
    *   Conception d'un outil personnalisé `mh_decryptor` pour rechercher les paramètres `(w, m)`.
    *   L'algorithme teste des valeurs de `m` et calcule `w` (inverse modulaire) pour vérifier si la séquence résultante `s[i] = (pub[i] * w^-1) mod m` est super-croissante.
    *   Exécution de l'outil avec une recherche bornée (`max_m_search=100000`).

5.  **Décryptage** :
    *   Une fois la trapdoor trouvée, chaque ciphertext est résolu par une recherche