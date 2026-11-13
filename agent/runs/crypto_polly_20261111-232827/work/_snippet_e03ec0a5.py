import socket
import hashlib
from Crypto.Hash import shake_256

def connect_and_get_nonce():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    try:
        sock.connect(("polly.chal.csaw.io", 5000))
        data = sock.recv(4096).decode()
        print("Initial data:")
        print(data)
        
        # Parse the nonce from the output
        # Format: "the nonce is {nonce.hex()} perhaps..."
        import re
        match = re.search(r'the nonce is ([a-f0-9]+)', data)
        if match:
            nonce_hex = match.group(1)
            print(f"Nonce hex: {nonce_hex}")
            return sock, nonce_hex
        sock.close()
    except Exception as e:
        print(f"Error: {e}")
    return None, None

sock, nonce_hex = connect_and_get_nonce()