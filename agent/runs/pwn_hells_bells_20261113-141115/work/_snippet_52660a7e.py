import subprocess
import os

# Essayer d'exécuter avec l'interpréteur système
env = os.environ.copy()
env['LD_LIBRARY_PATH'] = '.'

try:
    proc = subprocess.run(
        ['./thermite-charge'],
        input=b'1\n2\n3\n4\n',
        capture_output=True,
        timeout=5,
        env=env
    )
    print("stdout:", proc.stdout.decode('latin-1', errors='replace'))
    print("stderr:", proc.stderr.decode('latin-1', errors='replace'))
    print("returncode:", proc.returncode)
except Exception as e:
    print("Exception:", e)