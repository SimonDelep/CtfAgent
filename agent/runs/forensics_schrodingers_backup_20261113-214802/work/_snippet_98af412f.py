north_hex = "C144A2E5314A2753401A0A4413B08A8B51FBEA0F618CDDC829F7CF24E0A8CF8A"
south_hex = "5E90B9133B231B6D9AC4F60EA10D70D6F76CAF83C2E71216F2F3625112BE9FD2"
print(f"North length: {len(north_hex)} hex chars = {len(north_hex)//2} bytes")
print(f"South length: {len(south_hex)} hex chars = {len(south_hex)//2} bytes")

# Calculate XOR token
north = bytes.fromhex(north_hex)
south = bytes.fromhex(south_hex)
token = bytes(a ^ b for a, b in zip(north, south))
print(f"Token: {token.hex()}")