SCHEMA = {
  "name": "extract_xmp_blocks",
  "description": "Extrait tous les blocs XMP d'un fichier MP4 et affiche leur contenu",
  "parameters": {
    "properties": {
      "filepath": {
        "description": "Chemin du fichier MP4",
        "type": "string"
      }
    },
    "required": [
      "filepath"
    ],
    "type": "object"
  }
}

import subprocess
import re

def main(args):
    filepath = args.get("filepath", "finderskeepers.mp4")
    
    # Utiliser exiftool ou strings pour extraire les métadonnées XMP
    result = subprocess.run(["strings", filepath], capture_output=True, text=True)
    content = result.stdout
    
    # Chercher les blocs XMP - ils contiennent souvent des balises rdf:li
    xmp_blocks = re.findall(r'<rdf:li>([^<]+)</rdf:li>', content)
    
    print(f"Nombre de blocs XMP trouvés: {len(xmp_blocks)}")
    for i, block in enumerate(xmp_blocks):
        print(f"Bloc {i}: {block}")
    
    # Chercher aussi les chaînes Base64 potentielles
    b64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
    b64_matches = re.findall(b64_pattern, content)
    print(f"\nChaînes Base64 potentielles: {len(b64_matches)}")
    for match in b64_matches[:10]:
        print(f"  {match}")

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
