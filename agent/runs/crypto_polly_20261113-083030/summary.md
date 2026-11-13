

---
## Résumé au tour 10 (08:32:12)

## Fait (actions utiles et ce qu'elles ont donné)
- **Exploration système :** Navigation dans `/home/etudiantelambda/Documents/...` pour localiser les fichiers du challenge (`crypto/polly/player/main.py`).
- **Analyse du code :** Identification du challenge crypto (PRNG linéaire sur GF(2), seed 64 bits, fuite du dernier octet du nonce).
- **Recherche d'outils :** Découverte de l'outil `polly_solver` conçu spécifiquement pour ce challenge.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Résolution DNS :** Tentative de connexion à `polly.chal.csaw.io` échouée (`Name or service not known`).
- **Connexion locale :** Tentative en `localhost:5000` refusée (`Connection refused`), le service n'est pas hébergé localement.
- **Exécution aveugle :** Lancer le solver sans vérifier la connectivité réseau préalable.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Théorie :** La méthode de résolution est comprise (système d'équations linéaires sur GF(2) pour retrouver le seed).
- **Fichiers clés :** `main.py` (logique du challenge), `polly_solver.py` (outil de résolution).
- **Blocage :** Le solveur existe mais est inutilisable à cause d'un problème de réseau ou de configuration d'hôte.

## Prochaines pistes
- **Debug réseau :** Vérifier la résolution DNS (nslookup/ping) ou trouver l'IP réelle du challenge.
- **Inspection du solveur :** Analyser `polly_solver.py` pour voir si les paramètres d'hôte sont hardcodés ou configurables.
- **Plan B :** Si le réseau reste bloqué, implémenter la logique de résolution GF(2) manuellement en Python.
