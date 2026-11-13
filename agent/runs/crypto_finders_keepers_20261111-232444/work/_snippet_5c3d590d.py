encoded = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"

# Essayons un décalage Caesar
for shift in range(26):
    result = ""
    for c in encoded:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            result += chr((ord(c) - base - shift) % 26 + base)
        else:
            result += c
    if "csaw" in result.lower():
        print(f"Shift {shift}: {result}")