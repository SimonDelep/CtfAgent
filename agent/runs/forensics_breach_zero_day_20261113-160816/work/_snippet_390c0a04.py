import base64

pdq_str = "PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j"
print(f"Original: {pdq_str}")

# Essai Base64 standard
try:
    decoded = base64.b64decode(pdq_str)
    print(f"Base64 standard: {decoded}")
except Exception as e:
    print(f"Base64 standard échec: {e}")

# Essai Base64 URL-safe
try:
    decoded_url = base64.urlsafe_b64decode(pdq_str)
    print(f"Base64 URL-safe: {decoded_url}")
except Exception as e:
    print(f"Base64 URL-safe échec: {e}")

# Essai avec padding
pdq_padded = pdq_str + "=" * (4 - len(pdq_str) % 4) if len(pdq_str) % 4 else pdq_str
print(f"Avec padding: {pdq_padded}")
try:
    decoded_padded = base64.urlsafe_b64decode(pdq_padded)
    print(f"Base64 URL-safe avec padding: {decoded_padded}")
except Exception as e:
    print(f"Échec avec padding: {e}")