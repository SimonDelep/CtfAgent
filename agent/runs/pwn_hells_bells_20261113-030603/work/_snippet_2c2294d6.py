import subprocess

# Disassemble main function (0x1318, 896 bytes)
result = subprocess.run(['objdump', '-D', '-M', 'intel', '-b', 'binary', '-m', 'i386:x86-64', 
                         '--start-address=0x1318', '--stop-address=0x1698', 'thermite-charge'], 
                        capture_output=True, text=True, timeout=10)
print(result.stdout)