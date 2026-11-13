SCHEMA = {
  "name": "disasm_masterkey",
  "description": "Désassemble le binaire masterkey x86-64 en utilisant capstone pour analyser la logique de vérification",
  "parameters": {
    "properties": {
      "binary_path": {
        "description": "Chemin du binaire masterkey",
        "type": "string"
      },
      "num_instructions": {
        "description": "Nombre d'instructions à désassembler (optionnel)",
        "type": "integer"
      },
      "start_addr": {
        "description": "Adresse de départ pour le désassemblage (optionnel)",
        "type": "integer"
      }
    },
    "required": [
      "binary_path"
    ],
    "type": "object"
  }
}

import capstone
import struct

def main(args):
    binary_path = args.get("binary_path", "masterkey")
    start_addr = args.get("start_addr", None)
    num_instructions = args.get("num_instructions", 200)
    
    # Lire le binaire
    with open(binary_path, "rb") as f:
        data = f.read()
    
    # Parser l'ELF pour trouver les sections
    # Magic ELF: 0x7f 'E' 'L' 'F'
    if data[:4] != b'\x7fELF':
        return f"Erreur: fichier ELF attendu, trouvé {data[:4]}"
    
    # Architecture x86-64
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    
    # Trouver la section .text
    # En-tête ELF 64-bit
    e_shoff = struct.unpack('<Q', data[0x28:0x30])[0]  # Section header offset
    e_shentsize = struct.unpack('<H', data[0x3a:0x3c])[0]
    e_shnum = struct.unpack('<H', data[0x3c:0x3e])[0]
    e_shstrndx = struct.unpack('<H', data[0x3e:0x40])[0]
    
    # Trouver la section .text
    text_offset = 0
    text_size = 0
    text_vaddr = 0
    
    for i in range(e_shnum):
        sh_offset = e_shoff + i * e_shentsize
        sh_type = struct.unpack('<I', data[sh_offset+4:sh_offset+8])[0]
        sh_offset_sec = struct.unpack('<Q', data[sh_offset+24:sh_offset+32])[0]
        sh_size = struct.unpack('<Q', data[sh_offset+32:sh_offset+40])[0]
        sh_addr = struct.unpack('<Q', data[sh_offset+16:sh_offset+24])[0]
        sh_name_idx = struct.unpack('<I', data[sh_offset:sh_offset+4])[0]
        
        # Lire le nom de la section depuis .shstrtab
        # D'abord trouver .shstrtab
        if i == e_shstrndx:
            shstrtab_offset = sh_offset_sec
            shstrtab_size = sh_size
            continue
    
    # Trouver .shstrtab d'abord
    shstrtab_offset = 0
    shstrtab_size = 0
    for i in range(e_shnum):
        sh_offset = e_shoff + i * e_shentsize
        sh_type = struct.unpack('<I', data[sh_offset+4:sh_offset+8])[0]
        sh_offset_sec = struct.unpack('<Q', data[sh_offset+24:sh_offset+32])[0]
        sh_size = struct.unpack('<Q', data[sh_offset+32:sh_offset+40])[0]
        if sh_type == 3:  # SHT_STRTAB
            # Vérifier si c'est .shstrtab
            pass
    
    # Approche simplifiée: trouver .text par recherche
    # L'entrée du programme est à e_entry
    e_entry = struct.unpack('<Q', data[0x18:0x20])[0]
    
    # Trouver la section contenant l'entrée
    for i in range(e_shnum):
        sh_offset = e_shoff + i * e_shentsize
        sh_type = struct.unpack('<I', data[sh_offset+4:sh_offset+8])[0]
        sh_offset_sec = struct.unpack('<Q', data[sh_offset+24:sh_offset+32])[0]
        sh_size = struct.unpack('<Q', data[sh_offset+32:sh_offset+40])[0]
        sh_addr = struct.unpack('<Q', data[sh_offset+16:sh_offset+24])[0]
        sh_flags = struct.unpack('<Q', data[sh_offset+32+8:sh_offset+32+16])[0]
        
        # SHT_PROGBITS avec execute flag
        if sh_type == 1 and (sh_flags & 4):  # SHF_EXECINSTR = 4
            if sh_addr <= e_entry < sh_addr + sh_size:
                text_offset = sh_offset_sec
                text_size = sh_size
                text_vaddr = sh_addr
                break
    
    if text_offset == 0:
        return f"Section .text non trouvée, e_entry={hex(e_entry)}"
    
    # Extraire le code .text
    text_data = data[text_offset:text_offset+text_size]
    
    # Désassembler
    result = []
    count = 0
    for insn in md.disasm(text_data, text_vaddr):
        result.append(f"{hex(insn.address)}: {insn.mnemonic} {insn.op_str}")
        count += 1
        if count >= num_instructions:
            break
    
    return "\n".join(result[:100])

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
