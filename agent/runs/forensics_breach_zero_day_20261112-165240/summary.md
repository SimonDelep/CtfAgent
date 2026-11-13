

---
## Résumé au tour 10 (16:54:48)

## Fait
- **Extraction :** Copie des 3 artefacts (`pcap`, `xml`, `memdump.txt`).
- **Memdump :** Identification de l'hôte (`FNW-WKS047`), du domaine (`fenwick.local`) et d'une chaîne suspecte `PDQ=...`.
- **PCAP :** Détection de trafic C2 sur `10.14.0.9:8443` (UA spoofé) et exfiltration JSON en clair sur port 80 (`/api/v2/telemetry`).
- **XML :** Confirmation des logs Windows (PrintService, TaskScheduler) sur la machine cible.

## Échecs / impasses
- **PCAP 8443 :** Lecture brute avec `tcpdump -A` peu lisible (traffic TLS chiffré), nécessite extraction de flux.
- **Memdump :** Fichier déjà en format texte (avec adresses hex), `strings` redondant, limite l'usage d'outils binaires classiques (Volatility).
- **Recherche initiale :** Trop de bruit dans le PCAP (mises à jour Windows légitimes vs trafic malveillant).

## État actuel
- **Cible :** `FNW-WKS047.fenwick.local`.
- **Indicateurs :** C2 sur `10.14.0.9:8443`, exfiltration vers `telemetry.microsoft.com`.
- **Preuve clé :** JSON d'exfiltration contenant `deviceId` et chaîne encodée `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j` dans le memdump.
- **Processus :** `MsMpEng.exe` (Windows Defender) potentiellement compromis ou utilisé comme couverture.

## Prochaines pistes
- **Décodage :** Tenter de décoder la chaîne `PDQ=...` (Base64, XOR, etc.).
- **PCAP :** Extraire le flux HTTP du port 80 pour récupérer le JSON complet de l'exfiltration.
- **Corrélation :** Chercher le `deviceId` trouvé dans le PCAP pour lier les événements.
- **Logs :** Analyser les EventID spécifiques dans le XML (TaskScheduler) pour trouver le point d'entrée.


---
## Résumé au tour 20 (16:56:30)

## Fait
- **Navigation :** Correction du chemin de travail (trouvé dans `work/` et non `/workdir`).
- **Memdump :** Extraction de la chaîne `PDQ` (`SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j`) depuis `fenwick_memdump.txt`.
- **PCAP :** Identification du trafic HTTP et des endpoints telemetry (`telemetry.microsoft.com`) via `strings`.
- **Indice :** Récupération du DeviceID (`FNW-WKS047`) et des en-têtes de requêtes POST.

## Échecs / impasses
- **Tshark :** Filtre `tcp.port == 80` muet (probable problème de format PCAP ou encapsulation).
- **Extraction HTTP :** Tentative initiale avec `-e http.file_data` sans résultat.
- **Hypothèse de chemin :** Erreur de supposition sur l'emplacement du dossier de travail.

## État actuel
- **Fichiers :** `fenwick_capture.pcap` et `fenwick_memdump.txt` dans le dossier de travail.
- **Données connues :** Chaîne PDQ, DeviceID, structure des requêtes telemetry (JSON partiel visible).
- **Manquant :** Le corps complet des requêtes POST (données exfiltrées) et la fonction exacte de la chaîne PDQ.

## Prochaines pistes
- **Extraction brute :** Utiliser `tshark -x` ou `tcpdump -A` pour voir le contenu brut des paquets POST.
- **Analyse PDQ :** Tester la chaîne PDQ comme clé de décryptage ou mot de passe.
- **Recherche texte :** Scanner le PCAP avec `strings` pour des mots-clés comme `flag`, `secret`, `password` ou `exfil`.


---
## Résumé au tour 30 (16:58:16)

## Fait (actions utiles et ce qu'elles ont donné)
- **Navigation :** Correction du path (on était déjà dans `work`).
- **PCAP :** Extraction des requêtes HTTP. Identification de trafic légitime (telemetry Microsoft) et suspect (`POST /api/sync` vers `backup-vault.fenwick.local`).
- **Base64 :** Décodage réussi de l'ID `QkFDS1VQU1ZD` → `BACKUPSVC`.
- **Memdump :** Recherche de chaînes critiques. Découverte de `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j` à proximité de `MsMpEng.exe` et de clés de registre services.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Commande `cd work` :** Redondante, perte de temps.
- **Base64 partiel :** Tentative de décodage de `UkVMQVF` et `lTSEVMTA==` sans contexte complet (erreurs de padding ou données corrompues).
- **Grep générique :** Recherche de "backdoor" dans le memdump trop bruyante, renvoyant principalement des services Windows standards (`WinDefend`, `SecurityHealthService`).

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichiers :** `fenwick_capture.pcap`, `fenwick_security.xml`, `fenwick_memdump.txt`.
- **Indice 1 :** Un service nommé `BACKUPSVC` communique avec un serveur interne `backup-vault.fenwick.local`.
- **Indice 2 :** Chaîne `PDQ=...` présente dans la mémoire, potentiellement un token ou une clé de configuration.
- **Indice 3 :** Contexte de sécurité Windows (Defender, Services) présent dans le dump, suggérant une tentative de masquage ou d'injection.

## Prochaines pistes
- **Analyse de la chaîne PDQ :** Déterminer si `SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j` est une clé de chiffrement ou un mot de passe.
- **Investigation PCAP :** Extraire le corps des réponses du `backup-vault` pour voir s'il y a des fichiers ou des commandes.
- **Corrélation Memdump :** Chercher des références à `BACKUPSVC` ou des binaires personnalisés dans le dump autour des adresses mémoire trouvées.
- **Logs XML :** Examiner les événements PrintService pour un lien avec le service de sauvegarde (méthode de persistance possible).


---
## Résumé au tour 40 (17:00:25)

## Fait
- Identification du service cible : décodage de l'ID `QkFDS1VQU1ZD` en `BACKUPSVC`.
- Analyse réseau : confirmation de la résolution DNS de `backup-vault.fenwick.local` vers `52.172.136.34`.
- Extraction de données : récupération de la chaîne suspecte `PDQ=...` directement depuis le fichier `fenwick_memdump.txt`.

## Échecs / impasses
- Filtres `tshark` HTTP (`-Y "http.host..."`) retournant vide : le trafic sur le port 8443 n'est pas du HTTP standard ou est chiffré.
- Tentative initiale de `strings` sur le PCAP trop générique, noyant les indices utiles.
- Analyse bloquée sur le fichier tronqué `fen...` (nom incomplet dans le listing).

## État actuel
- **Indice réseau :** Communication POST vers `/api/sync` avec réponse `{"status":"ok"}`.
- **Indice mémoire :** Chaîne encodée `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j` présente dans le memdump.
- **Contexte :** Service de sauvegarde compromis (`BACKUPSVC`), trafic mixte (DNS clair, TCP 8443 opaque).

## Prochaines pistes
- **Décodage :** Tester la chaîne `PDQ=...` en Base64 pour révéler le nom du backdoor ou une clé.
- **Fichier manquant :** Trouver le nom complet du fichier `fen...` (probablement `fenwick...`) pour l'ouvrir.
- **Corrélation :** Rechercher des références à `BACKUPSVC` ou `backup-vault` dans le memdump pour trouver des clés de chiffrement.
