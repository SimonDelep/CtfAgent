# Essayons d'appeler l'outil subset_sum_solver
# Les outils forgés sont probablement disponibles via un module ou un mécanisme spécial

# D'abord, vérifions si on peut importer quelque chose
import sys
print("Modules disponibles:")
for m in sorted(sys.modules.keys()):
    if not m.startswith('_'):
        print(f"  {m}")