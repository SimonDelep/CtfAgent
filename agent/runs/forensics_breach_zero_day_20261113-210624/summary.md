

---
## Résumé au tour 10 (21:10:15)

## Fait (actions utiles et ce qu'elles ont donné)
- **Copie des artefacts** : Récupération de `fenwick_capture.pcap`, `fenwick_security.xml` et `fenwick_memdump.txt` dans le workdir.
- **Analyse Memdump** : Extraction de chaînes via `strings` révélant la clé `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j`, une chaîne contenant littéralement "C2" (`r/o2e5adE76q=MuQJ_+C2LNY...`), et des traces de `services.exe`/`MsMpEng.exe`.
- **Analyse XML** : Identification d'un EventID 7045 (création service "Windows Update" pointant vers `C:\Windows\System32\WindowsUpdate.exe`) et EventID 307 (PrintService).
- **Analyse PCAP** : Confirmation du trafic C2 vers `10.14.0.9:8443` (heartbeat `GET /heartbeat`) et téléchargement de payload `pkg_6941.cab` depuis `52.38.116.235:80`.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Environnement initial** : Workdir vide au démarrage (nécessité de copier les fichiers manuellement).
- **Lecture PCAP brute** : Le contenu des paquets 8443 et 80 apparaît binaire/chiffré dans `tcpdump -A`, peu lisible sans extraction préalable.
- **Filtrage de chaînes** : Le filtre `grep` sur les chaînes encodées (base64-like) dans le memdump n'a pas encore donné de résultats clairs (trop de bruit système).
- **XML tronqué** : L'aperçu initial du XML ne montrait que l'EventID 307, nécessitant une recherche ciblée pour les 7045.

## État actuel (ce qu'on sait


---
## Résumé au tour 20 (21:14:09)

## Fait (actions utiles et ce qu'elles ont donné)
- **Récupération des artefacts** : Copie initiale de `fenwick_capture.pcap`, `fenwick_security.xml` et `fenwick_memdump.txt`.
- **Analyse XML approfondie** : Identification de 7 services falsifiés créés (EventID 7045), dont `Windows Update` pointant vers `C:\Windows\System32\WindowsUpdate.exe`, ainsi que `Application Identity`, `Network Location Awareness`, etc.
- **Extraction Memdump** : Utilisation de `strings` et scripts Python pour extraire les chaînes. Découverte de la clé `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j` et de la chaîne `r/o2e5adE76q=MuQJ_+C2LNY,6bfJvVo+NKwbTHk` (contient littéralement "C2").
- **Analyse PCAP** : Confirmation du trafic C2 vers `10.14.0.9:8443` (heartbeat) et téléchargement de `pkg_6941.cab` depuis `52.38.116.235:80`.
- **Format du flag** : Identification du format attendu : `csaw{{C2INDICATOR_SERVICENAME_BACKDOORNAME}}`.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Environnement initial** : Workdir vide au démarrage (nécessité de copier les fichiers manuellement).
- **Lecture PCAP brute** : Le contenu des paquets 8443 et 80 reste binaire/chiffré dans `tcpdump -A`, peu lisible sans extraction préalable.
- **Filtrage de chaînes** : Le `grep` avec regex strict (`^[A-Za-z0-9+/=]{20,}$`) sur le memdump a échoué.
- **Recherche par mots-clés** : La recherche Python pour "Service", "Backdoor" a principalement retourné des processus système légitimes (`lsass.exe`, `MsMpEng.exe`, `wmiprvse.exe`) plutôt que des indices directs.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichiers** : `fenwick_capture.pcap`, `fenwick_security.xml`, `fenwick_memdump.txt` disponibles.
- **Infrastructure** : C2 interne (`10.14.0.9:8443`), Serveur de téléchargement (`52.38.116.235:80`).
- **Backdoor** : Service `Windows Update` exécutant `WindowsUpdate.exe` dans `System32`.
- **Indicateurs Memdump** : Clé `PDQ=...` et chaîne `...C2LNY...` (contenant "C2").
- **Format Flag** : `csaw{{C2INDICATOR_SERVICENAME_BACKDOORNAME}}`.

## Prochaines pistes
- **Construction du flag** : Tester les combinaisons avec `Windows Update` (Service) et `WindowsUpdate.exe` (Backdoor).
- **Indicateur C2** : Déterminer si l'indicateur est la chaîne `PDQ=...` ou la chaîne contenant "C2" (`r/o2e5adE76q=...`).
- **Décodage** : Tenter de décoder les chaînes encodées (base64-like) trouvées dans le memdump.
- **Payload** : Si possible, extraire et analyser le contenu du fichier `.cab` téléchargé sur le port 80.


---
## Résumé au tour 30 (21:17:21)

## Fait (actions utiles et ce qu'elles ont donné)
- **Récupération des artefacts** : Copie initiale de `fenwick_capture.pcap`, `fenwick_security.xml` et `fenwick_memdump.txt`.
- **Analyse XML** : Identification de 7 services falsifiés. Confirmation forte du service `Windows Update` pointant vers `C:\Windows\System32\WindowsUpdate.exe` (répété plusieurs fois dans les logs).
- **Extraction Memdump** : Utilisation de `strings` couplé à `sed` (`s/^[0-9a-f]* //`) pour nettoyer les adresses hexadécimales. Découverte de la clé `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j` et de chaînes encodées (base64-like) contenant "C2".
- **Analyse PCAP** : Confirmation du trafic C2 vers `10.14.0.9:8443` (handshake/heartbeat) et téléchargement HTTP de `pkg_6941.cab` depuis `52.38.116.235:80`.
- **Format du flag** : Validé : `csaw{{C2INDICATOR_SERVICENAME_BACKDOORNAME}}`.

## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)
- **Environnement initial** : Workdir vide au démarrage (nécessité de copier les fichiers manuellement).
- **Lecture PCAP brute** : Le contenu des paquets 8443 et 80 reste binaire/chiffré dans `tcpdump -A`, peu lisible sans extraction préalable.
- **Filtrage de chaînes (initial)** : Le `grep` avec regex strict sur le memdump a échoué car il ne tenait pas compte des adresses hexadécimales en préfixe (résolu par `sed`).
- **Recherche par mots-clés** : La recherche Python pour "Service", "Backdoor" a principalement retourné des processus système légitimes (`lsass.exe`, `MsMpEng.exe`) plutôt que des indices directs.

## État actuel (ce qu'on sait, fichiers/indices clés)
- **Fichiers** : `fenwick_capture.pcap`, `fenwick_security.xml`, `fenwick_memdump.txt` disponibles.
- **Infrastructure** : C2 interne (`10.14.0.9:8443`), Serveur de téléchargement (`52.38.116.235:80`).
- **Backdoor** : Service `Windows Update` exécutant `WindowsUpdate.exe` dans `System32`.
- **Indicateurs Memdump** : 
    - Clé unique : `PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j`.
    - Chaînes suspectes : `r/o2e5adE76q=MuQJ_+C2LNY...` (contient littéralement "C2").
- **Format Flag** : `csaw{{C2INDICATOR_SERVICENAME_BACKDOORNAME}}`.

## Prochaines pistes
- **Construction du flag** : Tester les combinaisons avec `Windows Update` (Service) et `WindowsUpdate.exe` (Backdoor).
- **Indicateur C2** : Déterminer si l'indicateur est la clé `PDQ=...` (probable) ou la chaîne contenant "C2". Nettoyer la clé (remplacer `=` par `_` ?) pour le flag.
- **Décodage** : Tenter de décoder les chaînes encodées (base64-like) trouvées dans le memdump pour voir si elles révèlent l'IP ou le nom exact.
- **Payload** : Si possible, extraire et analyser le contenu du fichier `.cab` téléchargé sur le port 80 pour confirmer le nom du binaire.
