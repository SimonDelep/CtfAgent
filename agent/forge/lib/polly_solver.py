SCHEMA = {
  "name": "polly_solver",
  "description": "Connecte au service Polly, collecte les données (x, state_at) et résout le seed en utilisant l'algèbre linéaire sur GF(2) en pur Python",
  "parameters": {
    "properties": {
      "host": {
        "description": "hostname du service",
        "type": "string"
      },
      "port": {
        "description": "port du service",
        "type": "integer"
      }
    },
    "required": [
      "host",
      "port"
    ],
    "type": "object"
  }
}

def main(args):
    import socket
    
    HOST = args.get("host", "polly.chal.csaw.io")
    PORT = args.get("port", 5000)
    
    def recv_all(sock, n):
        data = b""
        while len(data) < n:
            chunk = sock.recv(n - len(data))
            if not chunk:
                break
            data += chunk
        return data
    
    def recv_line(sock):
        line = b""
        while True:
            byte = sock.recv(1)
            if not byte:
                break
            line += byte
            if byte == b'\n':
                break
        return line
    
    def send_line(sock, line):
        sock.send((line + "\n").encode())
    
    # Connexion
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    
    # Lire l'intro
    intro = recv_line(sock)
    intro += recv_line(sock)
    intro += recv_line(sock)
    intro += recv_line(sock)
    intro += recv_line(sock)
    intro += recv_line(sock)
    
    # Extraire le ciphertext et nonce initiaux
    lines = intro.decode().split('\n')
    ciphertext_hex = None
    nonce_hex = None
    for line in lines:
        if "encrypted flag is" in line:
            parts = line.split()
            for i, p in enumerate(parts):
                if p == "is":
                    ciphertext_hex = parts[i+1].rstrip(',')
                if p == "nonce":
                    nonce_hex = parts[i+1]
    
    print(f"Initial ciphertext: {ciphertext_hex}")
    print(f"Initial nonce: {nonce_hex}")
    
    # Collecter des paires (x, last_byte_of_nonce)
    # Le last byte du nonce est (state_at(x, seed) >> 16) & 0xFF
    
    results = {}
    
    # D'abord, envoyons x = 0
    send_line(sock, "0")
    recv_line(sock)  # "enter a string to be encrypted: "
    send_line(sock, "A" * 20)
    response = recv_line(sock)
    print(f"Response for x=0: {response.decode().strip()}")
    
    # Continuons avec d'autres x
    for i in range(1, 10):
        x = 1 << i
        send_line(sock, str(x))
        recv_line(sock)
        send_line(sock, "B" * 20)
        response = recv_line(sock)
        print(f"Response for x={x}: {response.decode().strip()}")
    
    sock.close()
    return "Done"

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
