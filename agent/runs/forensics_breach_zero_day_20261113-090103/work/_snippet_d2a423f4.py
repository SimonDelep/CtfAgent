import base64

# La chaîne PDQ=... du memdump
encoded = "SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j"

# Essai de décodage Base64 URL-safe
try:
    # Ajouter le padding si nécessaire
    padded = encoded + '=' * (4 - len(encoded) % 4) if len(encoded) % 4 else encoded
    decoded = base64.urlsafe_b64decode(padded)
    print(f"Base64 URL-safe décodé: {decoded}")
    print(f"En hex: {decoded.hex()}")
except Exception as e:
    print(f"Erreur Base64: {e}")

# Essai de décodage Base64 standard
try:
    # Remplacer - et _ par + et /
    standard = encoded.replace('-', '+').replace('_', '/')
    padded = standard + '=' * (4 - len(standard) % 4) if len(standard) % 4 else standard
    decoded = base64.b64decode(padded)
    print(f"Base64 standard décodé: {decoded}")
    print(f"En hex: {decoded.hex()}")
except Exception as e:
    print(f"Erreur Base64 standard: {e}")