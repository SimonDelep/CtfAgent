import base64

# La chaîne PDQ
pdq_str = "SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j"
print(f"PDQ string: {pdq_str}")

# Essayer de décoder en base64 (remplacer - par + et _ par /)
pdq_modified = pdq_str.replace('-', '+').replace('_', '/')
# Ajouter padding si nécessaire
padding = 4 - (len(pdq_modified) % 4)
if padding != 4:
    pdq_modified += '=' * padding

print(f"Modified for base64: {pdq_modified}")

try:
    decoded = base64.b64decode(pdq_modified)
    print(f"Decoded bytes: {decoded}")
    print(f"Decoded hex: {decoded.hex()}")
    try:
        print(f"Decoded ascii: {decoded.decode('ascii')}")
    except:
        print("Not ASCII")
except Exception as e:
    print(f"Base64 decode error: {e}")