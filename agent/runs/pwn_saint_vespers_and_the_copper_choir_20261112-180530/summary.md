

---
## Résumé au tour 10 (18:10:55)

## Fait
- **Récupération complète** : Source (`vespers.c`), binaire (`vespers`), libc (`libc.so.6`) et loader (`ld-2.35.so`) copiés dans `work/`.
- **Analyse statique** : Identification de la structure `chorister_t` (88 octets) et des opérations (Recruit/Retire/Restore).
- **Hypothèse de vulnérabilité** : Détection d'un **UAF (Use-After-Free)** potentiel dans la fonction `Retire` (libération mémoire sans mise à NULL des pointeurs).
- **Checksec** : Binaire PIE (Position Independent Executable), stripped, glibc 2.35.

## Échecs / impasses
- **Connexion distante** : Résolution DNS du challenge (`saint-vespers...`) échouée (`NXDOMAIN`), empêchant le test direct du client.
- **Script client** : L'outil `vespers_client` forgé plante au `socket.connect` à cause du DNS.
- **Exécution locale** : Tentative de run local avec `echo` génère une erreur de décodage UTF-8 (sortie binaire non gérée par le runner), masquant le prompt exact.

## État actuel
- **Environnement** : Prêt pour le debug local (fichiers présents).
- **Vulnérabilité** : Le `Retire` laisse des pointeurs dangling dans le tableau des choristes.
- **Contrainte** : Protection PIE active, nécessitant une fuite d'adresse (libc ou stack) avant d'exploiter l'UAF.
- **Indice** : La structure contient un callback `sing` (pointeur de fonction) qui pourrait être surécrit.

## Prochaines pistes
- **Debug local** : Lancer le binaire dans GDB ou Pwntools (`gdb ./vespers`) pour contourner l'erreur UTF-8 et comprendre le format exact des entrées/sorties.
- **Fuite d'adresse** : Tester la commande `7` (ou similaire) pour voir si elle affiche des pointeurs ou du contenu mémoire.
- **Exploitation** : Une fois le leak obtenu, construire un ROP ou surécrire le callback `sing` pour gagner un shell.
- **Réseau** : Vérifier si le challenge est accessible via IP ou si le nom de domaine change dynamiquement.


---
## Résumé au tour 20 (18:13:08)

## Fait
- Récupération complète du code source `src/vespers.c` par chunks.
- Analyse de la structure `chorister_t` (88 octets) et identification de la vulnérabilité **UAF** dans `op_retire`.
- Vérification du format binaire (ELF64).
- Création d'un outil Python `list_files` pour contourner les erreurs d'encodage UTF-8 du shell.

## Échecs / impasses
- Commandes `ls -la` classiques échouées à cause de bytes invalides (0x80) dans la sortie.
- Nécessité de multiples appels `read_file` pour obtenir le code source complet.
- Pas encore de compilation ou d'exécution du binaire testée dans cette session.

## État actuel
- Vulnérabilité confirmée : Use-After-Free sur les pointeurs de fonction ou de transcript lors du retrait d'un choriste.
- Taille de l'objet cible connue (88 octets).
- Environnement de travail stabilisé (outil de listing fonctionnel).
- Binaire `vespers` présent dans le dossier de travail.

## Prochaines pistes
- Lancer `checksec` complet sur le binaire pour connaître les protections (PIE, Canary, ASLR).
- Écrire un script d'exploitation pour déclencher l'UAF et surcharger le pointeur `sing`.
- Analyser la gestion de la mémoire (glibc heap) pour cibler les allocations libres.


---
## Résumé au tour 30 (18:17:22)

## Fait
- **Analyse binaire :** Identifié ELF64, PIE activé, `BIND_NOW` (GOT résolu au démarrage), pas de canary visible.
- **Analyse source :** Lu `src/vespers.c`. Structure `chorister_t` comprise (56 octets `name`, pointeurs `sing` et `transcript`).
- **Vulnérabilité :** UAF confirmée dans `op_retire` (`free(c)` mais `choir[idx]` reste valide).
- **Outils :** Script `vespers_client` forgé pour interagir avec le service.

## Échecs / impasses
- **Outils manquants :** `checksec` et `pwntools` absents de l'environnement (contourné par `readelf` et analyse manuelle).
- **Connexion réseau :** Échec critique sur le host distant (`Name or service not known`). Le DNS ne résout pas le domaine depuis l'environnement actuel.
- **Hypothèse :** Tentative de connexion directe sans vérification préalable de la connectivité réseau.

## État actuel
- **Cible :** Binaire local `dist/vespers` et source `src/vespers.c`.
- **Mécanisme :** UAF permet de réallouer la mémoire libérée et d'écraser le pointeur `sing` (fonction) ou `transcript`.
- **Contraintes :** PIE nécessite un leak d'adresse (libc ou binaire) pour calculer les offsets.
- **Blocage :** Service distant inaccessible via le nom de domaine fourni.

## Prochaines pistes
- **Connectivité :** Vérifier le DNS, essayer l'IP directe ou `ping` pour valider l'accessibilité du service.
- **Debug local :** Lancer le binaire avec GDB pour valider les offsets de la structure et le comportement du `free`.
- **Exploitation :** Préparer un payload pour surécrire `sing` avec une adresse de gadget ou de `system` (après leak).
- **Leak :** Chercher un moyen de fuite d'adresse (format string ou lecture GOT) pour contourner le PIE.


---
## Résumé au tour 40 (18:19:30)

## Fait (actions utiles et ce qu'elles ont donné)
- **Récupération des assets :** Copie réussie du binaire `vespers`, de la `libc` et du `ld` depuis le dossier `dist` vers le workdir.
- **Contournement technique :** Utilisation de `run_python` pour copier les fichiers binaires, contournant le bug d'encodage UTF-8 de `run_shell`.
- **Analyse préliminaire :** Identification du binaire comme PIE (Position Independent Executable) via `readelf`.
- **Compréhension du contexte :** Lecture partielle de `vespers.c` révélant un système de gestion de "choristes" (allocation, archivage, restauration).

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Résolution DNS :** `ping`, `nslookup` et `dig` ont tous retourné `NXDOMAIN` pour le domaine remote. Le service distant semble inaccessible ou mal configuré.
- **Copie de binaires via Shell :** L'outil `run_shell` a échoué avec une erreur `'utf-8' codec can't decode byte` lors de la copie des fichiers binaires. À éviter pour les données brutes.
- **Lecture brute du binaire :** Tenter de lire le binaire comme du texte produit du "garbage" (caractères non imprimables).

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichiers locaux :** `vespers`, `libc.so.6`, `ld-2.35.so`, `vespers.c` sont disponibles dans le dossier de travail.
- **Hypothèse de vulnérabilité :** Le code source suggère une gestion de cycle de vie (recruter/retirer/restaurer), pointant fortement vers une **Use-After-Free (UAF)**.
- **Code source :** Début de lecture effectué (`#define MAX_CHOIR` visible), logique de gestion mémoire à confirmer.
- **Environnement :** Challenge PWN, protections standards probables (PIE confirmé).

## Prochaines pistes
- **Analyse de code :** Terminer la lecture de `vespers.c` pour identifier les fonctions `malloc`/`free` et les conditions de réutilisation de mémoire.
- **Checksec :** Lancer `checksec` sur le binaire local pour confirmer les protections (Canary, NX, RELRO).
- **Test local :** Lancer le binaire localement avec `gdb` (pwndbg) pour simuler l'interaction, puisque le remote est injoignable.
- **Chasse au UAF :** Repérer dans le code source où un pointeur est libéré mais potentiellement utilisé par la suite (restauration/archivage).
