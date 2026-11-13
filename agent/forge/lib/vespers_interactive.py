SCHEMA = {
  "name": "vespers_interactive",
  "description": "Client interactif pour le service vespers local. Envoie une séquence de commandes et retourne la réponse complète. Gère les encodages binaires.",
  "parameters": {
    "properties": {
      "binary_path": {
        "description": "Chemin vers le binaire vespers",
        "type": "string"
      },
      "commands": {
        "description": "Liste des commandes à envoyer (une par ligne)",
        "items": {
          "type": "string"
        },
        "type": "array"
      }
    },
    "required": [
      "commands",
      "binary_path"
    ],
    "type": "object"
  }
}

import subprocess
import sys

def main(args):
    commands = args.get("commands", [])
    binary_path = args.get("binary_path", "./vespers")
    
    # Préparer les entrées avec des nouveaux lignes
    input_data = "\n".join(commands) + "\n"
    
    try:
        # Lancer le processus
        proc = subprocess.Popen(
            [binary_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd="."
        )
        
        # Envoyer les commandes
        stdout, stderr = proc.communicate(input=input_data.encode('latin-1'), timeout=5)
        
        # Décoder la sortie en gérant les erreurs
        try:
            output = stdout.decode('utf-8', errors='replace')
        except:
            output = stdout.decode('latin-1', errors='replace')
        
        return f"Exit code: {proc.returncode}\n--- Output ---\n{output}\n--- Stderr ---\n{stderr.decode('utf-8', errors='replace') if stderr else ''}"
    except subprocess.TimeoutExpired:
        proc.kill()
        return "Timeout!"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
