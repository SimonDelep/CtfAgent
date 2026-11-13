# Les ClientRandoms du PCAP (avec prefix de version)
cr_443_full = "03036aa4f15c976aa8e351b7fe1246ca34d77983e3a2340aafaa6b28502f04e0"
cr_4433_full = "03016aa4f15e9f5793cf966ea28bc7635164064d751c19a6eb36fa4695672798"

# Le vrai ClientRandom est après les 2 premiers bytes (version)
cr_443 = cr_443_full[4:]  # Skip "0303" (2 bytes = 4 hex chars)
cr_4433 = cr_4433_full[4:]  # Skip "0301"

print(f"ClientRandom pour port 443: {cr_443}")
print(f"ClientRandom pour port 4433: {cr_4433}")

# Les clés du sslkeylog.txt
key1_cr = "6aa4f15c976aa8e351b7fe1246ca34d77983e3a2340aafaa6b28502f04e0895a"
key2_cr = "6aa4f15e9f5793cf966ea28bc7635164064d751c19a6eb36fa4695672798d4fd"

print(f"\nKey1 CR: {key1_cr}")
print(f"Key2 CR: {key2_cr}")

# Corrélation
if cr_443 == key1_cr:
    print("\nPort 443 correspond à Key1")
    key_443_master = "7843e5988faf198cc4c2c10d20e6af50fd868e2f712d86f2cca808c67fab8d77f8b268eca9d3f6fb66786a78158ebd05"
elif cr_443 == key2_cr:
    print("\nPort 443 correspond à Key2")
    key_443_master = "4c47398320e2b2d40eac1b86168a7cb854d15e49d7c086a63307c25a01d2d1b75f1817f7f3a31dccab08dba5e106f31c"

if cr_4433 == key1_cr:
    print("Port 4433 correspond à Key1")
    key_4433_master = "7843e5988faf198cc4c2c10d20e6af50fd868e2f712d86f2cca808c67fab8d77f8b268eca9d3f6fb66786a78158ebd05"
elif cr_4433 == key2_cr:
    print("Port 4433 correspond à Key2")
    key_4433_master = "4c47398320e2b2d40eac1b86168a7cb854d15e49d7c086a63307c25a01d2d1b75f1817f7f3a31dccab08dba5e106f31c"

print(f"\nMaster secret pour port 4433: {key_4433_master}")