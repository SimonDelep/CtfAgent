import base64

# Chaînes en majuscules trouvées
strings = ["DIHWTROXP", "TGCPAQYTAH"]

for s in strings:
    print(f"Original: {s}")
    
    # Essayer ROT13
    rot13 = ''.join(chr((ord(c) - 65 + 13) % 26 + 65) if c.isupper() else c for c in s)
    print(f"  ROT13: {rot13}")
    
    # Essayer Base64
    try:
        # Ajouter padding
        s_padded = s + '=' * (4 - len(s) % 4) if len(s) % 4 != 0 else s
        decoded = base64.b64decode(s_padded)
        print(f"  Base64 decoded: {decoded}")
    except Exception as e:
        print(f"  Base64 failed: {e}")
    
    # Essayer Base64 URL-safe
    try:
        s_std = s.replace('-', '+').replace('_', '/')
        s_padded = s_std + '=' * (4 - len(s_std) % 4) if len(s_std) % 4 != 0 else s_std
        decoded = base64.b64decode(s_padded)
        print(f"  Base64 URL-safe decoded: {decoded}")
    except Exception as e:
        print(f"  Base64 URL-safe failed: {e}")
    
    print()