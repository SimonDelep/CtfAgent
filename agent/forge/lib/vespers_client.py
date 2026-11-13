SCHEMA = {
  "name": "vespers_client",
  "description": "Client interactif pour le service vespers. Envoie des commandes et retourne la réponse.",
  "parameters": {
    "commands": {
      "description": "Liste des commandes à envoyer (une par ligne)",
      "items": {
        "type": "string"
      },
      "type": "array"
    },
    "host": {
      "type": "string"
    },
    "port": {
      "type": "integer"
    }
  }
}

import socket
import sys

def main(args):
    host = args.get('host', 'saint-vespers-and-the-copper-choir.chal.csaw.io')
    port = args.get('port', 5000)
    commands = args.get('commands', [])
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((host, port))
        
        # Lire le prompt initial
        data = s.recv(4096).decode('utf-8', errors='replace')
        result = "Initial: " + data[:200] + "\n"
        
        for cmd in commands:
            s.send((cmd + '\n').encode())
            s.settimeout(2)
            try:
                resp = s.recv(4096).decode('utf-8', errors='replace')
                result += f"> {cmd}\n{resp}\n"
            except socket.timeout:
                result += f"> {cmd} (timeout)\n"
        
        s.close()
        return result
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
