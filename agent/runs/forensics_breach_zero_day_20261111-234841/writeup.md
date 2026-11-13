# Write-up — Breach: Zero Day (forensics)

- **Flag** : `NON TROUVÉ`

# Write-up CTF : Breach Zero Day

## 1. Challenge
*   **Nom** : Breach Zero Day
*   **Catégorie** : Forensics
*   **Résumé** : Analyse d'une capture réseau, de logs Windows et d'un dump mémoire pour identifier un service malveillant et une backdoor.

## 2. Vulnérabilité / mécanique
*   **Masquage de service** : Un service malveillant nommé `SecurityHealthService` est créé pour ressembler à un processus légitime.
*   **Communication C2** : Le service communique avec un serveur de commande et contrôle (C2) sur le port 8443, déguisé en trafic de mise à jour ou de santé système.
*   **Artéfacts mémoire** : Les chaînes de caractères et les indicateurs de compromission (IOCs) sont laissés en clair ou faiblement encodés dans le dump mémoire.

## 3. Étapes de résolution

1.  **Préparation des fichiers** :
    *   Copie des trois fichiers fournis : `fenwick_capture.pcap`, `fenwick_security.xml`, `fenwick_memdump.txt`.
    *   Vérification des types de fichiers avec `file` : le PCAP est valide, le XML contient des logs Windows, le memdump est un fichier texte contenant des adresses mémoire et des chaînes.

2.  **Analyse des logs (XML)** :
    *   Lecture de `fenwick_security.xml`.
    *   Identification de fournisseurs d'événements suspects : `Microsoft-Windows-PrintService` (EventID 307), `Service Control