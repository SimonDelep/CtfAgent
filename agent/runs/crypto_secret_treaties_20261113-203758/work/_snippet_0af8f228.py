# Testons l'outil mh_subsetsum_solver
# D'abord, vérifions s'il est callable
from tools import mh_subsetsum_solver

# Lire les données
pubkey = []
with open('pubkey.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            pubkey.append(int(line))

ciphertexts = []
with open('ciphertext.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            ciphertexts.append(int(line))

# Essayer de résoudre le premier bloc avec différentes méthodes
for method in ['lagarias', 'cvp', 'bkz']:
    print(f"\n=== Méthode: {method} ===")
    try:
        result = mh_subsetsum_solver(pubkey, ciphertexts[0], method)
        print(f"Résultat: {result}")
        if result:
            # Vérifier si c'est binaire
            if all(b in [0, 1] for b in result):
                print("Vecteur binaire trouvé!")
                # Convertir en bytes
                bits = result
                bytes_val = []
                for i in range(0, 72, 8):
                    byte_bits = bits[i:i+8]
                    byte_val = 0
                    for b in byte_bits:
                        byte_val = (byte_val << 1) | b
                    bytes_val.append(byte_val)
                print(f"Bytes: {bytes_val}")
                try:
                    print(f"ASCII: {bytes(bytes_val)}")
                except:
                    pass
    except Exception as e:
        print(f"Erreur: {e}")