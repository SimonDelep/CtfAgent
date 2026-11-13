import base64

# Chaînes encodées trouvées dans le memdump
encoded_strings = [
    "SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j",
    "ag2+b2tfU2=A=wO+c7vlO,TDDXG_7QacpvSoNa66Ckif",
    "RRJTJvMD4Xi0ZVY,4zR",
    "Fq7zVQSp3cct/Nk-ebjmHW5K62RoJLQNfcRAp/C",
    "h.H4_7LFT6Znhia33n=Bei3P85CrBgiev45Go+v/rR",
    "im5DCjJwPWi.Q",
    "LPWi.kAK.99N,Eec7c",
    "McB5K5PBs2sD6crsh2d6OQm79+o3",
    "0=gHtNRu/d4j1/PMhDn,z1inu-9Z,4MGyAKE/bs",
    "+WF0GzPC5riP",
    "k0q+yE6u=AMNABFiOg",
    "r9-q,cRFlMNCSigV44lGS/GRn8gOvXr7Ci6m-38CvN8",
    "ItqFNGUIX8pLcraot05NkFEolV,hnH/zocbrk6,I",
    "6y2ytiICPd-IyMF_B9ATDSAann+BwY",
    "F06eS8E9fHSTpaJZ=LpkmfcAKYXI+Ju",
    "DJcy-PC,1V_ymjQviVlqkT4cst4",
    "wM,6I6,=x.89QYHX=RRHBUAyUv8gePaJ0",
    "ftrvbqAEik"
]

for s in encoded_strings:
    # Essayer Base64 URL-safe
    try:
        # Remplacer les caractères URL-safe par les caractères Base64 standards
        s_std = s.replace('-', '+').replace('_', '/')
        # Ajouter du padding si nécessaire
        padding = 4 - len(s_std) % 4
        if padding != 4:
            s_std += '=' * padding
        decoded = base64.b64decode(s_std)
        print(f"Original: {s}")
        print(f"Decoded (bytes): {decoded}")
        try:
            print(f"Decoded (str): {decoded.decode('utf-8')}")
        except:
            pass
        print("---")
    except Exception as e:
        print(f"Failed for {s}: {e}")