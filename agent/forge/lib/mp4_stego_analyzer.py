SCHEMA = {
  "name": "mp4_stego_analyzer",
  "description": "Extrait et analyse les données stéganographiques d'un MP4 : LSB des pixels, métadonnées cachées, et recherche de patterns dans les frames",
  "parameters": {
    "properties": {
      "mode": {
        "description": "Mode d'analyse: 'lsb', 'metadata', 'strings'",
        "enum": [
          "lsb",
          "metadata",
          "strings",
          "full"
        ],
        "type": "string"
      },
      "mp4_file": {
        "description": "Chemin du fichier MP4",
        "type": "string"
      }
    },
    "required": [
      "mp4_file",
      "mode"
    ],
    "type": "object"
  }
}

import subprocess
import base64
import re

def main(args):
    mp4_file = args.get('mp4_file', 'finderskeepers.mp4')
    mode = args.get('mode', 'full')
    
    results = []
    
    if mode in ['metadata', 'full']:
        # Extraire toutes les chaînes et métadonnées
        results.append("=== MÉTADONNÉES ===")
        try:
            result = subprocess.run(['strings', mp4_file], capture_output=True, text=True, timeout=30)
            strings = result.stdout.split('\n')
            
            # Chercher le Base64
            for s in strings:
                if len(s) > 20 and re.match(r'^[A-Za-z0-9+/=]+$', s):
                    try:
                        decoded = base64.b64decode(s).decode('utf-8', errors='ignore')
                        if '{' in decoded and '}' in decoded:
                            results.append(f"Base64 trouvé: {s}")
                            results.append(f"Décodé: {decoded}")
                    except:
                        pass
        except Exception as e:
            results.append(f"Erreur: {e}")
    
    if mode in ['lsb', 'full']:
        # Extraire les frames et analyser le LSB
        results.append("\n=== ANALYSE LSB ===")
        try:
            # Utiliser ffmpeg pour extraire les frames
            subprocess.run(['ffmpeg', '-i', mp4_file, '-vf', 'fps=1', 'frame_%04d.png'], 
                          capture_output=True, timeout=60)
            
            # Analyser le LSB de la première frame
            import os
            frames = sorted([f for f in os.listdir('.') if f.startswith('frame_') and f.endswith('.png')])
            
            if frames:
                results.append(f"Nombre de frames: {len(frames)}")
                
                # Lire la première frame et extraire le LSB
                from PIL import Image
                img = Image.open(frames[0])
                pixels = list(img.getdata())
                
                # Extraire les bits LSB
                lsb_bits = []
                for pixel in pixels[:1000]:  # Premier millier de pixels
                    if isinstance(pixel, tuple):
                        for channel in pixel[:3]:  # RGB
                            lsb_bits.append(channel & 1)
                    else:
                        lsb_bits.append(pixel & 1)
                
                # Convertir en bytes
                lsb_bytes = []
                for i in range(0, len(lsb_bits) - 7, 8):
                    byte = 0
                    for j in range(8):
                        byte = (byte << 1) | lsb_bits[i + j]
                    lsb_bytes.append(byte)
                
                # Essayer de décoder en texte
                try:
                    lsb_text = bytes(lsb_bytes).decode('utf-8', errors='ignore')
                    results.append(f"LSB texte: {lsb_text[:100]}")
                except:
                    results.append(f"LSB bytes: {lsb_bytes[:20]}")
            else:
                results.append("Aucune frame extraite")
                
        except Exception as e:
            results.append(f"Erreur LSB: {e}")
    
    if mode == 'strings':
        results.append("=== CHAÎNES UNIQUE ===")
        try:
            result = subprocess.run(['strings', mp4_file], capture_output=True, text=True, timeout=30)
            # Filtrer les chaînes intéressantes
            interesting = [s for s in result.stdout.split('\n') if len(s) > 10 and any(c.isalpha() for c in s)]
            results.extend(interesting[:50])
        except Exception as e:
            results.append(f"Erreur: {e}")
    
    return '\n'.join(results)

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
