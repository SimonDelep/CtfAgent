import base64

# Token suspect
token = "SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j"

# Essai de décodage Base64 URL-safe
try:
    # Remplacer - et _ par + et /
    padded = token + "=" * (4 - len(token) % 4) if len(token) % 4 else token
    decoded = base64.urlsafe_b64decode(padded)
    print(f"Base64 URL-safe décodé: {decoded}")
    print(f"En hex: {decoded.hex()}")
except Exception as e:
    print(f"Erreur Base64: {e}")

# Essai simple Base64
try:
    decoded_std = base64.b64decode(token + "==")
    print(f"Base64 standard: {decoded_std}")
except Exception as e:
    print(f"Erreur Base64 std: {e}")

# Les chaînes majuscules
strings = ["DIHWTROXP", "TGCPAQYTAH", "HJKSYJGAM", "AncillaryDynamics"]
for s in strings:
    print(f"\n{ s }:")
    # ROT13
    rot13 = ''.join(chr((ord(c) - 65 + 13) % 26 + 65) if c.isupper() else 
                    chr((ord(c) - 97 + 13) % 26 + 97) if c.islower() else c for c in s)
    print(f"  ROT13: {rot13}")