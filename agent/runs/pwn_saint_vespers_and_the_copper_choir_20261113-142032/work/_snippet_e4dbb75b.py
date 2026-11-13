import socket

def send_recv(sock, data):
    sock.sendall(data.encode() if isinstance(data, str) else data)
    return sock.recv(4096).decode(errors='replace')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('saint-vespers-and-the-copper-choir.chal.csaw.io', 5000))
print("Connected!")

# Recevoir le message initial
print(sock.recv(1024).decode(errors='replace'))

# Menu
print(sock.recv(1024).decode(errors='replace'))

# Essai de recrutement
sock.sendall(b'1\n')  # Recruter
print(sock.recv(1024).decode(errors='replace'))

# Nom
sock.sendall(b'TestChorister\n')
print(sock.recv(1024).decode(errors='replace'))

# Style
sock.sendall(b'0\n')
print(sock.recv(1024).decode(errors='replace'))

# Longueur transcript
sock.sendall(b'10\n')
print(sock.recv(1024).decode(errors='replace'))

# Transcript
sock.sendall(b'0123456789\n')  # 10 bytes + newline
print(sock.recv(1024).decode(errors='replace'))

# Menu
print(sock.recv(1024).decode(errors='replace'))

sock.close()