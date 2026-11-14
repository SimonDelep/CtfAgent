import base64
import re

with open('audio.wav', 'rb') as f:
    data = f.read()

b64_pattern = rb'[A-Za-z0-9+/]{4,}={0,2}'
matches = re.findall(b64_pattern, data)

print(f"Total {len(matches)} chaînes Base64:\n")

for i, m in enumerate(matches):
    try:
        padded = m + b'=' * (4 - len(m) % 4) if len(m) % 4 else m
        decoded = base64.b64decode(padded)
        # Afficher la chaîne et son décodage
        try:
            text = decoded.decode('ascii', errors='replace')
            printable = all(c.isprintable() or c in '\n\r\t' for c in text)
            if printable:
                print(f"{i:2}: {m.decode('ascii'):20} -> {repr(text)}")
            else:
                print(f"{i:2}: {m.decode('ascii'):20} -> [binaire] {decoded[:20].hex()}...")
        except:
            print(f"{i:2}: {m.decode('ascii'):20} -> [binaire] {decoded[:20].hex()}...")
    except Exception as e:
        print(f"{i:2}: {m.decode('ascii'):20} -> ERROR: {e}")