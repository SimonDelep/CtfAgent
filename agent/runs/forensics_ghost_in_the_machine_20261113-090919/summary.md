

---
## Résumé au tour 10 (09:11:31)

## Fait (actions utiles et ce qu'elles ont donné)
- **Localisation du fichier :** Correction du chemin initial erroné (`files/capture.pcap` inexistant) et copie réussie depuis le dossier source (`ghost_in_the_machine`).
- **Analyse du trafic :** Identification de 504 paquets UDP. Séparation claire entre le bruit (6 ports fréquents avec payload "PING") et le signal potentiel (112 ports singletons).
- **Extraction des données :** Récupération des valeurs hexadécimales des ports sources singletons (ex: `0xc6e1`, `0xc555`).

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Chemin par défaut :** Avoir supposé que `capture.pcap` était dans le dossier de travail actuel sans vérifier.
- **Déchiffrement XOR :** L'opération `port % 256` n'a pas produit de texte lisible (résultat non ASCII).
- **Focus sur les ports fréquents :** Les ports 40115, 40104, etc., ne contiennent que du trafic de maintien ("PING"), c'est un leurre.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichier :** `capture.pcap` (31 Ko, 504 paquets).
- **Indice clé :** Le hint mentionne "la clé cachée à plain sight, dans une autre colonne ignorée". Le port source lui-même semble être le vecteur.
- **Données brutes :** 112 ports singletons dans la plage `0xc300` - `0xc700`. Payload UDP des singletons non encore inspecté en détail, mais les ports sont l'indice principal.

## Prochaines pistes
- **Décodage direct :** Tester si les valeurs des ports singletons (ou une soustraction d'offset comme `port - 0xc000`) forment la chaîne de caractères du flag.
- **Ordre d'arrivée :** Vérifier si l'ordre chronologique des paquets singletons est nécessaire pour reconstruire le message.
- **Inspecter le payload :** Vérifier si les paquets singletons ont un payload différent de "PING" ou s'il est vide (confirmant que le port est la donnée).


---
## Résumé au tour 20 (09:14:29)

## Fait
- Contournement de l'environnement Python isolé en utilisant `run_shell` pour exécuter le script.
- Parsing manuel du fichier `capture.pcap` pour gérer le *byte order* inversé (magic `0xa1b2c3c4`).
- Extraction réussie de 504 paquets UDP et identification de 112 ports sources "singletons" (apparaissant une seule fois).

## Échecs / impasses
- Outil `pcap_extractor` initial (dépendance `scapy` manquante).
- Tentative avec `run_python` (environnement sandboxé sans `scapy`).
- Lecture directe avec `scapy` sans ajustement du *byte order* (erreur `Scapy_Exception`).
- Décodage brut des ports (modulo 256, soustractions fixes) donnant du texte illisible.

## État actuel
- Fichier `capture.pcap` valide mais en little-endian.
- Payloads UDP constants ("PING"), indiquant que le signal est dans les métadonnées (ports).
- 112 ports singletons détectés dans la plage 50004-50996.
- Les ports fréquents (ex: 40115) semblent être du bruit de fond.

## Prochaines pistes
- Trier les paquets singletons par ordre chronologique (timestamp).
- Découper les ports en 2 octets séparés pour tenter une conversion ASCII.
- Tester un décalage constant sur les ports (ex: `port - 0xC000` ou `0xC100`).
- Vérifier si la séquence des ports forme une chaîne de caractères lisible.


---
## Résumé au tour 30 (09:19:44)

## Fait
- Vérification du fichier `capture.pcap` (déjà présent dans le répertoire).
- Création et itération de l'outil `extract_singletons` pour parser le PCAP.
- Correction du parsing du header PCAP (passage de 16 à 24/20 bytes selon la structure).
- Extraction réussie de 504 paquets UDP et identification de 112 ports sources "singletons".

## Échecs / impasses
- Commande `cp` initiale inutile (fichier déjà local).
- Première exécution de l'outil `extract_singletons` (sortie vide due à un bug de décalage de lecture).
- Confusion initiale sur le magic number (`c4c3b2a1` vs standard `a1b2c3d4`), résolue par inspection hexadécimale.

## État actuel
- Fichier `capture.pcap` entièrement lu.
- Données clés : Séquence ordonnée de 112 ports singletons (ex: `[50913, 50517, 50915, ...]`).
- Hypothèse confirmée : Les ports singletons contiennent le message caché, les autres ports sont du bruit.

## Prochaines pistes
- Convertir les valeurs des ports (entiers 16 bits) en octets (high/low byte).
- Tenter un décodage ASCII ou Hex sur la séquence de ports.
- Vérifier le format de la flag (ex: `CTF{...}`).


---
## Résumé au tour 40 (09:27:05)

## Fait (actions utiles et ce qu'elles ont donné)
- Écriture d'un parser Python personnalisé pour corriger l'offset Ethernet (Network: 1).
- Identification de 504 paquets UDP au total.
- Extraction de 112 ports sources "singletons" (apparaissant une seule fois).
- Confirmation que le payload UDP est constant (`50494e47` = "PING").
- Vérification des adresses IP et ports de destination (constants : 10.13.37.5 -> 10.13.37.9:9000).

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- Outil `extract_singletons` initial (retour vide dû à un mauvais parsing).
- Conversion directe des ports singletons en octets (résultat illisible : `c6 e1...`).
- Tentative de XOR des données avec les ports fréquents (résultat bruité).
- Recherche de la clé dans les champs IP/Port standards (tous constants).

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichier :** `capture.pcap`.
- **Structure :** 112 paquets "message" (singletons) + 392 paquets "bruit" (fréquents).
- **Indice clé :** "the sender left the key hiding in plain sight, in another column you skipped".
- **Données connues :** Ports singletons (candidats message), Ports fréquents (candidats clé), Payload constant.
- **Blocage :** La clé n'est pas dans les ports sources/dest ou les IPs.

## Prochaines pistes
- Examiner les champs UDP ignorés (Length, Checksum) correspondant à la "colonne oubliée".
- Vérifier si l'ordre d'apparition des ports fréquents (blocs de 8) génère la clé.
- Tester le XOR des ports singletons (au lieu des données) avec les ports fréquents.
- Analyser les timestamps pour une séquence temporelle masquée.
