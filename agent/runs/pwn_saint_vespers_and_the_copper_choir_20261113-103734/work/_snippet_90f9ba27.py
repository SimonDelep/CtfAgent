import socket

host = 'saint-vespers-and-the-copper-choir.chal.csaw.io'
port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5)
sock.connect((host, port))

def recv_all(sock, timeout=2):
    sock.settimeout(timeout)
    data = b''
    while True:
        try:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
        except socket.timeout:
            break
    return data

# Lire le prompt initial
print("Initial recv:")
data = recv_all(sock)
print(repr(data))

# Recruter un chorister
print("\nSending: 1")
sock.sendall(b'1\n')
data = recv_all(sock)
print("Recv:", repr(data))

print("\nSending: TestChorister")
sock.sendall(b'TestChorister\n')
data = recv_all(sock)
print("Recv:", repr(data))

print("\nSending: 0")
sock.sendall(b'0\n')
data = recv_all(sock)
print("Recv:", repr(data))

print("\nSending: 10")
sock.sendall(b'10\n')
data = recv_all(sock)
print("Recv:", repr(data))

print("\nSending: AAAAAAAAAA (10 bytes)")
sock.sendall(b'AAAAAAAAAA\n')
data = recv_all(sock)
print("Recv:", repr(data))

# Voir la roster
print("\nSending: 7")
sock.sendall(b'7\n')
data = recv_all(sock)
print("Recv:", repr(data))

sock.close()