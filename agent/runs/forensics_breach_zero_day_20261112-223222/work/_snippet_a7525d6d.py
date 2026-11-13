import base64

# Chaînes suspectes du memdump
strings_to_try = [
    "PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j",
    "ag2+b2tfU2=A=wO+c7vlO,TDDXG_7QacpvSoNa66Ckif",
    "Fq7zVQSp3cct/Nk-ebjmHW5K62RoJLQNfcRAp/C",
    "h.H4_7LFT6Znhia33n=Bei3P85CrBgiev45Go+v/rR",
    "McB5K5PBs2sD6crsh2d6OQm79+o3",
    "r9-q,cRFlMNCSigV44lGS/GRn8gOvXr7Ci6m-38CvN8",
    "ItqFNGUIX8pLcraot05NkFEolV,hnH/zocbrk6,I",
    "6y2ytiICPd-IyMF_B9ATDSAann+BwY",
    "F06eS8E9fHSTpaJZ=LpkmfcAKYXI+Ju",
    "wM,6I6,=x.89QYHX=RRHBUAyUv8gePaJ0",
    "4o3nBh0xWxc0X0+DaNOnY8IN4",
    "a0.RSg7MS6Z8+TBQ2oWVRMFpZlLqsVwBAf",
    "i8VNUP.l9SmEEoWL-2HyY5fTbryObD3b5574yRp",
]

for s in strings_to_try:
    # Essayer de décoder en Base64 standard
    try:
        # Remplacer les caractères non-standard
        s_std = s.replace('-', '+').replace('_', '/')
        # Ajouter du padding si nécessaire
        padding = 4 - len(s_std) % 4
        if padding != 4:
            s_std += '=' * padding
        decoded = base64.b64decode(s_std)
        print(f"Original: {s}")
        print(f"Decoded: {decoded}")
        print()
    except Exception as e:
        pass