import inspect
# Essayons de voir si on peut trouver le code de l'outil polly_solver
# D'abord, regardons s'il y a un fichier de définition des outils
import os
for root, dirs, files in os.walk('/home/etudiantelambda/.local'):
    for f in files:
        if 'polly' in f.lower():
            print(os.path.join(root, f))