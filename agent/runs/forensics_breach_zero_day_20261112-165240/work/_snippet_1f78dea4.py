import base64

# Extraire les IDs base64 visibles
ids = ["QkFDS1VQU1ZD", "UkVMQVF", "lTSEVMTA=="]

for id_str in ids:
    try:
        decoded = base64.b64decode(id_str).decode('utf-8', errors='replace')
        print(f"{id_str} -> {decoded}")
    except Exception as e:
        print(f"{id_str} -> Erreur: {e}")

# Essayons de trouver plus d'IDs dans le fichier