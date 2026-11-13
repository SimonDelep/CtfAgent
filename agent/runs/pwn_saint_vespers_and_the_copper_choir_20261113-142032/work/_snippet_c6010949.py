import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect(('saint-vespers-and-the-copper-choir.chal.csaw.io', 5000))
    print("Connected!")
    
    # Recevoir le message initial
    data = b''
    while b'> ' not in data:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
    print("Initial:", data.decode(errors='replace')[:200])
    
    # Menu
    sock.sendall(b'1\n')  # Recruter
    data = b''
    while b':' not in data:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
    print("After recruit:", data.decode(errors='replace'))
    
    sock.sendall(b'TestChorister\n')
    data = b''
    while b':' not in data:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
    print("After name:", data.decode(errors='replace'))
    
    sock.sendall(b'0\n')
    data = b''
    while b':' not in data:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
    print("After style:", data.decode(errors='replace'))
    
    sock.sendall(b'10\n')
    data = b''
    while b':' not in data:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
    print("After len:", data.decode(errors='replace'))
    
    sock.sendall(b'ABCDEFGHIJ\n')  # 10 bytes + newline
    data = b''
    timeout = 2
    sock.settimeout(timeout)
    try:
        while b'position' not in data:
            chunk = sock.recv(1024)
            if not chunk:
                break
            data += chunk
    except:
        pass
    print("After transcript:", data.decode(errors='replace'))
    
    sock.close()
except Exception as e:
    print(f"Error: {e}")