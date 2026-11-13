import sys
sys.path.insert(0, './py7zr_lib')
import py7zr

with py7zr.SevenZipFile('vcheck.7z', 'r') as archive:
    archive.extractall(path='./extracted')
print("Extraction terminée")