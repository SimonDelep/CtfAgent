from pwn import *
import sys

# Charger le binaire
elf = ELF('files/thermite-charge')

# Désassembler main
print("=== DÉCOMPILATION DE MAIN ===")
main_addr = elf.symbols['main']
print(f"main @ 0x{main_addr:x}")

# Désassembler les 100 premières instructions de main
disasm_code = disasm(elf.read(main_addr, 500))
print(disasm_code)