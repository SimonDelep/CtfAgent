SCHEMA = {
  "name": "polly_client",
  "description": "Connecte au service Polly, envoie x et un plaintext, retourne le nonce et le ciphertext",
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
    host = args.get("host", "polly.chal.csaw.io")
    port = args.get("port", 5000)
    x = args.get("x", 0)
    plaintext = args.get("plaintext", "test")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        
        # Lire le message initial
        data = b""
        while b"perhaps theirs a way" not in data:
            chunk = sock.recv(1024)
            if not chunk:
                break
            data += chunk
        
        # Envoyer x
        sock.sendall(f"{x}\n".encode())
        
        # Lire le prompt
        data = b""
        while b"enter a string" not in data:
            chunk = sock.recv(1024)
            if not chunk:
                break
            data += chunk
        
        # Envoyer le plaintext
        sock.sendall(f"{plaintext}\n".encode())
        
        # Lire la réponse
        data = b""
        for _ in range(5):
            chunk = sock.recv(1024)
            if not chunk:
                break
            data += chunk
        
        sock.close()
        
        # Parser la réponse
        result = {}
        lines = data.decode("latin-1").split("\n")
        for line in lines:
            if "ciphertext is:" in line:
                ct = line.split("ciphertext is:")[1].strip()
                result["ciphertext"] = ct
            if "nonce byte is:" in line:
                nb = line.split("nonce byte is:")[1].strip()
                result["nonce_byte"] = nb
        
        return str(result)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
