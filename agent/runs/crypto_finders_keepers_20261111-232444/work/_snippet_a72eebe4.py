encoded = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
target_prefix = "csaw{"

# XOR avec chaque caractère possible
for key in range(256):
    result = ""
    for i, c in enumerate(encoded):
        result += chr(ord(c) ^ key)
    if result.startswith("csaw{"):
        print(f"Key {key} (0x{key:02x}): {result}")