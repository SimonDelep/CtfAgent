import base64

target = '2_5t3@1_'

# Essayer de voir si c'est du Base32
try:
    # Base32 utilise A-Z et 2-7, pas de '_' ou '@'
    # Donc ce n'est probablement pas du Base32 direct
    decoded_b32 = base64.b32decode(target.upper() + '===')
    print(f"Base32: {decoded_b32}")
except Exception as e:
    print(f"Base32 échec: {e}")

# Peut-être que c'est une substitution simple
# '2_5t3@1_' - 8 caractères
# Si c'est un flag, il pourrait être 'csaw{...}'
# csaw{} = 6 caractères, donc pas directement

# Regardons les valeurs ASCII
print(f"\nValeurs ASCII de '2_5t3@1_':")
for c in target:
    print(f"  '{c}' = {ord(c)} = 0x{ord(c):02x}")

# Peut-être que le flag est 'csaw{2_5t3@1_}'
# Ou peut-être qu'il faut lire les métadonnées ID3 plus en détail