SCHEMA = {
  "name": "vespers_interactive_client",
  "description": "Client interactif pour le service vespers. Envoie des commandes et retourne la réponse. Permet de tester les opérations du choeur.",
  "parameters": {
    "properties": {
      "binary_mode": {
        "description": "Si vrai, lit les réponses binaires sans décoder UTF-8",
        "type": "boolean"
      },
      "commands": {
        "description": "Liste des commandes à envoyer (une par ligne)",
        "items": {
          "type": "string"
        },
        "type": "array"
      },
      "host": {
        "description": "Hostname du service",
        "type": "string"
      },
      "port": {
        "description": "Port du service",
        "type": "integer"
      }
    },
    "type": "object"
  }
}

import socket
import sys

def main(args):
    host = args.get("host", "saint-vespers-and-the-copper-choir.chal.csaw.io")
    port = args.get("port", 5000)
    commands = args.get("commands", [])
    binary_mode = args.get("binary_mode", False)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((host, port))
        
        # Lire le message d'accueil
        data = b""
        while True:
            chunk = sock.recv(1024)
            if not chunk:
                break
            data += chunk
            if b"> " in data or b"choir" in data.lower():
                break
        
        if binary_mode:
            print("Initial:", repr(data))
        else:
            print("Initial:", data.decode('utf-8', errors='replace'))
        
        for cmd in commands:
            sock.sendall((cmd + "\n").encode())
            # Lire la réponse
            data = b""
            while True:
                sock.settimeout(2)
                try:
                    chunk = sock.recv(1024)
                    if not chunk:
                        break
                    data += chunk
                    if b"> " in data:
                        break
                except socket.timeout:
                    break
            
            if binary_mode:
                print(f"Après '{cmd}':", repr(data))
            else:
                print(f"Après '{cmd}':", data.decode('utf-8', errors='replace'))
        
        sock.close()
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
