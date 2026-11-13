# Peut-être que "esnp" est juste un déguisement et que le vrai préfixe est "csaw"
# Et que le payload est aussi déguisé d'une manière similaire

# Regardons la transformation caractère par caractère
# e -> c : décalage -2
# s -> s : décalage 0
# n -> a : décalage -13 (ou +13)
# p -> w : décalage +7

# Peut-être que c'est une substitution basée sur une clé de mot de passe
# Ou peut-être que c'est simplement "csaw" au lieu de "esnp" et le reste est le même

# Essayons de remplacer juste le préfixe
decoded = "esnp{d0c_@yz@gl_mn0j_pm3z3_g0_o00s}"
flag_candidate = "csaw{" + decoded[5:]
print("En remplaçant juste le préfixe:", flag_candidate)

# Maintenant, décodons le payload comme du leetspeak
payload = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"

# Mapping leetspeak plus complet
leetspeak = {
    '0': 'o', '1': 'i', '2': 'z', '3': 'e', '4': 'a', '5': 's', 
    '6': 'g', '7': 't', '8': 'b', '9': 'q', '@': 'a',
    '!': 'i', '|': 'l', '3': 'e', '4': 'a', '5': 's', '7': 't'
}

decoded_payload = ""
for c in payload:
    decoded_payload += leetspeak.get(c, c)

print("Payload décodé (leetspeak):", decoded_payload)

# "doc_ayzagl_mnoj_pmeze_go_ooos"
# Peut-être que c'est "doc_ayzagl" -> "doc_ayzagl" n'a pas de sens
# Mais "doc" pourrait être "doc" (document)
# "ayzagl" -> peut-être "ayzagl" est un mot déguisé

# Essayons de voir si c'est une substitution ROT sur le payload
for rot in range(26):
    result = ""
    for c in decoded_payload:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            result += chr((ord(c) - base + rot) % 26 + base)
        else:
            result += c
    if rot in [0, 13]:  # Juste quelques tests
        print(f"ROT{rot}: {result}")