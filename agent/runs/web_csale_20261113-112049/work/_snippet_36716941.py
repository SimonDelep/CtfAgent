with open("workdir/player/main.py", "r") as f:
    content = f.read()
print(f"Total lines: {len(content.splitlines())}")
print(f"Total chars: {len(content)}")
# Print the whole file in chunks
chunks = [content[i:i+2000] for i in range(0, len(content), 2000)]
for i, chunk in enumerate(chunks):
    print(f"=== CHUNK {i} ===")
    print(chunk)
    print()