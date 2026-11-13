import socket

def send_recv(host, port, commands):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.settimeout(5)
    
    data = s.recv(1024).decode()
    print("Initial:", repr(data))
    
    for cmd in commands:
        s.send((cmd + "\n").encode())
        import time
        time.sleep(0.1)
        try:
            resp = s.recv(1024).decode()
            print(f"After '{cmd}':", repr(resp))
        except:
            print(f"After '{cmd}': (timeout)")
    
    s.close()

send_recv("saint-vespers-and-the-copper-choir.chal.csaw.io", 5000, ["1", "A", "0", "10", "test", "9"])