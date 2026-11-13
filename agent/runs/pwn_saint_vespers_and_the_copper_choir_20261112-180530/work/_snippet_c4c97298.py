import shutil
import os

src_dir = "/home/etudiantelambda/Documents/CSAW_LLM_2026-BTN-DLP/CtfAgent/CSAW-Quals/pwn/saint_vespers_and_the_copper_choir/dist"
files = ["vespers", "libc.so.6", "ld-2.35.so"]

for f in files:
    src = os.path.join(src_dir, f)
    dst = f
    shutil.copy2(src, dst)
    print(f"Copié {f}")

print("Fichiers copiés:")
for f in os.listdir("."):
    print(f"  {f}")