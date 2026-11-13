import os
for f in os.listdir("workdir/player/templates"):
    with open(f"workdir/player/templates/{f}", "r") as file:
        print(f"=== {f} ===")
        print(file.read())
        print()