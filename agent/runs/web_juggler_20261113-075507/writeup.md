# Write-up — Juggler (web)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Juggler

## 1. Challenge
*   **Nom :** Juggler
*   **Catégorie :** Web
*   **Résumé :** Escalade de privilèges via une manipulation de session non sécurisée dans une application PHP.

## 2. Vulnérabilité / mécanique
La faille réside dans le fichier `src/profile_update.php`. Ce script accepte des données JSON et met à jour dynamiquement les variables de session (`$_SESSION`) en fonction des clés reçues dans le JSON, sans validation stricte des clés autorisées. Cela permet à un utilisateur connecté de modifier son propre rôle (`role`) dans la session pour correspondre aux rôles administrateurs définis dans `config/config.ini`.

## 3. Étapes de résolution
1.  **Extraction de l'archive :** Décompression de `juggler.zip` pour accéder aux fichiers sources (`public/`, `src/`, `config/`).
2.  **Analyse de la configuration :** Lecture de `config/config.ini` révélant les rôles administrateurs (`placeholder_admin_role1`, `placeholder_admin_role2`) et la structure de la base de données SQLite.
3.  **Identification de la faille :** Analyse de `src/profile_update.php` montrant que la boucle de mise à jour applique n'importe quelle clé JSON à `$_SESSION` (`$_SESSION[$jsonKey] = $jsonValue`).
4.  **Vérification de l'accès :** Examen de `public/admin.php` confirmant que l'accès au panneau admin dépend de la présence de `$_SESSION["role"]` dans la liste des rôles admin.
5.  **Analyse du déploiement :** Lecture du `Dockerfile` montrant que les rôles admin sont générés aléatoirement au démarrage, nécessitant une injection précise du rôle dans la session pour contourner la vérification.
6.  **Test réseau :** Tentative de connexion au service distant (`curl juggler.chal.csaw.io`) échouée (résolution DNS), confirmant la nécessité d'une analyse statique approfondie.

## 4. Flag
`csaw{test_flag}` *(Note : Flag présent dans `flag.txt` lors de l'analyse initiale, le flag réel étant généré dynamiquement dans le panneau admin une fois le rôle injecté)*.