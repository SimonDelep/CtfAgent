with open('capture.pcap', 'rb') as f:
    data = f.read()

# Each block is 62 bytes, starting from position 82
blocks = []
for i in range(504):
    pos = 82 + i * 62
    block = data[pos:pos+62]
    blocks.append(block)

first_block = blocks[0]
print(f"First block length: {len(first_block)}")

# Compare each block to the first one
variations = []
for i, block in enumerate(blocks):
    if len(block) != len(first_block):
        continue
    diff_positions = [j for j in range(len(block)) if block[j] != first_block[j]]
    if diff_positions:
        variations.append((i, diff_positions, [block[j] for j in diff_positions]))

print(f"Number of varying blocks: {len(variations)}")

# Show first 20 variations
print("\nFirst 20 variations:")
for i, (block_idx, diff_pos, diff_vals) in enumerate(variations[:20]):
    print(f"  Block {block_idx}: diff at positions {diff_pos}, values {diff_vals}")

# Check if there's a pattern in the variations
# Maybe only certain positions vary
all_diff_positions = set()
for _, diff_pos, _ in variations:
    all_diff_positions.update(diff_pos)

print(f"\nAll positions that vary: {sorted(all_diff_positions)}")