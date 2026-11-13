# Break sur mprotect
break mprotect
# Lancer avec un mot de passe dummy
run testpass
# Après mprotect, dump la mémoire de la section .enccode
# Adresse de départ: 0x40130d, taille: 0x15e
dump binary memory enccode_decrypted.bin 0x40130d 0x40146b
quit
