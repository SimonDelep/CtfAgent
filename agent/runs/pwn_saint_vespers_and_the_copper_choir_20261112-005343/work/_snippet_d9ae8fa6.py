import socket

host = "saint-vespers-and-the-copper-choir.chal.csaw.io"
port = 5000

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((host, port))
    data = s.recv(1024)
    print("Received:", repr(data))
    s.close()
except Exception as e:
    print("Error:", e)