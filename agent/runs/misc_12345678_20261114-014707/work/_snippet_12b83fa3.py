import base64
import re

# Lire le fichier WAV
with open('audio.wav', 'rb') as f:
    data = f.read()

# Extraire toutes les chaînes Base64
b64_pattern = re.compile(r'[A-Za-z0-9+/]{4,}={0,2}')
matches = b64_pattern.findall(data.decode('latin-1'))

# Décode chaque chaîne et concaténer
full_payload = b''
for m in matches:
    try:
        padded = m + '=' * (4 - len(m) % 4) if len(m) % 4 else m
        decoded = base64.b64decode(padded)
        full_payload += decoded
    except:
        pass

# Le ciphertext est les 133 premiers octets
ciphertext = full_payload[:133]

# Essayons de voir si le ciphertext est lui-même du Base64 décodé
# Ou peut-être que c'est du texte XORé avec une clé répétitive

# Essayons de trouver un pattern de clé en supposant que le flag commence par "csaw{"
# Si plaintext = "csaw{..." et ciphertext = XOR(plaintext, key), alors key = XOR(ciphertext, "csaw{...")

target = b'csaw{'
key_candidate = bytes([ciphertext[i] ^ target[i] for i in range(len(target))])
print(f"Clé candidate (si plaintext commence par 'csaw{{'): {key_candidate}")
print(f"Clé candidate hex: {key_candidate.hex()}")

# Vérifions si cette clé se répète
print("\nVérification de la répétition de la clé:")
for i in range(0, len(ciphertext), len(key_candidate)):
    chunk = ciphertext[i:i+len(key_candidate)]
    decrypted = bytes([chunk[j] ^ key_candidate[j] for j in range(len(chunk))])
    print(f"  Position {i}: {decrypted}")

# Essayons aussi avec "csaw{" répété
key_extended = key_candidate * (len(ciphertext) // len(key_candidate) + 1)
decrypted = bytes([ciphertext[i] ^ key_extended[i] for i in range(len(ciphertext))])
print(f"\nDécrypté avec clé répétée: {decrypted[:50]}")

# Peut-être que la clé est "qsTDRC" en ASCII
key_qs = b'qsTDRC'
decrypted_qs = bytes([ciphertext[i] ^ key_qs[i % len(key_qs)] for i in range(len(ciphertext))])
print(f"\nDécrypté avec 'qsTDRC' répété: {decrypted_qs[:50]}")

# Ou peut-être que la clé est "2_5t3@1_"
key_25t = b'2_5t3@1_'
decrypted_25t = bytes([ciphertext[i] ^ key_25t[i % len(key_25t)] for i in range(len(ciphertext))])
print(f"\nDécrypté avec '2_5t3@1_' répété: {decrypted_25t[:50]}")