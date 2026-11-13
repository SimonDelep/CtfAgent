# Analyser la structure de session.bin plus en détail
with open('csirac/session.bin', 'rb') as f:
    data = f.read()

# Chercher "DENIED" encodé
denied_pos = data.find(bytes([0x81, 0x44, 0x81, 0x45, 0x81, 0x4e, 0x81, 0x49, 0x81, 0x45, 0x81, 0x44]))
print("DENIED a la position:", denied_pos)

# Chercher "HELP" encodé
help_pos = data.find(bytes([0x81, 0x48, 0x81, 0x45, 0x81, 0x4c, 0x81, 0x50]))
print("HELP a la position:", help_pos)

# Chercher "RESET" encodé
reset_pos = data.find(bytes([0x81, 0x52, 0x81, 0x45, 0x81, 0x53, 0x81, 0x45, 0x81, 0x54]))
print("RESET a la position:", reset_pos)

# Chercher "RUN" encodé
run_pos = data.find(bytes([0x81, 0x52, 0x81, 0x55, 0x81, 0x4e]))
print("RUN a la position:", run_pos)

# Chercher "csaw"
csaw_pos = data.find(b'csaw')
print("csaw a la position:", csaw_pos)

# Chercher "csaw{"
csaw_brace_pos = data.find(b'csaw{')
print("csaw{ a la position:", csaw_brace_pos)

# Chercher "}" simple
close_pos = data.find(b'}')
print("} simple a la position:", close_pos)

# Chercher "}" encodé (0x81 0x7d)
close_enc_pos = data.find(bytes([0x81, 0x7d]))
print("} encodé a la position:", close_enc_pos)

# Chercher "}" encodé (0x81 0x7d) partout
for i in range(len(data)-1):
    if data[i] == 0x81 and data[i+1] == 0x7d:
        print("Trouve 0x81 0x7d a la position", i)