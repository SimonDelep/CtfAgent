import socket
try:
    ip = socket.gethostbyname("saint-vespers-and-the-copper-choir.chal.csaw.io")
    print("IP:", ip)
except Exception as e:
    print("DNS Error:", e)