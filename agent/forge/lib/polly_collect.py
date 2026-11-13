SCHEMA = {
  "name": "polly_collect",
  "description": "Connecte au service Polly et collecte les bytes de nonce pour différents x",
  "parameters": {
    "properties": {
      "host": {
        "type": "string"
      },
      "port": {
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
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((HOST, PORT))
    
    # Lire l'intro (6 lignes)
    initial_info = []
    for _ in range(6):
        line = recv_line(sock)
        initial_info.append(line.decode().strip())
        print(f"INIT: {line.decode().strip()}")
    
    # Extraire ciphertext et nonce initial
    ciphertext_hex = None
    nonce_hex = None
    for line in initial_info:
        if "encrypted flag is" in line:
            parts = line.split()
            for i, p in enumerate(parts):
                if p == "is" and i+1 < len(parts):
                    ciphertext_hex = parts[i+1].rstrip(',')
                if p == "nonce" and i+1 < len(parts):
                    nonce_hex = parts[i+1]
    
    print(f"\n=== Initial state ===")
    print(f"Ciphertext: {ciphertext_hex}")
    print(f"Nonce: {nonce_hex}")
    
    # Collecter les bytes de nonce pour x = 0, 1, 2, 4, 8, 16, 32, 64, 128, 256
    # Chaque x donne (state_at(x, seed) >> 16) & 0xFF
    collected = {}
    
    test_xs = [0] + [1 << i for i in range(8)]
    
    for x in test_xs:
        send_line(sock, str(x))
        prompt = recv_line(sock)  # "enter a string to be encrypted: "
        send_line(sock, "X" * 32)
        response = recv_line(sock)
        response_str = response.decode().strip()
        print(f"x={x}: {response_str}")
        
        # Extraire le nonce byte
        if "Your nonce byte is:" in response_str:
            nonce_byte_hex = response_str.split("Your nonce byte is:")[1].strip()
            collected[x] = int(nonce_byte_hex, 16)
            print(f"  -> nonce_byte = 0x{nonce_byte_hex:02x} = {collected[x]}")
    
    sock.close()
    
    print(f"\n=== Collected data ===")
    for x, b in collected.items():
        print(f"x={x}: byte=0x{b:02x} ({b})")
    
    return collected

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
