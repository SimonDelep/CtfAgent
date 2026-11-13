from capstone import *
import sys

# Lire le binaire
with open('thermite-charge', 'rb') as f:
    code = f.read()

# Désassembler avec x86-64
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

# Trouver les fonctions principales - on cherche les chaînes de caractères d'abord
# Les chaînes sont généralement dans la section .rodata
# On va faire un désassemblage complet et chercher les appels intéressants

# D''abord, trouvons l'adresse de base
import struct

# ELF header
e_type = struct.unpack('<H', code[16:18])[0]
e_entry = struct.unpack('<Q', code[24:32])[0]
e_phoff = struct.unpack('<Q', code[32:40])[0]

print(f"ELF type: {e_type}, entry: {hex(e_entry)}, phoff: {e_phoff}")

# Trouvons les sections
# Section header offset
e_shoff = struct.unpack('<Q', code[64:72])[0]
e_shentsize = struct.unpack('<H', code[58:60])[0]
e_shnum = struct.unpack('<H', code[60:62])[0]
e_shstrndx = struct.unpack('<H', code[62:64])[0]

print(f"shoff: {hex(e_shoff)}, shentsize: {e_shentsize}, shnum: {e_shnum}, shstrndx: {e_shstrndx}")

# Trouvons la section .rodata pour les chaînes
for i in range(e_shnum):
    sh_offset = e_shoff + i * e_shentsize
    sh = code[sh_offset:sh_offset + e_shentsize]
    sh_name_idx = struct.unpack('<I', sh[0:4])[0]
    sh_type = struct.unpack('<I', sh[4:8])[0]
    sh_addr = struct.unpack('<Q', sh[16:24])[0]
    sh_offset_sec = struct.unpack('<Q', sh[24:32])[0]
    sh_size = struct.unpack('<Q', sh[32:40])[0]
    
    if sh_type == 1:  # SHT_PROGBITS
        # C'est une section de données
        pass
    elif sh_type == 8:  # SHT_NOBITS (BSS)
        pass

# Cherchons les chaînes directement dans le binaire
strings = []
current = b''
for i, b in enumerate(code):
    if 32 <= b < 127:
        current += bytes([b])
    else:
        if len(current) >= 4:
            strings.append((i - len(current), current.decode()))
        current = b''
if len(current) >= 4:
    strings.append((len(code) - len(current), current.decode()))

# Affichons les chaînes intéressantes
interesting = ['plant', 'defuse', 'rewire', 'inspect', 'charge', 'menu', 'printf', 'free', 'malloc', 'system', '/bin/sh']
for offset, s in strings:
    if any(i in s.lower() for i in interesting) or len(s) > 10:
        print(f"{hex(offset)}: {s}")