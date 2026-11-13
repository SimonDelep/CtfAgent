# Vérifions comment polly_solver est implémenté en regardant son code source
import inspect
import sys

# On va essayer d'importer et inspecter l'outil
try:
    # L'outil est probablement dans le module des outils
    from tools import polly_solver
    print("polly_solver trouvé")
    print(inspect.signature(polly_solver))
except Exception as e:
    print(f"Erreur: {e}")