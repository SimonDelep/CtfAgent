SCHEMA = {
  "name": "mp4_analyzer",
  "description": "Extrait et analyse toutes les chaînes de caractères et métadonnées d'un fichier MP4, en identifiant les blocs XMP et autres métadonnées encodées",
  "parameters": {
    "properties": {
      "mp4_file": {
        "description": "Chemin du fichier MP4",
        "type": "string"
      }
    },
    "required": [
      "mp4_file"
    ],
    "type": "object"
  }
}

def main(args):
    import base64
    import re

    mp4_file = args['mp4_file']

    # Lire le fichier
    with open(mp4_file, 'rb') as f:
        data = f.read()

    # Extraire toutes les chaînes imprimables de longueur >= 4
    strings = []
    current = []
    for byte in data:
        if 32 <= byte <= 126:
            current.append(chr(byte))
        else:
            if len(current) >= 4:
                strings.append(''.join(current))
            current = []
    if len(current) >= 4:
        strings.append(''.join(current))

    # Trouver les blocs XMP
    xmp_blocks = []
    for i, s in enumerate(strings):
        if 'xmp' in s.lower() or 'XMP' in s or 'rdf' in s.lower() or 'RDF' in s:
            xmp_blocks.append((i, s))

    # Chercher des chaînes encodées en Base64 (pattern typique)
    base64_pattern = re.compile(r'[A-Za-z0-9+/]{20,}={0,2}')
    b64_candidates = []
    for s in strings:
        matches = base64_pattern.findall(s)
        for m in matches:
            if len(m) >= 20:
                b64_candidates.append(m)

    # Essayer de décoder les candidats Base64
    decoded_candidates = []
    for candidate in b64_candidates:
        try:
            decoded = base64.b64decode(candidate).decode('utf-8', errors='ignore')
            if len(decoded) >= 10:  # Filtrer les courts
                decoded_candidates.append((candidate, decoded))
        except:
            pass

    # Afficher les résultats
    print("=== Chaînes trouvées (échantillon) ===")
    for s in strings[:20]:
        print(f"  {s}")

    print(f"\n=== Blocs XMP trouvés: {len(xmp_blocks)} ===")
    for i, s in xmp_blocks:
        print(f"  [{i}] {s[:100]}...")

    print(f"\n=== Candidats Base64: {len(b64_candidates)} ===")
    for candidate, decoded in decoded_candidates[:10]:
        print(f"  Encodé: {candidate[:50]}...")
        print(f"  Décodé: {decoded[:100]}...")
        print()

    # Afficher toutes les chaînes uniques
    unique_strings = sorted(set(strings))
    print(f"\n=== Toutes les chaînes uniques ({len(unique_strings)}) ===")
    for s in unique_strings:
        print(f"  {s}")

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
