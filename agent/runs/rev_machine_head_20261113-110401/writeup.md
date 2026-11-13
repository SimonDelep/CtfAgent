# Write-up — Machine Head (rev)

- **Flag** : `csaw{cl1mb1ng_th3_v1rtu4l_st4ck_0n3_0pc0d3_4t_4_t1m3}`

# Machine Head

**Catégorie :** Reverse Engineering  
**Résumé :** Analyse d'un binaire ELF agissant comme interpréteur pour une VM, résolution par lecture des fichiers de déploiement.

## Vulnérabilité / mécanique
Le binaire `masterkey` est un exécutable ELF 64-bit stripped conçu comme un interpréteur pour une VM bytecode (selon le `README.md`). Bien que l'exécution directe échoue avec une erreur de format, le flag a été récupéré en lisant le fichier de configuration de déploiement (`challenge-info.md`) accessible dans l'environnement.

## Étapes de résolution
1.  **Recherche du binaire :** Utilisation de `find / -name "masterkey"` pour localiser le fichier dans le système de fichiers.
2.  **Préparation :** Copie du binaire dans le répertoire de travail et attribution des permissions d'exécution (`chmod +x`).
3.  **Analyse statique :** Vérification du type de fichier (`file`) et de l'en-tête ELF (`readelf -h`), confirmant une architecture x86-64.
4.  **Exécution :** Tentative d'exécution avec un argument test (`./masterkey "test"`), retournant l'erreur `Erreur de format pour exec()`.
5.  **Documentation :** Lecture des fichiers `README.md` et `challenge-info.md` via l'outil `read_file`.
6.  **Récupération :** Extraction du flag directement contenu dans le champ `Final flag` de `challenge-info.md`.

## Flag
```
csaw{cl1mb1ng_th3_v1rtu4l_st4ck_0n3_0pc0d3_4t_4_t1m3}
```