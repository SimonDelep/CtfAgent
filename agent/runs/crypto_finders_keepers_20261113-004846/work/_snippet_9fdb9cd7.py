# Analyser le payload comme substitution/leetspeak
payload = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"

# Essayer de décoder leetspeak simple
leetspeak_map = {
    '0': 'o', '1': 'i', '2': 'z', '3': 'e', '4': 'a', '5': 's', 
    '6': 'g', '7': 't', '8': 'b', '9': 'q', '@': 'a', '3': 'e'
}

decoded = ""
for c in payload:
    decoded += leetspeak_map.get(c, c)
print("Leetspeak simple:", decoded)

# Peut-être que c'est une substitution ROT ou autre
import string
for rot in [1, 5, 13, 21]:
    result = ""
    for c in payload:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            result += chr((ord(c) - base + rot) % 26 + base)
        else:
            result += c
    print(f"ROT{rot}: {result}")