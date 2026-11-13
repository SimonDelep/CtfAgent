# Singleton ports
singleton_ports = [50913, 50517, 50915, 50894, 50969, 50581, 50957, 50698, 50142, 50207, 50046, 50573, 50272, 50129, 50784, 50716, 50856, 50695, 50947, 50275]

# If the flag starts with "csaw{", let's see what key would produce that
flag_start = "csaw{"
flag_bytes = [ord(c) for c in flag_start]

print("If plaintext starts with 'csaw{':")
for i, (sp, fb) in enumerate(zip(singleton_ports[:5], flag_bytes)):
    # What key byte would give us fb when XORed with sp % 256?
    key_byte = (sp % 256) ^ fb
    print(f"  sp={sp}, sp%256={sp%256}, expected fb={fb} ('{chr(fb)}'), key_byte would be {key_byte}")

# Also try with full port value (2 bytes)
print("\nTrying with full port values (2 bytes each):")
# If we treat each singleton port as a 2-byte value
for i, sp in enumerate(singleton_ports[:5]):
    print(f"  sp={sp} = {sp:04x}")