from PIL import Image
# Essayons d'ouvrir le fichier MP4 comme une image (ça pourrait révéler quelque chose)
try:
    img = Image.open('finderskeepers.mp4')
    print("Format:", img.format)
    print("Mode:", img.mode)
    print("Size:", img.size)
    print("Info:", img.info)
    # Essayons de lire toutes les frames
    frame_count = 0
    while True:
        try:
            img.seek(frame_count)
            print(f"Frame {frame_count}: size={img.size}, mode={img.mode}")
            frame_count += 1
        except EOFError:
            break
except Exception as e:
    print("Erreur:", e)