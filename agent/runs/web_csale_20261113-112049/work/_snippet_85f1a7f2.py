with open("workdir/player/main.py", "r") as f:
    content = f.read()

# Find all routes
import re
routes = re.findall(r'@app\.route\("([^"]+)"', content)
print("Routes trouvées:")
for r in routes:
    print(f"  {r}")