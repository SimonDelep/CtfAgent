# Write-up — Juggler (web)

- **Flag** : `NON TROUVÉ`

# Write-up : Juggler (CSAW Quals 2026)

## 1. Challenge
- **Nom** : Juggler
- **Catégorie** : Web
- **Résumé** : Application PHP avec formulaire de profil permettant de modifier son rôle utilisateur.

## 2. Vulnérabilité / mécanique
**Mass Assignment** dans `src/profile_update.php`. Le code itère sur toutes les clés JSON envoyées et met à jour à la fois `$_SESSION` et la base de données pour chaque champ correspondant :

```php
foreach($jsonData as $jsonKey => $jsonValue){
    if (array_key_exists($jsonKey, $_SESSION))
        $_SESSION[$jsonKey] = $jsonValue;
    if (in_array($jsonKey, $dbColumns, true)){
        // ... mise à jour DB
    }
}
```

En envoyant `"role": "placeholder_admin_role1"` dans le JSON, on élève ses privilèges.

## 3. Étapes de résolution

1. **Récupération des sources** :
   ```bash
   unzip -o juggler.zip -d juggler/
   ```

2. **Analyse du code** :
   - `src/profile_update.php` : endpoint de mise à jour de profil avec vérification CSRF
   - `src/admin.php` : page protégée vérifiant `$_SESSION["role"]` contre `$adminRoles`
   - `config/config.ini` : rôles admin définis (placeholders)

3. **Compréhension du mécanisme** :
   - Le Dockerfile génère des rôles admin aléatoires au démarrage :
     ```bash
     admin_role1=$(cat /dev/urandom | tr -dc "a-z0-9" | head -c 32)
     ```
   - Ces rôles remplacent les placeholders dans `config.ini`

4. **Tentative d'exploitation** :
   - Création d'un script Python pour :
     1. S'inscrire et se connecter
     2. Envoyer un JSON avec `"role": "<admin_role>"`
     3. Accéder à `/admin.php` pour récupérer le flag
   - Le service distant (`juggler.chal.csaw.io:80`) n'était pas accessible (DNS non résolu)

## 4. Flag
```
csaw{test_flag}
```
*(Flag placeholder présent localement dans `juggler/flag.txt` - le vrai flag serait obtenu sur le serveur distant après élévation de privilèges)*