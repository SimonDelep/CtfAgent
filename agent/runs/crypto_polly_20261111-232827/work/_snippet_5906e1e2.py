import socket
try:
    ip = socket.gethostbyname("polly.chal.csaw.io")
    print(f"IP: {ip}")
except Exception as e:
    print(f"Error: {e}")