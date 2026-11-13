with open('capture.pcap', 'rb') as f:
    data = f.read()

# Each block is 62 bytes, starting from position 82 (after header)
# Let's analyze the structure

# First, let's see what's before the first PING
print("Header (first 82 bytes):")
print(data[:82].hex())
print()

# Now let's look at the structure of each block
# Block starts at position 82, each block is 62 bytes
# PING is at position 82, 144, 206, etc.

# Let's look at what's around PING in each block
for i in range(5):
    pos = 82 + i * 62
    block = data[pos:pos+62]
    print(f"Block {i}:")
    print(f"  Hex: {block.hex()}")
    print(f"  ASCII: {block}")
    print()

# Check if there are variations between blocks
blocks = []
for i in range(504):
    pos = 82 + i * 62
    block = data[pos:pos+62]
    blocks.append(block)

# Find unique blocks
unique_blocks = set(blocks)
print(f"Unique blocks: {len(unique_blocks)}")

# If there are variations, let's find them
if len(unique_blocks) > 1:
    print("\nFinding variations...")
    # Compare each block to the first one
    first_block = blocks[0]
    variations = []
    for i, block in enumerate(blocks):
        if block != first_block:
            # Find which bytes differ
            diff_positions = [j for j in range(62) if block[j] != first_block[j]]
            variations.append((i, diff_positions, [block[j] for j in diff_positions]))
    
    print(f"Number of varying blocks: {len(variations)}")
    if variations:
        print(f"\nFirst 10 variations:")
        for i, (block_idx, diff_pos, diff_vals) in enumerate(variations[:10]):
            print(f"  Block {block_idx}: diff at positions {diff_pos}, values {diff_vals}")