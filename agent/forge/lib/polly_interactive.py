SCHEMA = {
  "name": "polly_interactive",
  "description": "Client interactif complet pour Polly : récupère le nonce initial, le ciphertext du flag, et permet de faire des requêtes (x, plaintext) pour obtenir (ciphertext, nonce_byte)",
  "parameters": {
    "properties": {
      "host": {
        "type": "string"
      },
      "plaintext": {
        "type": "string"
      },
      "port": {
        "type": "integer"
      },
      "x": {
        "type": "integer"
      }
    },
    "required": [
      "host",
      "port",
      "x",
      "plaintext"
    ],
    "type": "object"
  }
}

import socket

def main(args):
    host = args["host"]
    port = args["port"]
    x = args["x"]
    plaintext = args["plaintext"]
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((host, port))
        
        # Recevoir le message initial (nonce et ciphertext du flag)
        initial = b""
        while b"perhaps theirs a way" not in initial:
            chunk = sock.recv(4096)
            if not chunk:
                break
            initial += chunk
        
        # Envoyer x
        sock.sendall(f"{x}\n".encode())
        
        # Recevoir le prompt "enter a string"
        prompt = b""
        while b"enter a string" not in prompt:
            chunk = sock.recv(4096)
            if not chunk:
                break
            prompt += chunk
        
        # Envoyer le plaintext
        sock.sendall(f"{plaintext}\n".encode())
        
        # Recevoir la réponse
        response = b""
        while True:
            sock.settimeout(2)
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
            except socket.timeout:
                break
        
        sock.close()
        
        return f"INITIAL:\n{initial.decode('utf-8', errors='replace')}\n\nRESPONSE:\n{response.decode('utf-8', errors='replace')}"
    
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
