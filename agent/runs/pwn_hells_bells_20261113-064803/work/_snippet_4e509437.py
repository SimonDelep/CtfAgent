import subprocess
import sys

# Utiliser radare2 ou r2pipe si disponible, sinon essayer avec readelf et objdump
result = subprocess.run(['r2', '-c', 'pd 200 @ main', '-qq', 'thermite-charge'], capture_output=True, text=True, timeout=10)
print("radare2 output:")
print(result.stdout[:3000] if result.stdout else "None")
print("stderr:", result.stderr[:500] if result.stderr else "None")