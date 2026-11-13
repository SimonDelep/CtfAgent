import base64

# La chaîne suspecte
s = "SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j"
print(f"Longueur: {len(s)}")

# Essayons de décoder en Base64 standard (remplacer - par + et _ par /)
s_std = s.replace('-', '+').replace('_', '/')
print(f"Après remplacement: {s_std}")

# Ajouter padding si nécessaire
padding = (4 - len(s_std) % 4) % 4
s_padded = s_std + '=' * padding
print(f"Avec padding: {s_padded}")

try:
    decoded = base64.b64decode(s_padded)
    print(f"Décodé (bytes): {decoded}")
    print(f"Décodé (hex): {decoded.hex()}")
    try:
        print(f"Décodé (str): {decoded.decode('utf-8')}")
    except:
        print("Pas un UTF-8 valide")
except Exception as e:
    print(f"Erreur: {e}")

# Essayons aussi URL-safe
try:
    decoded_url = base64.urlsafe_b64decode(s + '==')  # Ajouter padding
    print(f"URL-safe décodé: {decoded_url}")
except Exception as e:
    print(f"Erreur URL-safe: {e}")