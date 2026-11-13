

---
## Résumé au tour 10 (12:56:17)

## Fait
- **Récupération des artefacts** : Copie réussie des 3 fichiers (`pcap`, `xml`, `memdump`) depuis le dossier challenge.
- **Analyse Memdump** : Extraction de chaînes utiles (utilisateurs `d.reyes`, `a.dubois`, machine `FNW-WKS047`, chaîne encodée `PDQ=...`).
- **Analyse XML** : Identification d'événements PrintService (ID 307) et d'un chemin suspect (`WindowsUpdate.exe` dans `System32`).
- **Analyse Réseau** : Repérage de trafic DNS massif et d'une connexion vers 10.14.0.9:8443.

## Échecs / impasses
- **Environnement** : Perte de temps initiale due à un workdir vide (fichiers absents).
- **Outil de parsing** : Le script `extract_singletons` a crashé (`struct.unpack` error) sur le binaire du pcap.
- **Inspection brute** : `tcpdump` standard n'a pas permis de voir les payloads applicatifs.

## État actuel
- **Fichiers** : 3 artefacts disponibles et partiellement lus.
- **Indicateurs** : Domaine `fenwick.local`, sous-domaine `fileshare-toulouse`, port 8443 suspect.
- **Hypothèse** : Compromission liée à l'impression (PrintNightmare ?) avec exfiltration via DNS ou C2 chiffré.

## Prochaines pistes
- **Débuggage** : Contourner le crash du script (utiliser `tshark` ou `scapy` pour les ports singleton).
- **Crypto** : Tenter de décoder la chaîne `PDQ=SXrPVed5HjrAoV...` (Base64 URL-safe ou XOR).
- **DNS** : Extraire les requêtes DNS du pcap pour chercher des données exfiltrées (tunneling).
- **Logs** : Chercher les détails complets de l'EventID 307 dans le XML.


---
## Résumé au tour 20 (13:00:12)

## Fait
- **Extraction Memdump** : Identification de chemins système (`shell32.dll`), clé registre `Cryptography` et blobs encodés (`PDQ=SXrPVed5...`).
- **Analyse PCAP** : Détection de trafic vers `10.14.0.9:8443` avec User-Agent spoofé (`Microsoft-Delivery-Optimization`).
- **Indice Réseau** : Mots-clés en clair trouvés (`fileshare-toulouse`, `fenwick`, `office365`).
- **Cryptanalyse** : Tentatives de décodage Base64 (URL-safe) et ROT13 sur les chaînes du memdump.

## Échecs / impasses
- **Environnement** : Module Python `scapy` manquant, bloquant l'analyse avancée du PCAP.
- **Déchiffrement** : Le décodage Base64 des blobs donne du binaire (probablement XOR/chiffré), pas de texte lisible.
- **Cryptanalyse** : ROT13 sur `DIHWTROXP` et `TGCPAQYTAH` ne produit pas de mots anglais évidents.
- **PCAP** : `tcpdump -A` sur le port 8443 montre le handshake, mais le payload HTTP reste difficilement exploitable.

## État actuel
- **Cible** : Serveur C2 suspecté à `10.14.0.9`.
- **Preuve** : Processus `MsMpEng.exe` et clé registre `Cryptography` présents en mémoire.
- **Données** : Chaînes encodées (Base64 URL-safe) et chaînes mystères (`DIHWTROXP`) à résoudre.
- **Contexte** : Environnement Windows compromis, simulation de trafic Office/Defender.

## Prochaines pistes
- **XOR Brute-force** : Tester des clés XOR sur les données binaires issues du décodage Base64.
- **Autres Ciphers** : Tester Atbash, Caesar ou Vigenère sur `DIHWTROXP`.
- **Outils PCAP** : Installer `scapy` ou utiliser `tshark` pour extraire les flux TCP complets.
- **Recherche** : Investiguer la signification de `fileshare-toulouse` (nom de domaine interne ou chemin de fichier).
