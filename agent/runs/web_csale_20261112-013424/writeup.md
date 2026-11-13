# Write-up — CSALE (web)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : CSALE

## 1. Challenge
- **Nom** : csale
- **Catégorie** : Web
- **Résumé** : Marketplace Flask avec système de chiffrement de mot de passe vulnérable

## 2. Vulnérabilité / mécanique
La faille réside dans le module `vault.py` qui implémente un chiffrement de mot de passe via **XOR avec clé répétitive**. La fonction `encrypt_password()` utilise une clé de récupération (`recovery_key`) générée aléatoirement (20 chiffres) mais réutilisée pour le XOR, ce qui permet une attaque de type **known-plaintext** si le format du mot de passe est connu.

```python
def xor_with_repeating_key(data, recovery_key):
    key_bytes = recovery_key.encode()
    return bytes(
        byte ^ key_bytes[index % len(key_bytes)]
        for index, byte in enumerate(data)
    )
```

## 3. Étapes de résolution

| Étape | Action | Commande/Outil |
|-------|--------|----------------|
| 1 | Vérification du service | `curl -s http://csale.chal.csaw.io:5000/` (échec : host not found) |
| 2 | Recherche des fichiers sources | `find / -name "player.zip" 2>/dev/null` |
| 3 | Extraction de l'archive | `unzip -o player.zip` |
| 4 | Analyse du code | `read_file player/main.py` et `read_file player/vault.py` |
| 5 | Identification de la vulnérabilité | Lecture de `vault.py` : XOR avec clé répétitive de 20 caractères |

## 4. Flag
**Note** : La trajectoire s'arrête durant l'analyse du code. Le flag n'a pas été récupéré dans cet historique, mais la voie d'exploitation identifiée est :
- Exploiter le XOR réutilisable avec une attaque known-plaintext sur le mot de passe
- Récupérer la `recovery_key` en connaissant une partie du plaintext

```
CSAW{...}  # (à compléter après exploitation complète)
```

---

**Observation** : Le challenge présente une faille classique de chiffrement XOR avec clé répétitive. La clé de 20 chiffres générée avec `secrets.choice(string.digits)` est prévisible si un mot de passe connu est disponible.