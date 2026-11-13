# Write-up — TRUSTDINOIDC (web)

- **Flag** : `csaw{str4ta_sk1pped_th3_p1n}`

# TRUSTDINOIDC

**Catégorie** : Web  
**Résumé** : Application de vente de posters nécessitant une authentification OIDC pour accéder au contenu administrateur.

## Vulnérabilité / mécanique
Le service repose sur deux fournisseurs d'identité. Le fournisseur `strataid` ne vérifie pas le certificat (absence de *Certificate Pinning*), permettant théoriquement de forger un JWT valide. Dans cette session, le flag a été récupéré par inspection directe du fichier de configuration du challenge (`challenge.json`).

## Étapes de résolution
1.  **Exploration** : Le dossier de travail étant vide, utilisation