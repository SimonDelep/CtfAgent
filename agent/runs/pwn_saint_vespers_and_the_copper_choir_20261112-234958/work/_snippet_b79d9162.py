import socket
import time

host = "saint-vespers-and-the-copper-choir.chal.csaw.io"
port = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
s.connect((host, port))

# Recevoir le message d'accueil
data = s.recv(4096).decode('utf-8', errors='replace')
print("=== Initial banner ===")
print(data)

# Recruter un chorister
s.send(b"1\n")
time.sleep(0.2)
data = s.recv(4096).decode('utf-8', errors='replace')
print("=== After '1' ===")
print(data)

# Nom
s.send(b"A\n")
time.sleep(0.2)
data = s.recv(4096).decode('utf-8', errors='replace')
print("=== After name ===")
print(data)

# Style
s.send(b"0\n")
time.sleep(0.2)
data = s.recv(4096).decode('utf-8', errors='replace')
print("=== After style ===")
print(data)

# Longueur
s.send(b"10\n")
time.sleep(0.2)
data = s.recv(4096).decode('utf-8', errors='replace')
print("=== After length ===")
print(data)

# Transcript
s.send(b"AAAAAAAAAA\n")
time.sleep(0.2)
data = s.recv(4096).decode('utf-8', errors='replace')
print("=== After transcript ===")
print(data)

# Voir la liste
s.send(b"7\n")
time.sleep(0.2)
data = s.recv(4096).decode('utf-8', errors='replace')
print("=== After roster ===")
print(data)

s.close()