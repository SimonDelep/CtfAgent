#!/usr/bin/env python3
import re

with open("vcheck.log", "r") as f:
    content = f.read()

print("Contenu du log:")
print(repr(content))

# Parser les lignes
lines = content.strip().split("\n")
for line in lines:
    print(f"Ligne: {line}")
    parts = line.split()
    if len(parts) >= 3:
        label = parts[0]
        client_random = parts[1]
        master_secret = parts[2]
        print(f"  Label: {label}")
        print(f"  CR: {client_random} (len={len(client_random)})")
        print(f"  MS: {master_secret} (len={len(master_secret)})")
        print()
