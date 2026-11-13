

---
## Résumé au tour 10 (14:02:37)

## Fait
- **Environnement préparé :** Copie complète des fichiers (`guard-dog`, `libc-2.31.so`, `ld-2.31.so`, `README.md`).
- **Analyse de sécurité :** `checksec` révèle un binaire **No PIE**, **No Canary**, **NX enabled**, **Partial RELRO**.
- **Hypothèse initiale :** Le README suggère un **Use-After-Free (UAF)** ("released dog doesn't always stay gone").
- **Identification des libs :** Version de libc confirmée (2.31), utile pour le calcul d'offsets.

## Échecs / impasses
- **Reverse Engineering bloqué :** `gdb` et `objdump` sur `main` retournent des instructions indéfinies (`.inst 0xfa1e0ff3`), rendant la lecture du code source difficile.
- **Outils manquants :** Tentative d'utilisation de `radare2` (`r2`) échouée car le binaire n'est pas dans le PATH, seul `r2pipe` est installé.
- **Strings peu utiles :** Les chaînes de caractères contiennent beaucoup de padding, aucune logique métier claire visible statiquement.

## État actuel
- **Cible :** Binaire `guard-dog` (ELF 64-bit, non-stripped mais entrée obscure).
- **Mémoire :** Heap probable (fonctions `malloc`/`free` présentes dans les strings).
- **Indices :** Menu interactif attendu (adopter/nommer/retirer chien).
- **Fichiers clés :** `guard-dog` (binaire), `libc-2.31.so` (pour le retour à `system` ou `one_gadget`).

## Prochaines pistes
- **Corriger l'outil d'analyse :** Installer le binaire `radare2` ou utiliser `pwndbg`/`gef` dans GDB pour mieux visualiser le code.
- **Analyse dynamique :** Lancer le binaire localement (`./guard-dog`) pour comprendre le menu et l'interaction.
- **Chercher la faille :** Repérer la fonction de "release" (retirement) qui omettrait de libérer la mémoire ou qui laisserait un pointeur dangling.
- **Exploitation :** Préparer un script Python (pwntools) pour tester des allocations et libérations successives.


---
## Résumé au tour 20 (14:04:31)

## Fait (actions utiles et ce qu'elles ont donné)
- **Analyse README** : Identification claire de la vulnérabilité (UAF sur les chiens libérés) et de l'indice structurel ("front of a dog" = pointeur de fonction/vtable).
- **Reconnaissance binaire** : Extraction des strings confirmant l'usage de `malloc`, `free`, `read`, `write` et la structure du menu (7 options).
- **Configuration d'exécution** : Résolution du problème d'interpréteur ELF en déplaçant `ld-2.31.so` dans `/tmp` et en utilisant `patchelf` pour corriger le chemin d'interpréteur du binaire.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Exécution directe** : `./guard-dog` a échoué car l'interpréteur est codé en relatif (`./ld-2.31.so`).
- **Variable d'environnement** : `LD_LIBRARY_PATH` n'a pas suffi car le problème venait du loader, pas des bibliothèques partagées.
- **Exécution via le loader** : `./ld-2.31.so ./guard-dog` a nécessité des permissions (`chmod +x`) et est moins pratique pour itérer que le binaire patché.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Vulnérabilité** : Use-After-Free (UAF) sur le pool de chiens.
- **Structure** : Le premier champ du `struct Dog` est critique (probablement un pointeur vers une fonction `bark`).
- **Environnement** : Glibc 2.31 (tcache, heap layout spécifique).
- **Binaire** : `guard-dog` est prêt à être exécuté localement avec le bon loader.

## Prochaines pistes
- **Validation locale** : Vérifier que le binaire patché s'exécute sans erreur.
- **Debugging** : Lancer GDB (pwndbg) pour inspecter les allocations `malloc` et la libération `free`.
- **Exploitation** : Tenter de libérer un chien, puis le commander pour écraser la fonction `bark` avec une adresse de gadget ou `system`.
- **Heap** : Analyser la taille des chunks alloués pour les chiens et les notes (UAF + Heap Feng Shui).


---
## Résumé au tour 30 (14:06:51)

## Fait
- Identification des fichiers du challenge dans le workdir (`guard-dog`, `ld-2.31.so`, `libc-2.31.so`).
- Analyse du binaire : ELF 64-bit, interpréteur durci vers `/tmp/ld-2.31.so`.
- Copie des bibliothèques système dans `/tmp` pour préparer l'environnement d'exécution.
- Envoi de données d'entrée simulées (`1\nTest\n...`) lors des tests.

## Échecs / impasses
- **Chemin de travail :** Exécution depuis `/tmp` échouée car le binaire `guard-dog` n'y a pas été copié correctement.
- **Outils manquants :** `patchelf` indisponible pour modifier l'interpréteur du binaire.
- **Exécution directe :** Lancer via le loader (`/tmp/ld-2.31.so ./guard-dog`) a renvoyé une "Erreur de format pour exec()" (problème de résolution de chemin ou de contexte).
- **Gestion des fichiers :** Tentatives de copie dans `/tmp` échouées (`Aucun fichier ou dossier de ce nom`), indiquant une confusion entre le workdir et `/tmp`.

## État actuel
- Le binaire `guard-dog` est physiquement situé dans le **workdir** (`.`).
- Les dépendances (`ld-2.31.so`, `libc-2.31.so`) sont présentes dans **`/tmp`**.
- L'interpréteur du binaire pointe vers `/tmp/ld-2.31.so`.
- Les permissions d'exécution sont définies sur le binaire.

## Prochaines pistes
- **Corriger le chemin :** Copier proprement `guard-dog` dans `/tmp` (ou déplacer les libs dans le workdir).
- **Exécuter depuis `/tmp` :** Une fois le binaire copié, lancer `./guard-dog` depuis `/tmp` en s'assurant que `LD_LIBRARY_PATH` pointe vers `/tmp` si nécessaire.
- **Patch alternatif :** Utiliser `sed` pour remplacer le chemin de l'interpréteur dans le binaire si `patchelf` manque.
- **Vérification :** S'assurer que l'architecture du loader correspond bien à celle du binaire (x86-64) pour éviter l'erreur de format.


---
## Résumé au tour 40 (14:08:50)

## Fait
- Copie des fichiers (`guard-dog`, `ld-2.31.so`, `libc-2.31.so`) dans `/tmp` pour faciliter l'exécution.
- Vérification de l'architecture avec `file` (tous deux détectés en x86-64).
- Utilisation de `patchelf` pour forcer l'interpréteur du binaire vers le loader local.
- Préparation des entrées de test (`1\nTest\n2\nHello\n3\n`).

## Échecs / impasses
- **Erreur persistante :** `Erreur de format pour exec()` (Exec format error) survenue à chaque tentative d'exécution.
- **Loader direct :** Lancer `./ld-2.31.so ./guard-dog` a échoué.
- **Patched binary :** Lancer `./guard-dog` après `patchelf` a échoué de la même manière.
- **Permissions :** Vérifiées (0775), ne semblent pas être la cause.

## État actuel
- Fichiers opérationnels dans `/tmp`.
- Binaire `guard-dog` modifié pour pointer vers `/tmp/ld-2.31.so`.
- Architecture supposée x86-64, mais le noyau semble rejeter le format.
- Environnement de test prêt, mais le binaire reste inaccessible.

## Prochaines pistes
- **Vérifier la "bitness" :** Utiliser `readelf -h` pour confirmer si le binaire ou le loader est en 32 bits (problème courant avec `Exec format error` sur x86-64).
- **Debugging :** Lancer avec `strace` pour voir l'appel système exact qui échoue.
- **Dépendances :** Vérifier les libs manquantes avec `ldd` (si possible) ou installer les paquets 32 bits (`libc6:i386`).
- **Alternative :** Essayer de lancer via `qemu` si l'architecture est différente.
