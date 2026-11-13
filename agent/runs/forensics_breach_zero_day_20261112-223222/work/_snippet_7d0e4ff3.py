import base64

encoded = "PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j"
# Essai de décodage Base64 standard d'abord
try:
    decoded = base64.b64decode(encoded)
    print("Base64 standard:", decoded)
except Exception as e:
    print("Base64 standard échec:", e)

# Essai URL-safe (remplacer - par + et _ par /)
try:
    # La chaîne contient déjà = et -
    # Pour URL-safe, - devient + et _ devient /
    url_safe = encoded.replace('-', '+').replace('_', '/')
    # Ajouter padding si nécessaire
    padding = 4 - len(url_safe) % 4
    if padding != 4:
        url_safe += '=' * padding
    decoded_url = base64.b64decode(url_safe)
    print("Base64 URL-safe:", decoded_url)
except Exception as e:
    print("Base64 URL-safe échec:", e)

# Essai avec le padding original
try:
    # Garder le = original, remplacer - par +
    padded = encoded.replace('-', '+')
    decoded_padded = base64.b64decode(padded)
    print("Avec remplacement - par +:", decoded_padded)
except Exception as e:
    print("Échec:", e)