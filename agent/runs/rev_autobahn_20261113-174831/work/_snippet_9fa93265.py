# Trouver smc_key.0 et extraire la clé
with open('nitro', 'rb') as f:
    data = f.read()

# Chercher smc_key.0
idx = data.find(b'smc_key.0')
print(f"smc_key.0 trouvé à offset {idx} (0x{idx:x})")

# Le nom de la variable est suivi de la valeur
# Regardons ce qui suit
context = data[idx:idx+50]
print(f"Contexte: {context}")

# Chercher la valeur de la clé - probablement juste après le nom
# Dans les ELF, les variables globales sont dans .rodata ou .data
# smc_key.0 est une variable, sa valeur est ailleurs

# Regardons autour de l'offset 0x20a0 où on a vu des motifs intéressants
print("\n=== Analyse autour de 0x20a0 ===")
offset_20a0 = 0x20a0
print(f"À 0x20a0: {data[offset_20a0:offset_20a0+32].hex()}")

# Chercher la clé XOR - peut-être que smc_key.0 pointe vers une zone de données
# Regardons les symboles
import subprocess
result = subprocess.run(['readelf', '-s', 'nitro'], capture_output=True, text=True)
print("\n=== Symboles ===")
for line in result.stdout.split('\n'):
    if 'smc' in line.lower() or 'key' in line.lower() or 'enc' in line.lower():
        print(line)