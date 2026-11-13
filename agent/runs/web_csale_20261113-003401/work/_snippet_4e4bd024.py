import os
# Lister les fichiers du challenge
for root, dirs, files in os.walk("/challenge"):
    for f in files:
        print(os.path.join(root, f))