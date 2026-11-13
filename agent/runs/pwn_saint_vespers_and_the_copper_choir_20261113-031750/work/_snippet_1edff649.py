from pwn import *

# Test local
context.binary = ELF('./vespers')
context.terminal = ['tmux', 'splitw', '-h']

# Lancer localement
p = process('./vespers', env={'LD_LIBRARY_PATH': '.'})

def recv_line():
    return p.recvline().decode().strip()

def send_line(s):
    p.sendlineafter(b'> ', s)

# Menu
print(recv_line())  # "The copper coils hum..."

# Option 1: Recruit
send_line(b'1')
print(recv_line())  # "Name this chorister: "
p.sendlineafter(b': ', b'TestChorister')
print(recv_line())  # "Choose a hymn style..."
send_line(b'0')
print(recv_line())  # "Transcript length..."
send_line(b'10')
print(recv_line())  # "Recite the transcript..."
p.sendlineafter(b': ', b'1234567890')
print(recv_line())  # "Chorister seated at position 0."

# Option 7: Roster
send_line(b'7')
print(recv_line())
print(recv_line())

# Option 2: Retire
send_line(b'2')
print(recv_line())  # "Retire which seat? "
send_line(b'0')
print(recv_line())  # "Seat 0 retired to the archive."

# Option 7: Roster
send_line(b'7')
print(recv_line())
print(recv_line())

# Option 3: Restore
send_line(b'3')
print(recv_line())  # "Restore which seat? "
send_line(b'0')
print(recv_line())  # "Seat 0 restored to the loft."

# Option 7: Roster
send_line(b'7')
print(recv_line())
print(recv_line())

p.close()