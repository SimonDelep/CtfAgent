# Générer les candidats de flag
pdq_key = "PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j"
service = "Windows Update"
backdoor = "WindowsUpdate.exe"

# Nettoyer les espaces et caractères spéciaux pour le format du flag
# Le format est csaw{{INDICATOR_SERVICE_BACKDOOR}}

# Candidats possibles:
candidates = []

# 1. Avec PDQ= complet, espaces remplacés par underscores
candidates.append(f"csaw{{{pdq_key}_{service.replace(' ', '_')}_{backdoor}}}")

# 2. Sans le préfixe PDQ=
pdq_value = "SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j"
candidates.append(f"csaw{{{pdq_value}_{service.replace(' ', '_')}_{backdoor}}}")

# 3. Avec = remplacé par _ dans la clé
pdq_clean = pdq_key.replace('=', '_')
candidates.append(f"csaw{{{pdq_clean}_{service.replace(' ', '_')}_{backdoor}}}")

# 4. Avec + remplacé par _ aussi
pdq_clean2 = pdq_key.replace('=', '_').replace('+', '_')
candidates.append(f"csaw{{{pdq_clean2}_{service.replace(' ', '_')}_{backdoor}}}")

# 5. Juste la valeur PDQ sans le préfixe, avec = remplacé
candidates.append(f"csaw{{{pdq_value.replace('=', '_').replace('+', '_')}_{service.replace(' ', '_')}_{backdoor}}}")

# 6. Avec la chaîne contenant C2
c2_string = "r/o2e5adE76q=MuQJ_C2LNY"  # version nettoyée
candidates.append(f"csaw{{{c2_string}_{service.replace(' ', '_')}_{backdoor}}}")

for i, c in enumerate(candidates):
    print(f"Candidat {i+1}: {c}")