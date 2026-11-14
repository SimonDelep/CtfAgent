

---
## Résumé au tour 10 (00:31:09)

## Fait
- **Identification :** Challenge `crypto_secret_treaties` confirmé comme système Merkle-Hellman (Knapsack/Subset-Sum).
- **Données :** 72 éléments de clé publique (~96 bits), 7 blocs de ciphertext (9 octets/bloc = 72 bits).
- **Environnement :** Fichiers `pubkey.txt` et `ciphertext.txt` copiés du dossier `files/` vers le répertoire de travail.
- **Implémentation :** Script Python fonctionnel utilisant `fpylll` pour la réduction LLL sur une matrice 73x73 (embedding du ciphertext).

## Échecs / impasses
- **Densité :** Ratio 72/72 = 1.0 trop élevé pour une résolution LLL standard directe sans structure super-croissante.
- **API fpylll :** Incompatibilité initiale (attributs `.rows`, `.dim` absents), corrigé via `.nrows`/`.ncols`.
- **Résultat LLL :** Vecteurs réduits non binaires (coeffs ex: -8, 13) et composante `last` non unitaire (ex: -203, -142 au lieu de 1).
- **Chemin :** Erreur `FileNotFoundError` initiale sur `files/pubkey.txt` résolue par copie explicite.

## État actuel
- **Données chargées :** Clé publique et ciphertexts analysés et validés en mémoire.
- **Lattice :** Matrice construite et réduite, mais solution brute non trouvée (bruit dans les coefficients).
- **Problème :** La construction actuelle ne force pas la contrainte binaire (0/1) ni la valeur cible de la dernière coordonnée.
- **Outils :** `numpy` et `fpylll` opérationnels dans l'environnement Python.

## Prochaines pistes
- **Embedding :** Ajuster le poids d'embedding (embedding constant) pour forcer la dernière coordonnée à 1.
- **Structure :** Vérifier si la clé publique cache une séquence super-croissante (clé privée) plutôt qu'un subset-sum générique.
- **Algorithme :** Tester BKZ au lieu de LLL pour améliorer la qualité de la base réduite.
- **Matrice :** Réviser la construction de la matrice pour mieux contraindre la solution binaire.


---
## Résumé au tour 20 (00:35:05)

## Fait
- **Identification :** Challenge `crypto_secret_treaties` confirmé comme système Merkle-Hellman (Knapsack/Subset-Sum).
- **Données :** 72 éléments de clé publique (valeurs jusqu'à ~79 quadrillions, nécessitent précision arbitraire), 7 blocs de ciphertext (9 octets/bloc = 72 bits).
- **Environnement :** Fichiers `pubkey.txt` et `ciphertext.txt` chargés et validés en mémoire.
- **Outils :** Script Python avec `fpylll` et `numpy` opérationnels ; outil `mh_subsetsum_lll` forgé pour résoudre le subset-sum.

## Échecs / impasses
- **Densité :** Ratio 72/72 = 1.0 trop élevé pour une résolution LLL standard directe sans structure super-croissante.
- **API fpylll :** Incompatibilité initiale (attributs `.rows`, `.dim` absents), corrigé via `.nrows`/`.ncols`.
- **Résultat LLL :** Vecteurs réduits non binaires (coeffs ex: -8, 13) et composante `last` non unitaire (ex: -203, -142 au lieu de 1).
- **Module BKZ :** `fpylll.tools.bkz` non disponible (ModuleNotFoundError).
- **Outil forgé :** `mh_subsetsum_lll` créé mais chargement problématique (erreur "No module named 'mh_subsetsum_lll'").
- **Chemin :** Erreur `FileNotFoundError` initiale sur `files/pubkey.txt` résolue par copie explicite.

## État actuel
- **Données chargées :** Clé publique (72 éléments) et 7 ciphertexts analysés et validés en mémoire.
- **Lattice :** Matrice construite et réduite, mais solution brute non trouvée (bruit dans les coefficients).
- **Problème :** La construction actuelle ne force pas la contrainte binaire (0/1) ni la valeur cible de la dernière coordonnée.
- **Précision :** Valeurs de la clé publique trop grandes pour int64 standard, nécessitent entiers Python natifs.
- **Outils :** `numpy` et `fpylll` opérationnels ; outil `mh_subsetsum_lll` forgé mais à activer correctement.

## Prochaines pistes
- **Embedding :** Ajuster le poids d'embedding (embedding constant) pour forcer la dernière coordonnée à 1.
- **Structure :** Vérifier si la clé publique cache une séquence super-croissante (clé privée) plutôt qu'un subset-sum générique.
- **Algorithme :** Tester BKZ au lieu de LLL pour améliorer la qualité de la base réduite (si module disponible).
- **Matrice :** Réviser la construction de la matrice pour mieux contraindre la solution binaire.
- **Outil :** Résoudre le chargement de l'outil `mh_subsetsum_lll` (import ou appel direct via `load_tool`).


---
## Résumé au tour 30 (00:41:26)

## Fait
- **Identification :** Challenge `crypto_secret_treaties` confirmé comme système Merkle-Hellman (Knapsack/Subset-Sum).
- **Données :** 72 éléments de clé publique (valeurs ~10^28, précision arbitraire requise), 7 blocs de ciphertext (72 bits).
- **Environnement :** Fichiers `pubkey.txt` et `ciphertext.txt` copiés dans le dossier de travail et chargés avec succès en mémoire.
- **Outils :** `fpylll` et `numpy` opérationnels (API `.nrows`/`.ncols` corrigée). Nouveau outil `mh_solver_v2` forgé avec signature `main(args)` valide.

## Échecs / impasses
- **Densité :** Ratio 72/72 = 1.0 trop élevé pour une résolution LLL standard directe sans structure super-croissante.
- **Résultat LLL :** Vecteurs réduits non binaires (coeffs ex: -8, 13) et composante `last` non unitaire (ex: -203).
- **Outils :** `mh_subsetsum_lll` initial introuvable (fichier manquant vs outil système). `fpylll.tools.bkz` manquant.
- **Chemin :** Erreurs `FileNotFoundError` initiales sur `files/` résolues par copie explicite.

## État actuel
- **Données chargées :** Clé publique (72 éléments) et 7 ciphertexts analysés et validés en mémoire.
- **Lattice :** Matrice construite mais solution brute non trouvée (bruit dans les coefficients, contrainte binaire absente).
- **Outil prêt :** `mh_solver_v2` est forgé et disponible pour exécution directe sur les cibles.
- **Précision :** Valeurs de la clé publique gérées via entiers Python natifs.

## Prochaines pistes
- **Exécution :** Lancer `mh_solver_v2` sur les 7 ciphertexts pour tenter la résolution.
- **Embedding :** Ajuster le poids d'embedding (constante) pour forcer la dernière coordonnée à 1.
- **Structure :** Vérifier si la clé publique cache une séquence super-croissante (clé privée) plutôt qu'un subset-sum générique.
- **Matrice :** Réviser la construction de la matrice pour mieux contraindre la solution binaire si LLL échoue.
- **Vérification :** Convertir les vecteurs binaires potentiels en texte ASCII pour valider le drapeau.


---
## Résumé au tour 40 (00:46:40)

## Fait
- **Identification :** Challenge `crypto_secret_treaties` confirmé comme système Merkle-Hellman (Knapsack/Subset-Sum).
- **Données :** 72 éléments de clé publique (~10^28) et 7 blocs de ciphertext (72 bits) chargés avec succès.
- **Intégrité :** Données vérifiées comme entiers Python (`int`), évitant la conversion float problématique de `mh_solver_v2`.
- **Outils :** `mh_lll_solver` forgé pour gérer les entiers et `fpylll` (simplifié). `mh_solver_v2` disponible mais instable (problème de type).

## Échecs / impasses
- **Densité :** Ratio 72/72 = 1.0 trop élevé pour une résolution LLL standard directe.
- **Résultat LLL :** Vecteurs réduits non binaires (coeffs ex: -8, 13), solution brute absente.
- **Tooling :** `mh_solver_v2` échoué (floats vs ints). `mh_lll_solver` échoué au import (`ModuleNotFoundError` : chemin `forge/` manquant dans `sys.path`).
- **Libs :** `fpylll.util.lattice` introuvable, nécessité d'import simplifié.

## État actuel
- **Données :** Pubkey et ciphertexts validés en mémoire (types `int` vérifiés).
- **Lattice :** Matrice construite une fois, échec de détection de vecteur binaire.
- **Outil prêt :** `mh_lll_solver` existe dans `forge/`, nécessite correction du `sys.path` pour exécution.
- **Environnement :** Dossier de travail actif `crypto_secret_treaties_...`, fichiers sources accessibles.

## Prochaines pistes
- **Import :** Corriger `sys.path` pour importer `mh_lll_solver` depuis le dossier `forge/`.
- **Exécution :** Relancer la résolution sur les 7 ciphertexts avec l'outil corrigé.
- **Matrice :** Ajuster la constante d'embedding (C) pour forcer la dernière coordonnée à 1.
- **Validation :** Convertir les vecteurs binaires potentiels en texte ASCII pour valider le drapeau.
- **Alternative :** Si échec, vérifier si la clé publique cache une séquence super-croissante (clé privée).
