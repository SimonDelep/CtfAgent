

---
## Résumé au tour 10 (10:41:18)

## Fait
- **Récupération des assets** : Copie du binaire `vespers`, source `vespers.c`, `libc.so.6` et `ld-2.35.so`.
- **Analyse statique** : Identification de la structure `chorister_t` (56 octets nom + pointeurs + flags).
- **Vulnérabilité clé** : Détection d'un **Use-After-Free (UAF)** dans `op_retire` qui libère `c->transcript` et `c` sans mettre `choir[idx]` à `NULL`, permettant une réutilisation via `op_restore`.
- **Outils** : Création et correction d'un client interactif (`vespers_client`) pour simuler les commandes.
- **Protection** : Confirmation du PIE et du linking dynamique.

## Échecs / impasses
- **Connectivité distante** : Résolution DNS échouée (`NXDOMAIN`) pour `saint-vespers-and-the-copper-choir.chal.csaw.io` depuis l'environnement de travail.
- **Test local** : Erreur de décodage UTF-8 lors de l'exécution locale (`byte 0xd0`), suggérant une sortie binaire non gérée ou un prompt spécifique.
- **Type de données** : Bug mineur initial sur le type `port` (string vs int) dans le script Python.

## État actuel
- **Hypothèse validée** : Le mécanisme de gestion de la mémoire des choristes permet de dupliquer des pointeurs (UAF).
- **Environnement** : Workspace configuré avec les binaires locaux prêts pour le debug.
- **Blocage** : Impossible de tester l'exploit sur le serveur distant à cause du DNS ; dépendance forte au debug local pour valider la fuite de libc.

## Prochaines pistes
- **Debug local** : Lancer `vespers` sous `gdb` ou `pwntools` en gérant les encodages pour valider le flux de données.
- **Exploitation UAF** : Tenter de libérer un `transcript`, en allouer un autre de même taille pour surécrire un pointeur de fonction (`sing`) ou un pointeur de données.
- **Contournement DNS** : Vérifier si l'IP est accessible ou se concentrer sur la résolution locale avec `libc` fournie pour calculer les offsets.
- **Leak** : Chercher à lire une adresse libc via le champ `transcript` ou `name` avant de corrompre le flux.


---
## Résumé au tour 20 (10:46:15)

## Fait (actions utiles et ce qu'elles ont donné)
- **Analyse statique** : Lecture du code source (`vespers.c`) révélant une vulnérabilité UAF (Use-After-Free) critique entre `op_retire` et `op_restore`.
- **Contournement technique** : Création de l'outil `vespers_interactive` et script Python pour gérer les encodages binaires corrompus (noms de fichiers invalides en UTF-8).
- **Localisation** : Identification des fichiers cibles (`vespers`, `libc.so.6`) à la racine du dossier de travail.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Commandes shell natives** : `ls -la` et `list_files` ont planté systématiquement à cause de caractères de contrôle (surrogates UTF-8) dans les noms de fichiers.
- **Lecture de fichier** : Nécessité de relancer `read_file` 3 fois (3000/6000/9000 bytes) pour obtenir le code complet, inefficace.
- **Hypothèse de structure** : Perte de temps à chercher le binaire dans un dossier `dist/` inexistant.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Vulnérabilité** : `op_retire` libère `c->transcript` et `c` sans mettre `choir[idx]` à `NULL`. `op_restore` vérifie `choir[idx] != NULL`, permettant de réutiliser un pointeur dangling.
- **Environnement** : Binaire ELF64, libc fournie (`libc.so.6`), protections à vérifier (checksec partiel).
- **Interaction** : Première séquence de commandes envoyée via l'outil interactif (résultat brut à analyser).

## Prochaines pistes
- **Exploitation** : Tenter de corrompre la structure `Chorister` via le UAF (double free ou overwrite de métadonnées).
- **ROP** : Chercher des gadgets dans `vespers` ou `libc` pour appeler `system` ou `puts`.
- **Debugging** : Utiliser GDB pour inspecter l'état de la mémoire après les appels `retire`/`restore` et valider le pointeur libre.


---
## Résumé au tour 30 (10:52:42)

## Fait
- **Analyse source** : Code `vespers.c` lu, logique de gestion des choristes identifiée.
- **Vulnérabilité** : Use-After-Free (UAF) détectée dans `op_retire`/`op_restore` (pointeur `choir[idx]` non mis à NULL).
- **Reconnaissance binaire** : ELF 64-bit, PIE, NX, RELRO partiel, stripped. Bibliothèques `libc.so.6` et `ld-2.35.so` disponibles localement.
- **Outils** : Client interactif `vespers_client` créé pour le test remote.

## Échecs / impasses
- **Initialisation** : Erreur de décodage UTF-8 lors de la copie des fichiers (`cp -r`).
- **Remote** : Connexion instable (DNS `gaierror` ou output vide avec le client).
- **Local** : Test avec `echo | ./vespers` échoué (le shell interprète le binaire comme un script).
- **Exploitation** : Aucun crash ou fuite d'adresse confirmée pour l'instant.

## État actuel
- **Théorie** : L'UAF est confirmée par le code source ; on peut réallouer un objet sur un slot libéré.
- **Environnement** : Binaire et libc locaux prêts pour le debugging.
- **Obstacle** : Difficulté à interagir proprement avec le service remote pour valider l'exploitation.

## Prochaines pistes
- **Stabilisation** : Script Python direct (`socket`) pour contourner les problèmes de client/tool.
- **Exploitation** : Forcer une double-free ou une allocation contrôlée sur le slot dangling.
- **Fuite** : Récupérer une adresse libc via le pointeur valide mais libéré.
- **Shell** : Construire une chaîne ROP pour appeler `system("/bin/sh")` en contournant PIE.
