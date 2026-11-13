import base64

# La chaîne PDQ suspecte
pdq_str = "PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j"
encoded_part = "SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j"

# Essai Base64 standard
try:
    decoded = base64.b64decode(encoded_part + '==')
    print(f"Base64 standard: {decoded}")
except Exception as e:
    print(f"Base64 échec: {e}")

# Essai Base64 URL-safe
try:
    decoded_url = base64.urlsafe_b64decode(encoded_part + '==')
    print(f"Base64 URL-safe: {decoded_url}")
except Exception as e:
    print(f"Base64 URL-safe échec: {e}")

# Essai avec padding différent
for padding in ['', '=', '==', '===']:
    try:
        decoded = base64.b64decode(encoded_part + padding)
        print(f"Padding '{padding}': {decoded}")
    except:
        pass