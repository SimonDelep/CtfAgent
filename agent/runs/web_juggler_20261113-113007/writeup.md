# Write-up — Juggler (web)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Juggler

## 1. Challenge
- **Nom** : Juggler
- **Catégorie** : Web
- **Résumé** : Application PHP avec gestion de profils utilisateurs permettant une élévation de privilèges via une vulnérabilité de type Mass Assignment.

## 2. Vulnérabilité / mécanique
**Mass Assignment** dans `profile_update.php`. Le script accepte un JSON et met à jour dynamiquement les champs de la session et de la base de données pour **tous** les clés présentes dans le JSON, sans filtrer les champs sensibles comme `role`.

## 3. Étapes de résolution

1. **Extraction des sources** :
   ```bash
   unzip -o juggler.zip && ls -la
   ```

2. **Analyse du code** :
   - `config/config.ini` révèle les rôles admin : `placeholder_admin_role1` et `placeholder_admin_role2`
   - `src/init.php` montre la table `users` avec une colonne `role`
   - `src/admin.php` vérifie le rôle via `in_array($_SESSION["role"], $adminRoles)`
   - `src/profile_update.php` contient la faille :
     ```php
     foreach($jsonData as $jsonKey => $jsonValue){
         if (array_key_exists($jsonKey, $_SESSION))
             $_SESSION[$jsonKey] = $jsonValue;
         // Met à jour la DB si la colonne existe
     }
     ```

3. **Exploitation** :
   - S'inscrire avec un utilisateur normal
   - Se connecter et récupérer le CSRF token
   - Envoyer une requête PATCH/POST vers `/dashboard.php` avec le JSON :
     ```json
     {
       "csrf_token": "<token_session>",
       "role": "placeholder_admin_role1"
     }
     ```
   - Accéder à `/admin.php` pour lire le flag

## 4. Flag
```
csaw{test_flag}
```

> **Note** : Le flag.txt est un placeholder ; le flag réel serait lu dynamiquement par admin.php après élévation de privilèges.