import struct

with open('nitro', 'rb') as f:
    data = f.read()

# Entrée à 0x10f0
entry_offset = 0x10f0
code = data[entry_offset:entry_offset+300]

# Désassemblage manuel approximatif
# f3 0f 1e fa = rep pause
# 31 ed = xor ebp, ebp
# 49 89 d1 = mov r9, rdx
# 5e = pop rsi
# 48 89 e2 = mov rdx, rsp
# 48 83 e4 f0 = and rsp, -16
# 50 = push rax
# 54 = push rsp
# 45 31 c0 = xor r8d, r8d
# 31 c9 = xor ecx, ecx
# 48 c7 c7 d6 11 40 00 = mov rdi, 0x4011d6 (adresse de main ?)
# ff 15 c3 2e 00 00 = call [rip+0x2ec3]
# f4 = hlt
# ...

# L'adresse 0x4011d6 est probablement main
# Regardons ce qui se trouve à 0x4011d6 (offset = 0x11d6)
main_offset = 0x11d6
print(f"Contenu à 0x11d6 (main ?):")
print(data[main_offset:main_offset+100].hex())

# Regardons aussi ce qui est appelé avant main
# L'instruction call est à l'offset relatif
# ff 15 c3 2e 00 00 = call [rip+0x2ec3]
# Après l'instruction call (6 bytes), rip = current + 6
# Donc l'adresse cible = (current_pos + 6) + 0x2ec3

# Trouvons la position de l'instruction call
call_pos = code.find(bytes.fromhex('ff15c32e0000'))
if call_pos != -1:
    print(f"\nCall trouvé à offset relatif {call_pos} dans le code d'entrée")
    # Adresse de l'instruction call = 0x4010f0 + call_pos
    call_addr = 0x4010f0 + call_pos
    # Après l'instruction (6 bytes), rip = call_addr + 6
    # Cible = rip + 0x2ec3 = call_addr + 6 + 0x2ec3
    target = call_addr + 6 + 0x2ec3
    print(f"Adresse de l'instruction call: {hex(call_addr)}")
    print(f"Adresse cible (fonction appelée): {hex(target)}")