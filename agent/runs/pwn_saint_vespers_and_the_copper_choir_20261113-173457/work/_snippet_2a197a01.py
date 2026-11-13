import subprocess
import sys

# Lancer le binaire avec le loader correct
proc = subprocess.Popen(
    ['./ld-2.35.so', './vespers'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    cwd='.'
)

# Envoyer les commandes
commands = b"1\nTestChorister\n0\n100\n" + b"A" * 100 + b"\n7\n9\n"
stdout, stderr = proc.communicate(input=commands, timeout=5)

print("STDOUT:")
print(stdout.decode('latin-1', errors='replace'))
print("STDERR:")
print(stderr.decode('latin-1', errors='replace'))
print("RETURNCODE:", proc.returncode)