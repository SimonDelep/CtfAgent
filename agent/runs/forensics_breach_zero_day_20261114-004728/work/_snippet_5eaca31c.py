import re

with open('fenwick_memdump.txt', 'r', errors='ignore') as f:
    content = f.read()

# Trouver le contexte autour de la chaîne C2
idx = content.find('r/o2e5adE76q=MuQJ_+C2LNY')
if idx != -1:
    print("Contexte autour de la chaîne C2:")
    print(content[max(0, idx-50):idx+100])
    print()

# Chercher aussi d'autres occurrences de C2
c2_occurrences = re.findall(r'.{0,30}C2.{0,30}', content)
print("Occurrences de C2:")
for o in c2_occurrences[:10]:
    print(repr(o))