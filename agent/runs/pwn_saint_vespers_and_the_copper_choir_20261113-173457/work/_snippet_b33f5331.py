import subprocess
import os

# Essayer d'exécuter avec le loader explicite
env = os.environ.copy()
env['LD_LIBRARY_PATH'] = '.'

proc = subprocess.Popen(
    ['./ld-2.35.so', './vespers'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env=env
)

stdout, stderr = proc.communicate(input=b'9\n')
print("STDOUT:", stdout.decode('latin-1', errors='replace'))
print("STDERR:", stderr.decode('latin-1', errors='replace'))
print("RETURNCODE:", proc.returncode)