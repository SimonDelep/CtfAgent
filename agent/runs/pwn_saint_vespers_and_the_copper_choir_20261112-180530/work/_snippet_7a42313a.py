# Taille de la structure chorister_t
# name[0x38] = 56 bytes
# sing = 8 bytes (pointeur 64-bit)
# transcript = 8 bytes (pointeur)
# transcript_len = 8 bytes (size_t)
# active = 4 bytes (int)
# padding pour alignement

import struct

# Structure:
# offset 0: name[56]
# offset 56: sing (8 bytes)
# offset 64: transcript (8 bytes)
# offset 72: transcript_len (8 bytes)
# offset 80: active (4 bytes)
# offset 84: padding (4 bytes)
# Total: 88 bytes

print(f"Taille estimée de chorister_t: 88 bytes")

# Vérifions avec ctypes
import ctypes

class Chorister(ctypes.Structure):
    _fields_ = [
        ("name", ctypes.c_char * 0x38),
        ("sing", ctypes.c_void_p),
        ("transcript", ctypes.c_void_p),
        ("transcript_len", ctypes.c_size_t),
        ("active", ctypes.c_int),
    ]

print(f"Taille réelle avec ctypes: {ctypes.sizeof(Chorister)} bytes")