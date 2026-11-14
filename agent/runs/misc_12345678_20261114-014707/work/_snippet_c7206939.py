# Essayons de trouver une clé qui transforme '2_5t3@1_' en 'csaw{...}'
# Mais '2_5t3@1_' a 8 caractères, et 'csaw{' a 5 caractères. Donc peut-être que '2_5t3@1_' est le contenu entre accolades.

# Si le format est csaw{2_5t3@1_}, alors le contenu est '2_5t3@1_'
# Mais ce n'est pas le bon flag selon la soumission précédente.

# Peut-être que le vrai flag est dans la partie binaire du payload, et qu'il faut la décoder différemment.

# Regardons le payload complet à nouveau
payload = b'\x8fH\xf4\xbf\xdb}\x93I\xf4\xc3\xdb\xbd\x97It\xcb\xdb=\x8bJ4,\x84\x93 \xd1N $C2_5t3@1_\xaa\xc4\xc3D2_5t3@1_'

# La partie avant '2_5t3@1_' est: \x8fH\xf4\xbf\xdb}\x93I\xf4\xc3\xdb\xbd\x97It\xcb\xdb=\x8bJ4,\x84\x93 \xd1N $C
# C'est 30 octets.

# Peut-être que ces 30 octets sont le flag XORé avec quelque chose.
# Ou peut-être que le flag est encodé en Base64 dans ces 30 octets?

# Essayons de voir si ces 30 octets, quand on les interprète comme du texte, donnent quelque chose
print("Partie binaire en ASCII (avec erreurs):")
print(payload[:30].decode('ascii', errors='replace'))

# Peut-être que le flag est caché dans les métadonnées ID3 de manière différente.
# Regardons le fichier WAV pour trouver d'autres indices.

import struct

with open('audio.wav', 'rb') as f:
    data = f.read()

# Trouvons la position de 'qsTDRC' dans le fichier
pos_qs = data.find(b'qsTDRC')
print(f"\nPosition de 'qsTDRC': {pos_qs}")

# Trouvons la position de 'Ml81dDNAMV8='
pos_m = data.find(b'Ml81dDNAMV8=')
print(f"Position de 'Ml81dDNAMV8=': {pos_m}")

# Regardons le contexte autour de ces positions
if pos_qs > 0:
    print(f"Contexte avant 'qsTDRC': {data[pos_qs-20:pos_qs]}")
    print(f"Contexte après 'qsTDRC': {data[pos_qs+6:pos_qs+26]}")

if pos_m > 0:
    print(f"Contexte avant 'Ml81dDNAMV8=': {data[pos_m-20:pos_m]}")
    print(f"Contexte après 'Ml81dDNAMV8=': {data[pos_m+12:pos_m+32]}")