import py7zr
import os

os.makedirs("vcheck_extracted", exist_ok=True)
with py7zr.SevenZipFile("vcheck.7z", 'r') as archive:
    archive.extractall("vcheck_extracted")
print("Extraction terminée")