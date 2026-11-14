# Analyser plus en détail le contenu ID3
with open('audio.wav', 'rb') as f:
    data = f.read()

id3_pos = 6064294
id3_content = data[id3_pos+10:id3_pos+10+35]  # 35 octets de contenu

print(f"Contenu ID3 complet ({len(id3_content)} octets):")
print(f"Hex: {id3_content.hex()}")
print(f"Repr: {repr(id3_content)}")

# La structure semble être:
# - Quelques octets de padding/métadonnées
# - 'qsTDRC' (description)
# - Null bytes
# - 'Ml81dDNAMV8=' (valeur)

# Chercher 'qsTDRC'
desc_pos = id3_content.find(b'qsTDRC')
print(f"\nPosition de 'qsTDRC': {desc_pos}")

# Chercher 'Ml81dDNAMV8='
val_pos = id3_content.find(b'Ml81dDNAMV8=')
print(f"Position de 'Ml81dDNAMV8=': {val_pos}")

# Afficher le contexte
if desc_pos != -1:
    print(f"Contexte autour de 'qsTDRC': {repr(id3_content[max(0,desc_pos-5):desc_pos+15])}")
if val_pos != -1:
    print(f"Contexte autour de 'Ml81dDNAMV8=': {repr(id3_content[max(0,val_pos-5):val_pos+20])}")

# Peut-être que le flag est simplement 'csaw{2_5t3@1_}'
# Mais vérifions aussi si 'qsTDRC' pourrait être une clé pour décoder quelque chose

# Regardons si 'qsTDRC' décodé en Base64 donne quelque chose
import base64
try:
    decoded_qs = base64.b64decode('qsTDRC' + '==')
    print(f"\n'qsTDRC' décodé Base64: {repr(decoded_qs)}")
    print(f"Hex: {decoded_qs.hex()}")
except Exception as e:
    print(f"Erreur décodage 'qsTDRC': {e}")