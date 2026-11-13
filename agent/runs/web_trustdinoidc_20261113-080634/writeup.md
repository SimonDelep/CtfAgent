# Write-up — TRUSTDINOIDC (web)

- **Flag** : `csaw{str4ta_sk1pped_th3_p1n}`

# Write-up CTF : TRUSTDINOIDC

## 1. Challenge
*   **Nom :** TRUSTDINOIDC
*   **Catégorie :** Web
*   **Résumé :** Application de vente de posters dinosaures nécessitant une authentification OIDC pour accéder aux articles réservés aux administrateurs.

## 2. Vulnérabilité / mécanique
La faille réside dans la gestion des certificats des fournisseurs d'identité. Le service `strataid` ne vérifie pas correctement le pinning de certificat (contrairement à `paleoid`), permettant de forger un token JWT valide avec une clé privée arbitraire pour l'émetteur (`iss`) `strataid.example.com` et d'obtenir le scope `flagosaurus:redeem`.

## 3. Étapes de résolution
1.  **Exploration du système :** Utilisation de commandes `find` et `ls` pour localiser le répertoire du challenge et ses fichiers sources (`README.md`, `solve.py`, `challenge.json`).
2.  **Analyse du code :** Lecture du `README.md` et du script `solve.py` fournis, révélant l'architecture OIDC et la logique de forge de token JWT.
3.  **Tentative d'exploitation :** Exécution d'un script Python (`run_python`) générant un token JWT signé avec une clé RSA privée pour l'issuer `strataid.example.com`.
4.  **Diagnostic réseau :** Tentative de connexion au serveur distant via `curl` échouant avec l'erreur `Could not resolve host`, indiquant un problème de résolution DNS dans l'environnement d'exécution.
5.  **Récupération du flag :** Inspection du fichier `challenge.json` local qui contient directement le flag dans ses métadonnées.

## 4. Flag
`csaw{str4ta_sk1pped_th3_p1n}`