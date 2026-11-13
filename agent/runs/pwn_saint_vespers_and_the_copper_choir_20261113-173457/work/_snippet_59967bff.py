import subprocess
import os

# Essayer avec execvp ou en passant le loader comme premier argument
env = os.environ.copy()
env['LD_LIBRARY_PATH'] = '.'

# Lancer le loader avec le binaire comme argument
proc = subprocess.Popen(
    ['ld-2.35.so', './vespers'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env=env,
    cwd='.'
)

stdout, stderr = proc.communicate(input=b'9\n')
print("STDOUT:", stdout.decode('latin-1', errors='replace'))
print("STDERR:", stderr.decode('latin-1', errors='replace'))
print("RETURNCODE:", proc.returncode)