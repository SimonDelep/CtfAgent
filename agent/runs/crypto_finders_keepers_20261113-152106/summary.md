

---
## Résumé au tour 10 (15:24:44)

## Fait
- Copié le fichier `finderskeepers.mp4` dans le répertoire de travail.
- Exécuté `mp4_analyzer` : identification de 21 blocs XMP dans les métadonnées.
- Extrait et décodé la chaîne Base64 : `ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30=` → `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- Testé plusieurs méthodes de décryptage : ROT13, décalage Caesar (-2/+2), XOR avec préfixe connu.

## Échecs / impasses
- `mp4_stego_analyzer` (mode full) : retourne vide, aucune stéganographie standard détectée.
- Recherche `strings` : aucun mot-clé évident ("flag", "csaw") trouvé dans le brut.
- XOR simple avec clé courte : corrige le préfixe `csaw{` mais corrompt le reste du message.
- Décalage Caesar simple : les décalages nécessaires pour passer de `esnp` à `csaw` sont incohérents (-2, 0, -13, +7).

## État actuel
- **Payload brut :** `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- **Objectif :** Transformer le préfixe `esnp{` en `csaw{`.
- **Meilleure piste :** Chiffrement de Vigenère. L'utilisation de la clé `cant` produit `csaw{b0c_@lg@el_zu0h_pz3g3_e0_o00f}`.
- **Problème :** Le préfixe est correct, mais le contenu entre accolades semble encore partiellement crypté ou la clé est incomplète.

## Prochaines pistes
- Tester des clés Vigenère liées au nom du challenge (`finders`, `keepers`, `finderskeepers`).
- Vérifier si la clé `cant` est un mot-clé partiel ou s'il faut itérer sur la longueur de la clé.
- Analyser le texte déchiffré avec la clé `cant` pour voir si des mots anglais apparaissent.


---
## Résumé au tour 20 (15:34:47)

## Fait
- Déchiffrage Vigenère effectué avec plusieurs clés ('cant', 'finders', 'keepers', 'cantfind').
- Outil `vigenere_bruteforce` forgé pour tester des listes de clés.
- Analyse de substitution Leet Speak appliquée (0→o, @→a, 3→e).
- Soumission d'un flag candidat basé sur la clé 'cantfind'.

## Échecs / impasses
- Clés 'finders' et 'keepers' produisent des préfixes incorrects (`zkam`, `uoja`).
- Tentatives de ROT sur le contenu déchiffré sans résultat lisible.
- Le flag soumis `csaw{y0u_@lw@el_zu0e_hz3w3_e0_o00f}` a été rejeté.
- Substitution Leet simple ne corrige pas totalement les mots (`alwael` au lieu de `always`).

## État actuel
- Ciphertext déchiffré avec la clé 'cantfind' : `csaw{y0u_@lw@el_zu0e_hz3w3_e0_o00f}`.
- Préfixe `csaw{` confirmé valide.
- Le contenu semble être une phrase anglaise en Leet Speak, mais avec des erreurs de caractères ou une couche de chiffrement supplémentaire.

## Prochaines pistes
- Tester des variantes de la clé 'cantfind' (ex: 'cantfindme', 'cantfindit') pour corriger les lettres.
- Vérifier si le texte déchiffré est lui-même un autre chiffrement (XOR, Base64).
- Déduire le flag en corrigeant manuellement les mots probables (`you_always_here_to_off`).


---
## Résumé au tour 30 (15:40:20)

## Fait
- Analyse complète du fichier `finderskeepers.mp4` via `mp4_stego_analyzer`.
- Extraction des métadonnées XMP contenant une chaîne Base64 : `ZXNucHtkMGNfQHl6QGdsX21uMGpfcG0zejNfZzBfbzAwc30=`.
- Décodage Base64 donnant `esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}`.
- Identification d'un chiffrement Vigenère en comparant le préfixe `esnp` au format attendu `csaw`.
- Déduction de la clé `cantfind` et déchiffrement du contenu.

## Échecs / impasses
- Tentative de décalage simple (Caesar) : les différences de caractères n'étaient pas constantes.
- Nettoyage "Leet Speak" trop agressif : la soumission `csaw{you_alwael_zuoe_hzewe_eo_ooof}` a été rejetée.
- La clé `cantfind` fonctionne parfaitement sur le préfixe, mais le reste du message contient des symboles (`@`, `0`, `3`) qui ne forment pas des mots clairs après substitution.

## État actuel
- Format de flag confirmé : `csaw{...}`.
- Chiffrement principal : Vigenère avec la clé `cantfind`.
- Texte déchiffré brut : `csaw{y0u_@lw@el_zu0e_hz3w3_e0_o00f}`.
- Incertitude sur la nature des caractères spéciaux : sont-ils une erreur de déchiffrement ou une partie du flag (Leet conservé) ?

## Prochaines pistes
- Soumettre le résultat brut du Vigenère (`csaw{y0u_@lw@el_zu0e_hz3w3_e0_o00f}`) sans nettoyage Leet.
- Vérifier si la clé `cantfind` s'applique correctement sur toute la longueur ou si elle change.
- Relire les autres blocs XMP (il y en avait 21) pour voir s'il existe une autre chaîne Base64 ou une clé complémentaire.
- Tester des variantes de la clé (ex: `cant`, `find`, `cantfind` inversé).
