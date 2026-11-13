import py7zr
with py7zr.SevenZipFile('vcheck.7z', 'r') as archive:
    archive.extractall(path='vcheck_extracted')
print("Extraction terminée")