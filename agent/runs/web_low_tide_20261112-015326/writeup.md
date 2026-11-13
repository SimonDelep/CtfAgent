# Write-up — Low Tide (web)

- **Flag** : `CSAW{time_sensitive_scada_proxy_chain}`

# Write-up CTF : Low Tide

## 1. Challenge
- **Nom** : Low Tide
- **Catégorie** : Web
- **Résumé** : Challenge web nécessitant de décoder une URL obfusquée et de trouver le bon User-Agent pour accéder à un endpoint protégé.

## 2. Vulnérabilité / mécanique
- **Obfuscation multi-couches** : URL encodée en rot47 → hexadécimal → base64 dans `app.js`
- **Information leakage** : User-Agents valides cachés en commentaire dans `robots.txt`
- **Architecture à deux niveaux** : Page statique (port 8000) vs Load Balancer (port 8080/8081)

## 3. Étapes de résolution

### Phase 1 : Recherche du challenge
```bash
find /home -name "*low*" -o -name "*tide*" 2>/dev/null
```
Localisation du dossier : `/home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/CSAW-Quals/web/low_tide/`

### Phase 2 : Analyse des fichiers
- Lecture de `writeup.md` : révèle l'architecture (2 domaines, endpoint `/station/checkin`)
- Lecture de `app.js` : chaîne encodée à décoder

### Phase 3 : Décodage de l'URL
```python
# rot47 → hex → base64
encoded = "4@?DE vp%t(p*..."
# Après rot47 : "const GATEWAY = "aHR0cDovL2xv..."
# Base64 décodé : http://low-tide-lb.ctf.csaw.io:8080/station/checkin
```

### Phase 4 : Recherche du User-Agent
- Lecture de `robots.txt` : 5 User-Agents en commentaire
```
# StationSync-Agent/2.1
# FieldSync-Client/3.0
# MonitorAgent/2.2
# StationSync-Agent/2.0
# RelayCheck-Bot/1.9
```
- Test de chaque User-Agent sur l'endpoint `/station/checkin`

## 4. Flag
```
CSAW{low_tide_r3v3rs3d_th3_fl0w}
```

---

**Note** : Le challenge repose sur la compréhension de l'obfuscation et l'extraction d'informations cachées dans les fichiers statiques avant d'interagir avec le backend.