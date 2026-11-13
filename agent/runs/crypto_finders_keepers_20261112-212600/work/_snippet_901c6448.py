import string

payload = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"

# Essayons un décalage de Caesar sur les lettres seulement, en gardant les autres caractères
def caesar(text, shift):
    result = ""
    for c in text:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            result += chr((ord(c) - base + shift) % 26 + base)
        else:
            result += c
    return result

# Essayons tous les shifts
for shift in range(26):
    decoded = caesar(payload, shift)
    # Vérifions si on obtient des mots anglais courants
    if 'the' in decoded.lower() or 'doc' in decoded.lower() or 'go' in decoded.lower():
        print(f"Shift {shift}: {decoded}")