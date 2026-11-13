

---
## Résumé au tour 10 (17:38:03)

## Fait
- **Récupération des assets** : Copie complète du binaire (`vespers`), source (`vespers.c`), libc (`libc.so.6`) et loader (`ld-2.35.so`).
- **Analyse statique** : Lecture du code source. Identification de la structure `chorister_t` et des opérations (recruit, retire, restore...).
- **Hypothèse de vulnérabilité** : Détection d'un **Use-After-Free (UAF)** potentiel dans `op_retire()` : `free(c)` est appelé sans mettre `choir[idx]` à `NULL`, permettant une réutilisation du pointeur.
- **Reconnaissance binaire** : ELF 64-bit PIE, lié dynamiquement, glibc 2.35.

## Échecs / impasses
- **Exécution locale directe** : `./vespers` échoue (loader relatif manquant).
- **Exécution via loader** : `./ld-2.35.so ./vespers` renvoie "Erreur de format pour exec()" (problème d'interprétation par le shell ou permissions).
- **Script Python (subprocess)** : Échec lors de l'initialisation `Popen` (gestion incorrecte du loader comme exécutable ou environnement).
- **Connexion locale** : Tentative de connexion au port 5000 refusée (service distant non monté localement).

## État actuel
- **Vulnérabilité cible** : UAF sur le tableau global `choir[]` après un `retire`.
- **Environnement** : glibc 2.35 (version connue, exploitable), PIE activé (nécessite un leak d'adresse).
- **Fichiers de travail** : Tous les fichiers nécessaires sont présents dans le dossier `work/`.
- **Logique** : Le challenge simule une gestion de choristes avec allocation/désallocation de mémoires (`transcript`).

## Prochaines pistes
- **Stabiliser l'exécution** : Utiliser `pwntools` (`process` avec `executable='./ld-2.35.so'` et `argv=['./vespers']`) ou `gdb` avec `set env LD_LIBRARY_PATH=.` pour tester localement.
- **Valider l'UAF** : Script simple pour `recruit` -> `retire` -> `recruit` (même taille) et vérifier si les données se chevauchent.
- **Préparer l'exploit** :
    1. Leak d'adresse (libc) via UAF.
    2. Calcul de l'adresse de `system` ou `one_gadget`.
    3. Overwrite du pointeur `transcript` ou `sing` pour ROP/Shell.


---
## Résumé au tour 20 (17:40:58)

## Fait (actions utiles et ce qu'elles ont donné)
- **Analyse statique** : Lecture complète de `vespers.c`. Identification claire d'une logique de gestion de mémoire (recruit/retire/restore).
- **Vulnérabilité théorique** : Détection d'une **Use-After-Free (UAF)** potentielle dans `op_retire` (libération de `c` sans mise à `NULL` de `choir[idx]`, réutilisable via `op_restore`).
- **Analyse binaire** : Confirmation que `vespers` est un ELF 64-bit PIE, lié dynamiquement avec une libc et un loader locaux (`ld-2.35.so`).

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Lancement direct** : `./ld-2.35.so ./vespers` échoue avec "Erreur de format pour exec()". Le système ne reconnaît pas le loader comme exécutable valide dans ce contexte.
- **Tentatives Python** : `subprocess.Popen` avec le loader plante avec `OSError: [Errno 8]`. À éviter tant que le problème d'exécution n'est pas résolu.
- **Hypothèse de chemin** : `cd work` était inutile, les fichiers sont déjà dans le dossier courant.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Code source** : La logique de la vulnérabilité est comprise (tableau global `choir` non initialisé à `NULL` après `free`).
- **Environnement** : Fichiers critiques présents (`vespers`, `libc.so.6`, `ld-2.35.so`).
- **Blocage** : Le binaire est fonctionnel logiquement mais "coincé" au niveau du système d'exploitation (problème d'interpréteur ou d'architecture).

## Prochaines pistes
- **Contourner le loader** : Utiliser `patchelf` pour changer l'interpréteur vers le système, ou lancer via `gdb ./ld-2.35.so ./vespers`.
- **Vérification d'architecture** : S'assurer que `ld-2.35.so` est bien 64-bit (sinon utiliser `qemu`).
- **Exploitation** : Une fois le binaire exécutable, écrire un script `pwntools` pour : `recruit` -> `retire` -> `alloc` (pour récupérer l'adresse) -> `restore` -> `write` (UAF).


---
## Résumé au tour 30 (17:43:11)

## Fait (actions utiles et ce qu'elles ont donné)
*   **Identification des fichiers :** Correction de la structure de répertoire (fichiers à la racine, pas dans `dist/`).
*   **Analyse statique :** Confirmation que `vespers` est un ELF 64-bit PIE, lié dynamiquement à `ld-2.35.so` et `libc.so.6`.
*   **Diagnostic d'exécution :** Utilisation de `strace` pour confirmer l'erreur `ENOEXEC` lors du lancement du loader.
*   **Découverte clé :** Présence du fichier source `vespers.c` (8226 bytes), souvent ignoré au profit du binaire.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
*   **Exécution directe du loader :** Tenter d'exécuter `./ld-2.35.so` comme un programme standard (c'est un shared object, pas un exécutable).
*   **Patching agressif :** Multiples tentatives avec `patchelf` (interpréteur, rpath, replace-needed) qui ont fini par corrompre la reconnaissance du binaire par `ldd`.
*   **Hypothèse `dist/` :** Perte de temps initiale à chercher dans un dossier inexistant.
*   **Guerre contre le binaire :** Avoir passé trop de temps à "réparer" l'exécution avant de lire le code source.

## État actuel (ce qu'on sait, fichiers/indices clés)
*   **Cible :** `vespers` (binaire) + `vespers.c` (source).
*   **Environnement :** Besoin de la libc et du loader spécifiques (`ld-2.35.so`, `libc.so.6`) fournis.
*   **Problème bloquant :** Le binaire ne s'exécute pas nativement à cause de l'interpréteur personnalisé.
*   **Outils disponibles :** `gdb` installé, `patchelf` installé, `strace` fonctionnel.

## Prochaines pistes
1.  **Lire `vespers.c` :** Analyser la logique et les vulnérabilités potentielles (buffer overflow, format string, etc.) avant de recompiler ou de debugger.
2.  **Exécution via GDB :** Lancer `gdb ./vespers` en spécifiant le `sysroot` ou les bibliothèques manuellement pour éviter de patcher le binaire.
3.  **Compilation locale :** Tenter de recompiler `vespers.c` avec les flags appropriés pour voir si le binaire fourni est une version spécifique ou si on peut le reconstruire.
4.  **QEMU :** Si l'architecture est différente, utiliser `qemu-x86_64` avec les bibliothèques fournies.
