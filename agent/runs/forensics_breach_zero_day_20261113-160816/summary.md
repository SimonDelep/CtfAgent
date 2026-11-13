

---
## Résumé au tour 10 (16:10:39)

## Fait
- **Copie des fichiers :** Résolution du problème de workdir vide en copiant `fenwick_capture.pcap`, `fenwick_security.xml` et `fenwick_memdump.txt` depuis le dossier source.
- **Analyse Memdump :** Extraction de chaînes via `strings` révélant des chemins Windows, le processus `MsMpEng.exe`, l'URL `graph.microsoft.com`, et des chaînes suspectes (ex: `PDQ=...`).
- **Analyse XML :** Identification de logs Windows (EventID 7045) montrant la création suspecte du service `WindowsUpdate.exe` et liste des utilisateurs connectés.
- **Analyse Réseau :** Inspection initiale du pcap montrant du trafic TCP vers 10.14.0.9 sur le port 8443.

## Échecs / impasses
- **Cheminement initial :** Perte de temps à chercher les fichiers dans le workdir et `/challenge/` avant de trouver la source réelle.
- **Analyse pcap brute :** `tcpdump -A` sur le port 8443 a révélé peu de payload lisible (probablement chiffré ou heartbeat).
- **Filtrage Regex :** Tentative de grep pour isoler les chaînes base64 dans le memdump retournée vide (problème de formatage des chaînes dans le fichier texte).

## État actuel
- **Fichiers disponibles :** Les 3 artefacts sont dans le dossier de travail et identifiés.
- **Indicateurs clés :** Machine cible `FNW-WKS047`, utilisateur `d.reyes`, domaine `fenwick.local`.
- **Suspicion forte :** Service `WindowsUpdate.exe` créé via logs XML et données encodées présentes dans la mémoire vive.
- **Communication :** Trafic sortant vers 10.14.0.9:8443 identifié mais non décodé.

## Prochaines pistes
- **Décodage :** Tenter de décoder manuellement les chaînes suspectes du memdump (base64).
- **Pcap avancé :** Utiliser `tshark` ou Wireshark pour extraire les objets HTTP ou les flux TLS du port 8443.
- **Corrélation :** Aligner les horodatages entre le memdump, les logs XML et le trafic réseau.
- **Flag hunting :** Chercher le flag ou le mot de passe dans les données décryptées ou les fichiers temporaires extraits.


---
## Résumé au tour 20 (16:13:46)

## Fait (actions utiles et ce qu'elles ont donné)
*   **Analyse du memdump (`fenwick_memdump.txt`)** : Extraction de chaînes de caractères révélant des chemins système suspects, des URLs internes (`fenwick-intranet.local`) et une chaîne encodée `PDQ=SXrPVed5HjrAoV...`.
*   **Analyse du PCAP (`fenwick_capture.pcap`)** : Utilisation de `tcpdump` (après échec de `tshark`) pour identifier un trafic HTTP sur le port 8443. Découverte d'un heartbeat (`GET /heartbeat`) entre la cible (10.14.22.47) et un C2 interne (10.14.0.9).
*   **Analyse des logs (`fenwick_security.xml`)** : Filtrage des EventID 7045 (création de service). Identification de services légitimes renommés en backdoors (ex: `WindowsUpdate.exe` dans System32).

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
*   **Outil `tshark`** : Commande initiale retournant vide, probablement due à un problème de format ou de filtre. À remplacer par `tcpdump` pour une inspection rapide.
*   **Regex sur `strings`** : Expression régulière trop stricte (`Expression régulière invalide`) lors du filtrage des chaînes encodées.
*   **Distraction réseau** : Perte de temps à analyser le trafic vers les IPs Microsoft (52.x.x.x) avant de se concentrer sur le trafic interne (10.14.x.x) qui contient le C2.

## État actuel (ce qu'on sait, fichiers/indices clés)
*   **Mécanisme de persistance** : Service "Windows Update" pointant vers `C:\Windows\System32\WindowsUpdate.exe` (fichier malveillant).
*   **Communication C2** : Port 8443, protocole HTTP simple, User-Agent spoofé (`Microsoft-Delivery-Optimization`), réponse JSON `{"ack":true}`.
*   **Indicateurs de compromission (IoC)** : Domaine `fileshare-toulouse.fenwick.local`, IP C2 `10.14.0.9`.
*   **Données sensibles** : Chaîne `PDQ=...` présente en mémoire, potentiellement une clé de chiffrement ou une partie du flag.

## Prochaines pistes
*   **Décodage** : Tenter de décoder la chaîne `PDQ=...` (Base64 URL-safe ou autre).
*   **Extraction PCAP** : Isoler les paquets TCP port 8443 pour extraire le payload complet au-delà du heartbeat.
*   **Vérification API** : Tester l'URL `https://fenwick-intranet.local/api/status` trouvée en mémoire.
*   **Corrélation temporelle** : Aligner les timestamps des logs XML (2026-07-13) avec le PCAP pour confirmer le moment de l'infection.
