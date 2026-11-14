import base64

# La chaîne qsTDRC décode en \xaa\xc4\xc3D
# Peut-être que c'est une clé XOR ou quelque chose comme ça

qsTDRD_decoded = bytes.fromhex('aac4c344')
print(f"qsTDRC décodé: {qsTDRD_decoded.hex()}")

# Peut-être que le flag est construit en utilisant cette clé
# Ou peut-être que 'qsTDRC' est lui-même une partie du flag

# Regardons aussi les autres chaînes qui ont un pattern similaire
# Beaucoup de chaînes ont un pattern de 4 caractères comme 'F5A5', 'u2q2', etc.

# Peut-être que le flag est simplement 'csaw{2_5t3@1_}' et qu'il faut le soumettre
# Mais le résumé dit que ça a déjà été essayé et refusé

# Essayons de voir si 'qsTDRC' contient un indice
print(f"\nqsTDRC en ASCII: {qsTDRD_decoded}")

# Peut-être que le flag est 'csaw{2_5t3@1_qsTDRC}' ou quelque chose comme ça
# Ou peut-être que 'qsTDRC' est le reste du flag

# Regardons la structure: 2_5t3@1_ semble être un pattern
# 2_5t3@1_ pourrait être '2_5t3@1_' = '2_5t3@1_'

# Peut-être que le flag complet est 'csaw{2_5t3@1_qsTDRC}'
# Ou 'csaw{2_5t3@1_+qsTDRC}'

# Essayons de soumettre quelques variantes
print("\nVariantes possibles:")
print("csaw{2_5t3@1_}")
print("csaw{2_5t3@1_qsTDRC}")
print("csaw{2_5t3@1_+qsTDRC}")
print("csaw{2_5t3@1_qsTDRD}")