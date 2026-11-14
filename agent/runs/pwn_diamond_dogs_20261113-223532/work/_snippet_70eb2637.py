from pwn import *

# Charger le binaire
elf = ELF('./guard-dog')

# Afficher les fonctions principales
print("=== Fonctions principales ===")
for sym in elf.symbols:
    if not sym.startswith('_') and sym in ['main', 'adopt', 'retire', 'command', 'note', 'read_note', 'shred_note']:
        print(f"{sym}: {hex(elf.symbols[sym])}")

# Afficher les sections
print("\n=== Sections ===")
for sec in elf.sections:
    if sec.name in ['.text', '.data', '.bss', '.got']:
        print(f"{sec.name}: {hex(sec.address)} - {sec.size}")

# Afficher les symboles
print("\n=== Symboles libc ===")
for sym in ['malloc', 'free', 'puts', 'read', 'write']:
    if sym in elf.symbols:
        print(f"{sym}: {hex(elf.symbols[sym])}")