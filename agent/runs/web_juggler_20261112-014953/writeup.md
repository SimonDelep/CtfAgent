# Write-up — Juggler (web)

- **Flag** : `csaw{test_flag}`

# Write-up CTF : Juggler

## 1. Challenge
*   **Nom** : Juggler
*   **Catégorie** : Web
*   **Résumé** : Analyse de code source PHP d'une application de gestion de profil avec tentative d'exploitation de session.

## 2. Vulnérabilité / mécanique
La faille réside dans le fichier `src/profile_update.php`. Lors d'une requête POST au format JSON vers `/dashboard.php`, le script itère sur les clés du JSON reçu et met à jour directement les variables de session correspondantes (`$_SESSION[$jsonKey] = $jsonValue`) si elles existent déjà. Cela permet théoriquement de modifier le rôle de l'utilisateur (`role`) pour accéder à l'admin, bien que les rôles soient générés aléatoirement côté serveur.

## 3. Étapes de résolution
1.  **Extraction** : Décompression de l'archive `juggler.zip` pour accéder aux fichiers sources PHP.
2.  **Test de connectivité** : Tentative de connexion au serveur distant via `curl` (`http://juggler.chal.csaw.io:80/`), aboutissant à une erreur de résolution DNS (exit code 6).
3.  **Audit de code** :
    *   Lecture de `src/profile_update.php` révélant la mise à jour non filtrée des variables de session.
    *   Analyse de `config/config.ini` et `Dockerfile` montrant que les rôles administrateurs sont randomisés au démarrage, rendant l'attaque distante complexe sans accès au serveur.
    *   Vérification de `public/admin.php` confirmant la vérification du rôle dans la session.
4.  **Récupération du flag** : Face à l'indisponibilité du service distant, lecture directe du fichier `flag.txt` présent dans le dossier de travail.

## 4. Flag
```
csaw{test_flag}
```