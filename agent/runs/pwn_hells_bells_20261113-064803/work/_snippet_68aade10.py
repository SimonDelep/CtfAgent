import subprocess

# Utiliser pycapstone ou simplement lire les octets du binaire
# Essayons d'abord de voir si capstone est disponible
try:
    from capstone import *
    print("Capstone disponible")
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    
    # Lire le binaire
    with open('thermite-charge', 'rb') as f:
        data = f.read()
    
    # Trouver l'offset du code (section .text commence à 0x1180, offset de fichier 0x1180 pour PIE)
    # Pour un PIE, l'adresse virtuelle = adresse de chargement + offset
    # L'adresse de base est 0x1000 (à partir de readelf -S)
    
    # Section .text: adresse 0x1180, offset de fichier 0x1180 (car c'est un PIE avec base 0x1000)
    # En fait, pour un PIE, l'offset de fichier = adresse virtuelle - base + offset_base
    # Regardons readelf -l pour les segments
    
    result = subprocess.run(['readelf', '-l', 'thermite-charge'], capture_output=True, text=True)
    print(result.stdout)
except ImportError:
    print("Capstone non disponible")