

---
## Résumé au tour 10 (16:50:08)

## Fait
- Copie du fichier challenge `12345678 (1).wav` vers `audio.wav`.
- Identification précise du format : WAV PCM 16-bit stéréo 44100 Hz.
- Extraction des données audio brutes via script Python (6 Mo, ~1.5M frames).
- Tentatives d'extraction de données cachées par LSB (global, par canal, somme/différence des canaux).

## Échecs / impasses
- **LSB Standard :** Les bits de poids faible extraits donnent du binaire illisible (pas de texte ASCII clair).
- **Outils automatisés :** Les appels `wav_analyzer` (modes `raw` et `lsb`) ont retourné des résultats vides ou non exploitables.
- **Séparation de canaux :** Isoler le canal gauche ou droit n'a pas révélé de message.
- **Opérations arithmétiques :** La somme et la différence des échantillons entre canaux n'ont pas produit de pattern lisible.

## État actuel
- Fichier `audio.wav` présent et analysé structurellement.
- Les valeurs audio sont extrêmement faibles au début (proches de 0), suggérant un silence ou un signal très atténué.
- Extraction LSB totale génère ~379 Ko de données brutes, sans entête de fichier visible.
- Aucun flag ou mot-clé détecté en lecture directe des données extraites.

## Prochaines pistes
- **Visualisation :** Générer un spectrogramme (via Python ou Audacity) pour repérer des motifs visuels cachés.
- **Autres bits :** Tester l'extraction sur d'autres bits (bit 2, 3, ou MSB) au lieu du LSB pur.
- **Recherche de strings :** Lancer `strings` ou recherche de motifs hexadécimaux dans le fichier brut.
- **Analyse fréquentielle :** Vérifier si le message est caché dans les fréquences spécifiques plutôt que dans l'amplitude des échantillons.


---
## Résumé au tour 20 (16:55:17)

## Fait
- **Localisation du fichier** : Identification du chemin absolu correct après échec initial (`find` et inspection manuelle).
- **Analyse des métadonnées** : Extraction des strings et analyse binaire des chunks WAV (ID3, LIST).
- **Décryptage** : Repérage et décodage de la chaîne Base64 `Ml81dDNAMV8=` présente dans les tags.
- **Résultat** : Obtention de la chaîne claire `2_5t3@1_`.

## Échecs / impasses
- **Chemin de fichier** : Confusion initiale entre le nom du fichier dans le dossier courant et le chemin réel.
- **Recherche système** : Tentative infructueuse d'accéder au dossier `/challenge/`.
- **Interprétation** : La chaîne décodée ne ressemble pas à un format de flag standard (manque préfixe `csaw{}`).

## État actuel
- **Fichier cible** : `/home/etudiantelambda/.../12345678 (1).wav`.
- **Indice clé** : Métadonnées ID3 et INFO contenant la chaîne encodée `Ml81dDNAMV8=`.
- **Donnée brute** : `2_5t3@1_`.

## Prochaines pistes
- **Soumission** : Tester `csaw{2_5t3@1_}` comme flag potentiel.
- **Exhaustivité** : Vérifier s'il existe d'autres chaînes Base64 à concaténer dans le fichier.
- **Audio** : Si échec, analyser le spectrogramme ou le contenu audio brut (LSB).


---
## Résumé au tour 30 (16:57:25)

## Fait
- **Extraction de données :** Script Python réussi pour scanner le binaire du WAV, révélant 57 chaînes Base64.
- **Décryptage :** Identification de `Ml81dDNAMV8=` décodant en `2_5t3@1_`, confirmant la structure du flag.
- **Gestion de fichiers :** Correction du chemin d'accès et copie du fichier `12345678 (1).wav` dans le workdir pour éviter les erreurs de chemin.
- **Développement :** Création d'un outil personnalisé `wav_lsb_extractor` pour contourner les limites de l'outil standard.

## Échecs / impasses
- **Soumission prématurée :** Le flag `csaw{2_5t3@1_}` a été refusé car non "grounded" (pas de sortie d'outil).
- **Outil défaillant :** L'outil `wav_analyzer` (modes `raw` et `lsb`) a retourné des résultats vides, probablement incompatible avec ce fichier spécifique.
- **Commande shell :** Premier `strings` échoué à cause d'un chemin absolu incorrect contenant des espaces.

## État actuel
- **Fichier cible :** `12345678 (1).wav` (6 Mo) disponible localement.
- **Indices clés :** Une partie du flag est cachée en clair/Base64 dans le binaire, mais la méthode de récupération complète (LSB ou autre) reste à valider.
- **Outils :** `wav_lsb_extractor` est prêt à être exécuté.

## Prochaines pistes
- **Exécution du nouvel outil :** Lancer `wav_lsb_extractor` sur le fichier local pour tenter de récupérer le message caché.
- **Analyse des autres chaînes :** Si LSB échoue, examiner les 56 autres chaînes Base64 trouvées (concaténation ou ordre spécifique ?).
- **Validation du format :** S'assurer que le résultat final est imprimé dans la console pour satisfaire la contrainte de "grounding".
