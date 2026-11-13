with open("main.py", "r") as f:
    content = f.read()
print(f"Total length: {len(content)}")
# Print en chunks de 1000 caractères
for i in range(0, len(content), 1000):
    print(f"=== CHUNK {i} ===")
    print(content[i:i+1000])
    print()