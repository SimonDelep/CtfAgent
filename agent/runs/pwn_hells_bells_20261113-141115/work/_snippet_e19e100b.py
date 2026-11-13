from pwn import *
import subprocess

# Test le binaire localement
p = process(['./thermite-charge'], env={'LD_LIBRARY_PATH': '.'})
p.sendlineafter(b'===', b'1')  # plant charge
p.sendlineafter(b'slot', b'0')
p.sendlineafter(b'size', b'10')
p.recvuntil(b'slot 0')
print(p.recvall().decode())