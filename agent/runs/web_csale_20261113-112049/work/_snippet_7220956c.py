with open("workdir/player/main.py", "r") as f:
    content = f.read()

# Chercher les routes liées aux drafts
import re
draft_routes = re.findall(r'@app\.route\([^)]+\)[^@]*?(?=@app\.route|$)', content, re.DOTALL)
for route in draft_routes:
    if 'draft' in route.lower() or 'slug' in route.lower():
        print(route[:500])
        print("---")