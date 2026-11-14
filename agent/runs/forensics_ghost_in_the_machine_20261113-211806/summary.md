

---
## Résumé au tour 10 (21:21:40)

## Fait
- **Environnement :** Workdir initial vide, fichier `capture.pcap` copié depuis le challenge.
- **Outils :** `scapy` installé (`--break-system-packages`), outil `pcap_analyzer` forgé pour l'analyse UDP.
- **Analyse binaire :** Lecture hexadécimale (`xxd`) effectuée.
- **Découvertes :** Magic number PCAP modifié (`c4c3b2a1`), présence de marqueurs `dead beef` délimitant les paquets, payload "PING" identifié.
- **Réseau :** Adresses IP extraites (ex: `10.13.37.5`, `10.13.37.9`), ports UDP visibles.

## Échecs / impasses
- **Persistance :** Outils forgés précédemment non chargés au redémarrage.
- **Bibliothèques :** `scapy` manquant initialement, erreur `externally-managed-environment`.
- **Parsing :** Lecture standard `rdpcap` échouée (format non conforme au standard).
- **Structure :** Tentative d'analyse automatique bloquée par les marqueurs `dead beef` inattendus.

## État actuel
- **Fichier :** `capture.pcap` (format custom, byte-swapped ou modifié).
- **Structure connue :** En-tête global (24 octets) + Paquets contenant `dead beef` + En-tête IP/UDP + Payload.
- **Données connues :** Payloads textuels ("PING"), adresses IP source/dest, ports sources.
- **Outils :** `pcap_analyzer` disponible mais nécessite adaptation pour ignorer les marqueurs `dead beef`.

## Prochaines pistes
- **Parsing :** Écrire un script Python pour lire le fichier binaire en sautant les `dead beef`.
- **Extraction :** Récupérer tous les payloads UDP et les ports sources dans l'ordre.
- **Cryptographie :** Tester un XOR sur les payloads avec les ports ou les marqueurs comme clé.
- **Automatisation :** Utiliser l'outil `pcap_analyzer` pour extraire les séquences de ports et vérifier une logique de flag.


---
## Résumé au tour 20 (21:27:07)

## Fait
- **Environnement :** `capture.pcap` (31272 octets) présent dans le workdir.
- **Analyse binaire :** Magic number `c4c3b2a1` (custom), en-tête global de 40 octets.
- **Structure :** 504 paquets identifiés (1008 marqueurs `dead beef`, 2 par paquet). Payloads "PING" détectés.
- **Réseau :** Adresses IP extraites (ex: `10.13.37.5`, `10.13.37.9`). Ports sources analysés.
- **Cryptographie :** Identification de 112 ports "singletons" (signal, ~50000) vs ports fréquents (bruit, ~40000). Clé dérivée "sh4dow" obtenue via modulo 256 des ports fréquents.

## Échecs / impasses
- **Outils :** `scapy` initial manquant (`externally-managed-environment`), `pcap_analyzer` planté (incompatibilité format).
- **Parsing :** `rdpcap` standard échoué (format non-conforme).
- **Crypto :** Résultat XOR illisible (données binaires) avec la clé "sh4dow" sur les singletons (problème d'ordre d'application suspecté).

## État actuel
- **Fichier :** `capture.pcap` entièrement parsé manuellement en Python.
- **Données clés :** 504 paquets, 121 ports uniques (112 singletons).
- **Clé :** "sh4dow" (bytes: `[115, 104, 52, 100, 111, 119]`).
- **Problème :** XOR des singletons (ordre d'apparition ou tri par valeur) ne donne pas de texte lisible.

## Prochaines pistes
- **Réajuster l'ordre :** Re-tester le XOR avec les singletons triés par valeur (vs ordre d'apparition).
- **Vérifier la clé :** Confirmer si "sh4dow" doit être répétée ou utilisée différemment.
- **Payload :** Examiner si le payload "PING" ou les ports de destination influencent le décryptage.
- **Alternative :** Tester d'autres combinaisons de clés basées sur les ports fréquents.


---
## Résumé au tour 30 (21:33:39)

## Fait
- **Environnement :** `capture.pcap` (31272 octets), Magic `c4c3b2a1`, en-tête global 40 octets.
- **Structure :** 504 paquets identifiés via marqueurs `deadbeef` (espacement 6 octets intra-paquet, 56 inter-paquet).
- **Réseau :** IPs `10.13.37.5` et `10.13.37.9` confirmées, payload "PING" visible dans les données brutes.
- **Crypto :** Clé "sh4dow" dérivée de ports fréquents (analyse précédente validée).

## Échecs / impasses
- **Outils :** `pcap_analyzer` et `scapy` incompatibles avec le format custom (plantage au chargement).
- **Parsing :** Script manuel récent a retourné 0 paquets UDP extraits (erreur de calcul d'offset sur l'en-tête IP).
- **Crypto :** Résultat XOR illisible avec "sh4dow" sur les singletons (ordre d'application suspecté).

## État actuel
- **Fichier :** Structure comprise (Header 40b + Paquets délimités par `deadbeef` + 2 octets + `deadbeef` + Données).
- **Données :** 112 ports singletons identifiés précédemment (extraction à refaire), clé "sh4dow" prête.
- **Blocage :** Extraction automatique des ports sources bloquée par un mauvais offset (IP Header Length non pris en compte).

## Prochaines pistes
- **Corriger l'offset :** Ajuster le script : IP Header débute à l'octet 4 du paquet, UDP à l'octet 24 (IP Len 20).
- **Ré-extraction :** Relancer l'extraction des ports sources pour confirmer les 112 singletons.
- **Crypto :** Re-tester le XOR sur les singletons (ordre d'apparition vs tri par valeur) avec la clé "sh4


---
## Résumé au tour 40 (21:39:36)

## Fait
- **Environnement :** `capture.pcap` (31272 octets), Magic `c4c3b2a1`.
- **Structure :** 504 paquets identifiés via marqueurs `deadbeef` (1008 occurrences).
- **Parsing :** Script corrigé (ajout de 4 octets de métadonnées avant l'IP). Extraction des ports sources fonctionnelle.
- **Réseau :** IPs `10.13.37.5` et `10.13.37.9` confirmées, payload "PING" visible.
- **Données :** 112 ports singletons extraits avec succès.

## Échecs / impasses
- **Outils :** `pcap_analyzer` (scapy) incompatible avec le format custom.
- **Parsing initial :** Script manuel retournant 0 ports (erreur d'offset : IP débutait à 0 au lieu de 4).
- **Crypto :** Résultat XOR illisible avec "sh4dow" sur les singletons (ordre d'application suspecté).

## État actuel
- **Fichier :** Structure comprise (Header 40b + Paquets : `deadbeef` + 2b + `deadbeef` + 4b méta + IP + UDP + Payload).
- **Données :** 112 singletons identifiés. Ports fréquents confirmés (ex: 40115, 40104). Clé "sh4dow" prête.
- **Blocage :** Extraction automatique validée, mais décryptage des singletons bloqué (clé ou ordre).

## Prochaines pistes
- **Crypto :** Re-tester le XOR sur les singletons (tester ordre d'apparition vs tri par valeur).
- **Clé :** Vérifier la dérivée de "sh4dow" basée sur les ports fréquents identifiés.
- **Payload :** Analyser le contenu XORé une fois la clé validée.
