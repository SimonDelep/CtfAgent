import base64
import re

with open('audio.wav', 'rb') as f:
    data = f.read()

b64_pattern = rb'[A-Za-z0-9+/]{4,}={0,2}'
matches = re.findall(b64_pattern, data)

decoded_parts = []
for m in matches:
    try:
        padded = m + b'=' * (4 - len(m) % 4) if len(m) % 4 else m
        decoded = base64.b64decode(padded)
        decoded_parts.append(decoded)
    except:
        pass

full_payload = b''.join(decoded_parts)

print(f"Taille: {len(full_payload)}")
print(f"Hex des premiers 50 octets: {full_payload[:50].hex()}")
print(f"Début du payload (repr): {repr(full_payload[:50])}")

# Chercher le motif '2_5t3@1_' dans le payload
target = b'2_5t3@1_'
positions = []
start = 0
while True:
    pos = full_payload.find(target, start)
    if pos == -1:
        break
    positions.append(pos)
    start = pos + 1

print(f"\nPositions de '2_5t3@1_': {positions}")

# Chercher aussi qsTDRC décodé = \xaa\xc4\xc3D
key = bytes([0xaa, 0xc4, 0xc3, 0x44])
pos_key = full_payload.find(key)
print(f"Position de la clé \\xaa\\xc4\\xc3D: {pos_key}")

# Afficher le contexte autour de chaque occurrence
for pos in positions:
    start_ctx = max(0, pos - 10)
    end_ctx = min(len(full_payload), pos + len(target) + 10)
    print(f"Contexte à pos {pos}: {repr(full_payload[start_ctx:end_ctx])}")