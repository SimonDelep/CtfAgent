from parse_wal_shares import parse_wal_shares

shares = parse_wal_shares("catalog.db-wal")
print(f"Nombre de shares extraits: {len(shares)}")
for i, share in enumerate(shares[:10]):
    print(f"Share {i}: {share.hex()}")