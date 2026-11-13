

---
## Résumé au tour 10 (05:27:03)

## Fait
- **Localisation & Copie :** Fichiers (`pcap`, `xml`, `memdump`) trouvés via `find` et copiés dans le workdir.
- **Analyse préliminaire :** Identification des types de fichiers et extraction de chaînes (`strings`).
- **Indices réseau :** Détection de trafic HTTP sur 8443 déguisé en `Microsoft-Delivery-Optimization` vers `10.14.0.9`.
- **Indices systèmes :** Noms de domaine (`fenwick.local`), processus (`MsMpEng.exe`) et chaîne suspecte (`PDQ=...`) repérés dans le memdump.

## Échecs / impasses
- **Chemin par défaut :** Dossier `/challenge/` inexistant, a nécessité une recherche système.
- **Filtre réseau :** Commande `tshark` sur le port 8443 retournée vide (problème de filtre ou d'encodage).
- **Flou sur le payload :** Le trafic 8443 est visible mais le contenu exact (commande/backdoor) reste à extraire proprement.

## État actuel
- **Fichiers :** Les 3 artefacts sont prêts à l'analyse dans le dossier de travail.
- **Hypothèse :** Un C2 communique via 8443 en utilisant un nom de service légitime comme couverture.
- **Format du flag :** `csaw{{C2INDICATOR_SERVICENAME_BACKDOORNAME}}`.
- **Données clés :** `fileshare-toulouse.fenwick.local`, `PDQ=SXrPVed5HjrAoV...`, Event Log PrintService (ID 307).

## Prochaines pistes
- **Décodage :** Tenter de décoder la chaîne `PDQ=...` (Base64, XOR, etc.).
- **Analyse XML :** Examiner en détail l'EventID 307 du fichier `fenwick_security.xml`.
- **Extraction réseau :** Utiliser `tshark` ou Wireshark pour extraire les objets HTTP du flux 8443.
- **Memdump :** Rechercher les noms de services et de backdoor spécifiques dans le texte brut.


---
## Résumé au tour 20 (05:29:53)

## Fait (actions utiles et ce qu'elles ont donné)
*   **Analyse Memdump :** Extraction de chaînes critiques via `strings` : URL C2 (`https://fenwick-intranet.local/api/status`), nom de service masqué (`SecurityHealthService`), et identifiants suspects (`XsH7x2iZ7`, `PDQ=...`).
*   **Analyse XML :** Identification de l'EventID 7045 (création de service) et 307 (activité d'impression), confirmant une persistance via service Windows.
*   **Analyse PCAP :** Contournement de l'absence de `tshark` avec `tcpdump`. Confirmation d'un flux TCP actif sur le port 8443 entre 10.14.22.47 et 10.14.0.9.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
*   **Outils manquants :** `tshark` et `scapy` absents, ayant ralenti l'analyse du PCAP et du parsing Python.
*   **Décodage Base64 :** Tentative de décodage de la chaîne `PDQ=...` (après correction des caractères URL-safe) : résultat binaire non lisible, probablement chiffré ou non Base64 standard.
*   **Extraction Payload PCAP :** `tcpdump -A` a affiché les en-têtes TCP mais le payload applicatif reste difficilement exploitable sans réassemblage de flux.

## État actuel (ce qu'on sait, fichiers/indices clés)
*   **Vecteur d'attaque :** Service Windows légitime détourné (`SecurityHealthService`) créé via l'EventID 7045.
*   **Infrastructure :** C2 hébergé sur `fenwick-intranet.local` (port 8443).
*   **Indices de compromission :**
    *   Chaîne `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j` (memdump).
    *   Chaîne `XsH7x2iZ7` (memdump).
    *   Fichiers clés : `fenwick_security.xml`, `fenwick_memdump.txt`, `fenwick_capture.pcap`.

## Prochaines pistes
*   **Extraire les données PCAP :** Écrire un script Python simple (sans scapy) pour lire les octets TCP bruts et chercher des headers HTTP/JSON.
*   **Investiguer l'EventID 7045 :** Extraire le champ `Image` ou `ServiceFileName` du XML pour trouver le nom du binaire malveillant.
*   **Analyse de la chaîne PDQ :** Tester d'autres encodages (Hex, XOR) ou considérer que c'est une clé de session chiffrée.
*   **Recherche de mots de passe :** Chercher `XsH7x2iZ7` dans les autres fichiers ou comme mot de passe par défaut du service.


---
## Résumé au tour 30 (05:32:19)

## Fait
- **Logs XML :** Identification d'EventID 7045 (création de service) avec des chemins suspects (`C:\Windows\System32\WindowsUpdate.exe`), imitant des processus légitimes.
- **Memdump :** Extraction d'URLs C2 (`fenwick-intranet.local/api/status`) et d'un token potentiel (`PDQ=SXrPVed5HjrAoV...`).
- **PCAP :** Confirmation du trafic C2 sur le port 8443 entre 10.14.22.47 et 10.14.0.9, avec un heartbeat (`GET /heartbeat`) et un User-Agent spoofé.

## Échecs / impasses
- **Recherche de chaînes :** Les `strings` bruts sur le memdump n'ont pas révélé directement le nom exact du service backdoor (trop de bruit système).
- **Analyse PCAP :** Le dump texte (`-A`) du flux 8443 reste majoritairement binaire/chiffré, rendant la lecture du payload difficile sans décryptage SSL.
- **Corrélation :** Difficulté à lier immédiatement l'IP source du PCAP à un processus spécifique dans le memdump.

## État actuel
- **Menace :** Service Windows malveillant déguisé (probablement lié à `SecurityHealthService` ou un des faux noms trouvés).
- **C2 :** Communication active sur 8443, protocole probablement HTTPs/TLS.
- **Preuve :** Token d'authentification ou clé de session trouvé en mémoire (`PDQ=...`).
- **Réseau :** IP compromise 10.14.22.47 communiquant avec l'infrastructure 10.14.0.9.

## Prochaines pistes
- **Décryptage :** Tenter de décrypter le flux TLS du PCAP (cherchez les clés SSL dans le memdump).
- **Corrélation PID :** Chercher dans le memdump les références à l'IP 10.14.22.47 pour identifier le PID du processus malveillant.
- **Exploitation :** Tester le token `PDQ=...` sur l'API `/api/status` ou `/heartbeat`.
- **Filtrage :** Isoler les services créés dans le XML pour trouver celui qui correspond au trafic 8443.
