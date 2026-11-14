import base64

# qsTDRC est une chaîne Base64 qui décode en \xaa\xc4\xc3D
# Mais peut-être que qsTDRC lui-même est un indice

# Regardons si qsTDRC est un mot ou un acronyme
qsTDRD = "qsTDRC"
print(f"qsTDRC: {qsTDRD}")

# Peut-être que c'est "qs" + "TDRC" ou "q" + "sTDRC"
# Ou peut-être que c'est une clé XOR

# Essayons de voir si qsTDRC XOR avec quelque chose donne un texte lisible
# Ou peut-être que qsTDRC est le reste du flag après 2_5t3@1_

# Regardons la structure du flag:
# 2_5t3@1_ semble être un pattern de 8 caractères
# Peut-être que le flag complet est plus long

# D'après le résumé, il y a 57 chaînes Base64
# Peut-être que certaines chaînes contiennent des parties du flag

# Cherchons des chaînes qui pourraient contenir 'csaw' ou des parties de flag
# en les décodant différemment

# Essayons de décoder les chaînes en utilisant d'autres encodages
# Ou peut-être que le flag est caché dans les données audio elles-mêmes

# Regardons les données audio brutes pour trouver 'csaw' ou 'flag'
with open('audio.wav', 'rb') as f:
    data = f.read()

# Chercher 'csaw' en cherchant chaque caractère
# Peut-être que c'est encodé différemment

# Essayons de chercher 'csaw' en XOR avec une clé simple
for key in range(256):
    decoded = bytes([b ^ key for b in data[:100]])
    if b'csaw' in decoded:
        print(f"Trouvé avec XOR key {key}: {decoded[:20]}")

# Chercher aussi 'flag'
for key in range(256):
    decoded = bytes([b ^ key for b in data[:100]])
    if b'flag' in decoded:
        print(f"Trouvé 'flag' avec XOR key {key}: {decoded[:20]}")