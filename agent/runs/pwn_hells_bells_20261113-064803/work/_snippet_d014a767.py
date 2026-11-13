import subprocess
result = subprocess.run(['objdump', '-d', '--no-show-raw-insn', '--demangle', 'thermite-charge'], capture_output=True, text=True, timeout=15)
print(result.stdout[:5000])