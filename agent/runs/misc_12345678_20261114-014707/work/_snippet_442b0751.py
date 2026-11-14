# Cherchons 'qsTDRC' dans le fichier audio
with open('audio.wav', 'rb') as f:
    data = f.read()

# Chercher 'qsTDRC' en tant que chaîne
idx = data.find(b'qsTDRC')
if idx != -1:
    print(f"'qsTDRC' trouvé à la position {idx}")
    print(f"Contexte: {data[idx-20:idx+30]!r}")
else:
    print("'qsTDRC' pas trouvé directement")

# Chercher 'Ml81dDNAMV8=' (Base64 de '2_5t3@1_')
idx2 = data.find(b'Ml81dDNAMV8=')
if idx2 != -1:
    print(f"\n'Ml81dDNAMV8=' trouvé à la position {idx2}")
    print(f"Contexte: {data[idx2-20:idx2+30]!r}")
else:
    print("'Ml81dDNAMV8=' pas trouvé directement")