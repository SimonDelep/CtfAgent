import os
for f in os.listdir('.'):
    try:
        print(f.encode('utf-8'))
    except:
        print(repr(f))