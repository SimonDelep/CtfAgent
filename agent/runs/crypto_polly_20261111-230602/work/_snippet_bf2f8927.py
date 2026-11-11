import socket
import time

def connect_and_interact(x_input, plaintext):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    try:
        s.connect(("polly.chal.csaw.io", 5000))
        data = s.recv(1024).decode()
        print("Initial data:", data[:200])
        
        # Send x_input
        s.sendall((str(x_input) + "\n").encode())
        time.sleep(0.1)
        
        # Receive prompt
        data = s.recv(1024).decode()
        print("After x_input:", data[:200])
        
        # Send plaintext
        s.sendall((plaintext + "\n").encode())
        time.sleep(0.1)
        
        # Receive response
        data = s.recv(1024).decode()
        print("Response:", data)
        
        s.close()
        return data
    except Exception as e:
        print("Error:", e)
        return None

# Try with x=0
result = connect_and_interact(0, "A" * 40)