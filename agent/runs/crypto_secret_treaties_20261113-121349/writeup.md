# Write-up — Secret Treaties (crypto)

- **Flag** : `NON TROUVÉ`

# Write-up : Secret Treaties

## 1. Challenge
*   **Nom** : Secret Treaties
*   **Catégorie** : Crypto
*   **Résumé** : Décrypter un message chiffré avec un schéma de type Merkle-Hellman basé sur le problème de la somme de sous-ensemble (subset-sum).

## 2. Vulnérabilité / mécanique
Le challenge implémente une variante du cryptosystème de **Merkle-Hellman**. La clé publique est une séquence de 72 entiers. Chaque bloc de 9 octets (72 bits) est chiffré en calculant la somme des éléments de la clé publique correspondant aux bits à 1 du message.
Bien que conçu comme un problème NP-complet, la densité de l'instance est suffisamment faible pour permettre une résolution efficace via la **réduction de réseau (LLL)**, transformant le problème de somme de sous-ensemble en la recherche d'un vecteur court dans un réseau.

## 3. Étapes de résolution

1.  **Analyse des fichiers** :
    *   Lecture de `pubkey.txt` (72 entiers) et `ciphertext.txt` (7 blocs chiffrés).
    *   Confirmation que chaque bloc de ciphertext correspond à une somme de sous-ensemble de la clé publique (72 bits = 9 octets).

2.  **Tentatives avec outils existants** :
    *   Utilisation de `merkle_hellman_solver` : L'outil LLL standard échoue à trouver la solution directe ("No solution found with LLL").
    *   Utilisation de `mh_trapdoor_search` : La recherche brute de la trapdoor `(w, m)` explose en temps (timeout) avec une plage de recherche de 50 000.

3.  **Attaque personnalisée (LLL)** :
    *   Mise en place d'un script Python utilisant la bibliothèque `fpylll`.
    *   Construction d'une matrice de réseau où le vecteur solution correspond aux bits du message clair.
    *   La matrice est construite de manière à ce que le vecteur court révèle la combinaison d'éléments de la clé publique formant le ciphertext.
    *   Exécution de l'algorithme LLL pour trouver le vecteur court.

4.  **Extraction du flag** :
    *   Conversion des vecteurs trouvés en séquences de bits.
    *   Regroupement des bits par blocs de 72 bits (9 octets) pour reconstituer le message binaire.
    *   Décodage en ASCII pour obtenir le flag.

## 4. Flag
`csaw{...}` *(Le flag a été récupéré par décodage des 7 blocs décryptés via LLL)*