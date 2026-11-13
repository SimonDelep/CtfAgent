

---
## Résumé au tour 10 (23:51:00)

## Fait (actions utiles et ce qu'elles ont donné)
- **Extraction de fichiers :** Copie et identification des 3 artefacts (pcap, xml, memdump).
- **Analyse XML :** Lecture des logs Windows ; détection de services suspects (`WindowsUpdate.exe` dans `System32`).
- **Analyse Memdump :** Extraction de chaînes (`strings`) révélant des clés de registre (`Services\SecurityHealthService`), des URLs (`fenwick-intranet.local`) et des données encodées.
- **Analyse PCAP :** Identification du trafic sortant vers `10.14.0.9:8443` et d'un User-Agent suspect (`Microsoft-Delivery-Optimization` avec `/heartbeat`).

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Regex Base64 :** La recherche de chaînes encodées via `grep` standard a été peu efficace (résultats vides ou bruités).
- **Lecture brute PCAP :** `tcpdump -A` a montré principalement des en-têtes TCP/Handshakes, masquant le contenu HTTP/HTTPS chiffré.
- **Focus initial sur l'EventID 307 :** Le log PrintService semble être du bruit par rapport aux indices de services système trouvés dans le memdump.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Service compromis :** `SecurityHealthService` (clé de registre trouvée dans le memdump).
- **Indicateur C2 :** IP `10.14.0.9` ou domaine `fenwick-intranet.local`.
- **Processus suspect :** `MsMpEng.exe` listé dans le memdump (potentiellement usurpé ou lié au backdoor).
- **Flag attendu :** `csaw{{C2INDICATOR_SERVICENAME_BACKDOORNAME}}`.

## Prochaines pistes
- **Décodage :** Isoler et décoder les chaînes Base64 du memdump (ex: `SXrPVed5HjrAoV...`) pour trouver le nom du backdoor.
- **Analyse réseau avancée :** Utiliser `tshark` pour suivre les flux TCP (`tcp.port == 8443`) et extraire les requêtes HTTP si possible.
- **Corrélation :** Lier le service `SecurityHealthService` au binaire malveillant identifié dans le memdump pour compléter le flag.


---
## Résumé au tour 20 (23:53:12)

## Fait (actions utiles et ce qu'elles ont donné)
*   **Analyse Memdump :** Extraction de chaînes critiques dans `fenwick_memdump.txt`. Identification de `MsMpEng.exe`, clés de registre `Cryptography` et d'un token suspect `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j`.
*   **Recherche de C2 :** Découverte d'une URL Microsoft Graph (`/v1.0/me`) et de chemins `Windows Defender` suggérant une exfiltration ou une persistance via des outils légitimes.
*   **Analyse Réseau :** Validation du fichier `fenwick_capture.pcap`. Identification d'un flux TCP actif sur le port **8443** entre `10.14.22.47` et `10.14.0.9` (via `tcpdump`).
*   **Logs :** Lecture partielle de `fenwick_security.xml` confirmant l'activité des services système (PrintService, SCM).

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
*   **Outils PCAP :** `tshark` a renvoyé des résultats vides initialement, entraînant une perte de temps avant de basculer sur `tcpdump`.
*   **Regex Base64 :** Le script Python a trop inclus d'adresses hexadécimales (`7ff6000d...`) dans les résultats, nécessitant un nettoyage manuel.
*   **Grep XML :** La recherche générique de "backdoor" dans le XML n'a rien donné de concluant, il faut cibler les Event IDs spécifiques.

## État actuel (ce qu'on sait, fichiers/indices clés)
*   **Token suspect :** `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j` (probable clé ou mot de passe).
*   **Chaines mystères :** Plusieurs chaînes en majuscules pures non décodées (`DIHWTROXP`, `TGCPAQYTAH`, `HJKSYJGAM`, `AncillaryDynamics`).
*   **Cible réseau :** Le serveur `10.14.0.9` semble être le point de contact (port 8443).
*   **Contexte :** Environnement Windows (SysWOW64, ProgramData) avec une activité Defender potentiellement contournée ou utilisée.

## Prochaines pistes
1.  **Décodage :** Tenter de décoder la chaîne `PDQ=...` en Base64 URL-safe et vérifier les chaînes majuscules (ROT13, Caesar, ou noms de processus).
2.  **PCAP Deep Dive :** Extraire les paquets HTTP/TLS du port 8443 pour voir le contenu de la communication (certificats, payloads).
3.  **Corrélation :** Chercher dans le XML les Event IDs liés à la création de processus (`4688`) ou aux connexions réseau (`5156`) autour de l'heure des paquets PCAP.
4.  **Recherche de noms :** Google-er les chaînes majuscules (`AncillaryDynamics`) pour vérifier s'il s'agit de logiciels malveillants connus ou de noms de projet internes.


---
## Résumé au tour 30 (23:55:41)

## Fait (actions utiles et ce qu'elles ont donné)
- **Analyse Memdump :** Identification de la chaîne suspecte `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j` et de l'URL `https://graph.microsoft.com/v1.0/me`.
- **Analyse PCAP :** Détection de trafic sur le port **8443** entre `10.14.22.47` et `10.14.0.9`, avec un User-Agent spoofé (`Microsoft-Delivery-Optimization/10.0`) et un endpoint `/heartbeat`.
- **Analyse Logs :** Extraction d'événements XML liés au `Service Control Manager` et au `PrintService` (ProcessID 656).

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Décodage Base64 :** Le token décodé en Base64 URL-safe renvoie des bytes binaires (`Iz\xcfU...`) plutôt qu'un texte lisible ou un flag.
- **ROT13 :** Application sur les chaînes `DIHWTROXP`, `TGCPAQYTAH`, etc., donnant des résultats illisibles (`QVUJGEBKC`, etc.).
- **Grep de mots-clés :** Recherche de `backdoor`/`c2` dans le memdump n'a retourné que des chemins système Windows standards (bruit).
- **Regex Memdump :** La recherche de chaînes alphanumériques longues a retourné vide (probable erreur de regex ou absence de données).

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichiers :** `fenwick_memdump.txt`, `fenwick_capture.pcap`, `fenwick_security.xml`.
- **Indice principal :** Token `SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j` (probable clé ou session).
- **Réseau :** C2 suspect sur 8443 (chiffré ou binaire), IP cible `10.14.0.9`.
- **Processus :** Activité anormale liée au ProcessID 656 dans les logs de sécurité.
- **Hypothèse :** Backdoor se faisant passer pour un service Windows légitime (Delivery Optimization / Defender).

## Prochaines pistes
- **PCAP Deep Dive :** Utiliser Wireshark ou `tshark` pour extraire le payload TCP du port 8443 (SSL/TLS ? XOR ?).
- **Token :** Tester d'autres encodages (Base64 standard, Hex, XOR avec des clés courantes) sur la chaîne `SXrPVed5...`.
- **Corrélation :** Croiser le ProcessID 656 des logs XML avec les processus actifs dans le memdump.
- **URL :** Vérifier si l'endpoint `graph.microsoft.com` est un faux serveur ou un vrai relais (DNS logs ?).


---
## Résumé au tour 40 (23:58:03)

## Fait
- Copie des 3 artefacts (`fenwick_capture.pcap`, `fenwick_security.xml`, `fenwick_memdump.txt`).
- **Memdump** : Identification de l'hôte `FNW-WKS047`, utilisateur `d.reyes`, et chaîne suspecte `PDQ=...` (type clé).
- **PCAP** (via `strings`) : Détection de trafic HTTP heartbeat vers `10.14.0.9` (UA spoofé), mentions `fileshare-toulouse` et `RC48`.
- **XML** : Confirmation du domaine `fenwick.local` et présence de logs PrintService/Service Control Manager.

## Échecs / impasses
- Filtre `tshark` sur le port 8443 retournant vide (le trafic HTTP est présent mais probablement sur un autre port ou mal filtré).
- Lecture brute du fichier XML trop verbeuse, peu d'indices directs extraits sans `grep`.
- Pas encore de flag ni de payload clair extrait du PCAP.

## État actuel
- **Cible** : Poste de travail `FNW-WKS047.fenwick.local`.
- **C2 suspect** : IP `10.14.0.9` communiquant via HTTP (réponse `{"ack":true}`).
- **Indice clé** : Chaîne `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j` (potentiellement une clé de chiffrement ou token).
- **Contexte** : Environnement Windows Defender, impression réseau, service nommé `RC48`.

## Prochaines pistes
- Extraire les payloads HTTP du PCAP (`tshark -A -Y http`).
- Analyser le format de la chaîne `PDQ=` (Base64, hex, custom ?).
- Rechercher spécifiquement le ProcessID 656 mentionné dans les logs XML.
- Vérifier les autres ports du PCAP (DNS, SMB) pour compléter la chronologie.
