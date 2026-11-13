# Analyser les payloads du WAL
payloads = [
    "03004cadeffa50697f806ca9bd3f57a8a523985dea73f49dff0733e807e0fdcae30185",
    "0400091f7265636f7264696e67",
    "03004ce00f2b31643cd153842814cfb2d0a44dabc94741d4b07c9c19c52c3024e077d7",
    "03000103",
    "03004c02fb3ab31e03b77ffc09cdb6cee5cd449352cca9458409e8efecd0181882bb86",
    "03004cc45487d4d6cea0ff3839470bc2e6266b33ea2f9cc19a0fe4a20d3ead857a61dd",
    "03004c26a09656acf1c6d340189e72bed34f620b71a47450ae7a905424c285b918ad8c",
    "03004cd3de5a6c5e62ceddd3e5de81caa1c3017fba2f6788329d5f902ddda0342042bb",
    "0400081b7374616e646279",
    "03004c3065019dea0f757f675d4d71206ce4a131070a27c87b198ec1bad26652c7bad6",
]

for p in payloads:
    data = bytes.fromhex(p)
    print(f"Payload: {p[:20]}...")
    print(f"  Longueur: {len(data)} octets")
    print(f"  Premier octet: 0x{data[0]:02x}")
    if len(data) >= 3:
        print(f"  Deuxième et troisième octets: 0x{data[1]:02x} 0x{data[2]:02x}")
        # Essayer de lire 0x004c comme taille
        if len(data) >= 3:
            size = (data[1] << 8) | data[2]
            print(f"  Taille potentielle (big-endian): {size}")
    print()

# Vérifier les shares actuels
north_share = bytes.fromhex("c144a2e5314a2753401a0a4413b08a8b51fbea0fa18cddc829f7cf24e0a8cf8a")
south_share = bytes.fromhex("5e90b9133b231b6d9ac4f60ea10d70d6f76caf83c2e71216f2f3625112be9fd2")

print(f"North share (32 octets): {north_share.hex()}")
print(f"South share (32 octets): {south_share.hex()}")
print(f"Token = XOR: {bytes(a^b for a,b in zip(north_share, south_share)).hex()}")
