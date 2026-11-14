SCHEMA = {
  "name": "disasm_section",
  "description": "Désassemble une section du binaire masterkey en utilisant Capstone. Prend l'adresse virtuelle de départ et la longueur à désassembler.",
  "parameters": {
    "properties": {
      "length": {
        "description": "Nombre d'octets à désassembler",
        "type": "integer"
      },
      "vaddr": {
        "description": "Adresse virtuelle de départ",
        "type": "integer"
      }
    },
    "required": [
      "vaddr",
      "length"
    ],
    "type": "object"
  }
}

import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

def main(args):
    vaddr = args['vaddr']
    length = args['length']
    
    # Lire le binaire
    with open('masterkey', 'rb') as f:
        data = f.read()
    
    # Parser l'entête ELF pour trouver l'offset
    e_phoff = struct.unpack('<Q', data[32:40])[0]
    e_phnum = struct.unpack('<H', data[56:58])[0]
    e_phentsize = struct.unpack('<H', data[54:56])[0]
    
    # Trouver le segment contenant l'adresse virtuelle
    def vaddr_to_offset(vaddr):
        for i in range(e_phnum):
            ph_offset = e_phoff + i * e_phentsize
            p_type = struct.unpack('<I', data[ph_offset:ph_offset+4])[0]
            p_offset = struct.unpack('<Q', data[ph_offset+8:ph_offset+16])[0]
            p_vaddr = struct.unpack('<Q', data[ph_offset+16:ph_offset+24])[0]
            p_filesz = struct.unpack('<Q', data[ph_offset+32:ph_offset+40])[0]
            p_memsz = struct.unpack('<Q', data[ph_offset+40:ph_offset+48])[0]
            if p_type == 1 and p_vaddr <= vaddr < p_vaddr + p_memsz:
                offset_in_seg = vaddr - p_vaddr
                return p_offset + offset_in_seg
        return None
    
    file_offset = vaddr_to_offset(vaddr)
    if file_offset is None:
        print(f"Adresse 0x{vaddr:x} non trouvée dans les segments")
    else:
        code = data[file_offset:file_offset+length]
        
        # Désassembler avec Capstone
        md = Cs(CS_ARCH_X86, CS_MODE_64)
        md.detail = True
        
        print(f"Désassemblage à partir de 0x{vaddr:x} (offset fichier 0x{file_offset:x}):")
        for insn in md.disasm(code, vaddr):
            print(f"  0x{insn.address:x}: {insn.mnemonic} {insn.op_str}")

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
