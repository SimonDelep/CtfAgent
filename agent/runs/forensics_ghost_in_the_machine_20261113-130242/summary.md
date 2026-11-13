

---
## Résumé au tour 10 (13:04:22)

## Fait
- Copie réussie de `capture.pcap` depuis le dossier source vers le dossier de travail.
- Analyse statistique : 504 paquets totaux, 112 ports sources uniques (singletons).
- Extraction des données : les paquets fréquents contiennent la chaîne hex `50494e47` ("PING").

## Échecs / impasses
- Navigation initiale : le chemin `/challenge` était inexistant, le dossier `work` était vide au départ.
- Bruit identifié : les ports fréquents (40000+) apparaissent ~64 fois chacun, confirmant l'hypothèse de leurres.

## État actuel
- Fichier `capture.pcap` prêt dans `work/`.
- Hypothèse validée : les 112 paquets singletons contiennent le signal, les autres sont du bruit.
- Données hexadécimales partiellement extraites, structure UDP identifiée.

## Prochaines pistes
- Filtrer le pcap pour isoler uniquement les paquets singletons.
- Extraire et concaténer les payloads hexadécimaux de ces paquets spécifiques.
- Convertir le résultat final en ASCII pour récupérer le flag.


---
## Résumé au tour 20 (13:08:42)

## Fait (actions utiles et ce qu'elles ont donné)
*   **Correction de chemin :** Identification et correction du chemin du fichier (`capture.pcap` à la racine du workdir).
*   **Analyse de trafic :** Identification de ports fréquents (401xx) et de 112 ports "singleton" (50xxx).
*   **Investigation payload :** Confirmation que le payload UDP est constant (`50494e47` = "PING"), éliminant le contenu comme source du signal.
*   **Format PCAP :** Identification du magic number spécifique (`0xa1b2c3c4` en little-endian) et visualisation de la structure des headers IP/UDP via hex dump.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
*   **XOR sur ports :** Tentative de XOR avec `port % 256` sur les singletons, résultat illisible.
*   **Outils standards :** `extract_signal_and_key` et parsers génériques ont échoué ou retourné 0 paquets à cause du magic number non standard.
*   **Parsing Python fragile :** Plusieurs scripts `run_python` ont planté (Traceback) lors de la lecture de l'entête PCAP (gestion incorrecte de l'endianness ou des offsets).
*   **Hypothèse Checksum nul :** L'outil initial affichait `checksum=0`, alors que le dump hex montre des valeurs actives (`c9 6e`), indiquant une erreur de lecture d'offset.

## État actuel (ce qu'on sait, fichiers/indices clés)
*   **Fichier :** `capture.pcap` (31272 bytes, format PCAP modifié).
*   **Flux :** UDP de `10.13.37.5` vers `10.13.37.9:9000`.
*   **Indice clé :** Le hint indique de chercher "what it was mixed with" dans "another column you skipped".
*   **Données disponibles :** Headers IP/UDP visibles (IP ID, Checksum UDP, Ports). Le signal est probablement caché dans un champ header (Checksum ou IP ID) et non dans le payload.

## Prochaines pistes
*   **Parser robuste :** Écrire un script Python stable pour lire ce format PCAP spécifique et extraire les champs UDP Checksum et IP ID.
*   **Extraction de données :** Récupérer la séquence des checksums UDP (ou IP ID) pour les paquets singletons.
*   **Décryptage :** Tester l'ASCII ou le XOR sur ces valeurs de checksums pour retrouver le flag.
*   **Vérification :** S'assurer que l'offset de lecture correspond bien à la position du checksum dans le dump hex (environ 0x40 dans le paquet).


---
## Résumé au tour 30 (13:14:38)

## Fait
- **Parsing personnalisé** : Contourné le format PCAP standard en identifiant les marqueurs `deadbeef` et le magic number `0xa1b2c3c4`.
- **Extraction des paquets** : Isolé 504 paquets et décodé les en-têtes IP/UDP (src `10.13.37.5`, dst `10.13.37.9`).
- **Filtrage du signal** : Identifié 112 paquets "singletons" (ports source uniques) contre 391 paquets de bruit (ports répétés 64 fois).
- **Corrélation** : Tous les singletons partagent un checksum IP spécifique (`0x986e`), distinct du bruit (`0xc96e`).

## Échecs / impasses
- **Lecture initiale** : Le script `struct` standard a échoué (1 paquet de 0 octet) à cause du header sur mesure.
- **XOR simple** : Tentative de XOR des ports avec `0x5365` ("Se") n'a pas produit de texte lisible immédiatement.
- **Checksums UDP** : Tous à 0, s'est avéré être un chemin sans issue.
- **Payload brut** : Les bytes après `PING` semblaient être un mélange de séquence et de données sans ordre évident.

## État actuel
- **Structure comprise** : Format custom `deadbeef` + IP/UDP + Payload.
- **Signal identifié** : Les 112 paquets avec port unique et checksum IP `0x986e` contiennent l'information.
- **Données connues** : Payload contient toujours `PING` + `00f1` (séquence) + `5365` ("Se") + données variables.
- **Indice clé** : Les ports source sont > 50000, mais leur octet bas varie probablement pour former le flag.

## Prochaines pistes
- **Extraction ASCII** : Convertir l'octet bas des ports des 112 singletons en caractères.
- **Tri par séquence** : Trier les singletons par le champ de séquence (`00f1`, `01f1`, etc.) avant de concaténer les octets.
- **Vérification XOR** : Tester si les données après `5365` sont le flag XORé avec le checksum IP ou le port.
- **Focus sur le hint** : "another column you skipped" suggère de ne pas ignorer le checksum IP ou le port comme clé de décodage.


---
## Résumé au tour 40 (13:20:01)

## Fait (actions utiles et ce qu'elles ont donné)
- Copie du fichier `capture.pcap` et vérification du magic number PCAP (`c4c3b2a1`).
- Identification de 1008 occurrences du marqueur `deadbeef` (504 paires).
- Parsing correct des headers PCAP (24 octets) et des headers de paquets (16 octets).
- Décryptage de l'encapsulation personnalisée : `deadbeef 0002 deadbeef 0001 0800` précède l'en-tête IP.
- Extraction réussie de 504 paquets UDP.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Hypothèse initiale fausse** : Croire que `deadbeef` délimite les paquets sans considérer le header PCAP standard.
- **Offset IP erroné** : Calcul initial à 12 octets au lieu de 14 (à cause des marqueurs personnalisés), causant un décalage.
- **Erreur de parsing** : `struct.error` sur le header UDP dû à une longueur IP mal calculée (buffer trop court).

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichier** : `capture.pcap` (31272 octets).
- **Structure** : 504 paquets encapsulés, UDP port 9000 (Src: 10.13.37.5, Dst: 10.13.37.9).
- **Contenu** : Payload visible "PING" (4 octets) constant sur les premiers paquets analysés.
- **Données suspectes** : Champ `0800` constant sur les premiers paquets (potentiellement un séquence ou type).

## Prochaines pistes
- **Analyse de masse** : Vérifier si le champ `0800` ou les marqueurs `0002`/`0001` varient sur les 504 paquets.
- **Extraction complète** : Concaténer tous les payloads pour détecter un message caché (stéganographie).
- **Variations** : Chercher des changements dans les checksums ou les timestamps qui pourraient indiquer des données exfiltrées.
