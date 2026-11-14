# Le texte déchiffré avec 'cantfindit'
decrypted = "csaw{y0u_@lw@ys_kn0w_wh3r3_t0_l00k}"

# Extraire le contenu entre accolades
content = decrypted[5:-1]  # "y0u_@lw@ys_kn0w_wh3r3_t0_l00k"
print(f"Contenu entre accolades: {content}")

# Nettoyer le Leet Speak
leet_map = {
    '0': 'o',
    '@': 'a',
    '3': 'e',
    '1': 'i',
    '4': 'a',
    '5': 's',
    '7': 't',
    '8': 'b',
    '9': 'g',
    '!': 'i',
    '$': 's'
}

def clean_leet(text):
    result = []
    for char in text:
        result.append(leet_map.get(char, char))
    return ''.join(result)

cleaned = clean_leet(content)
print(f"Nettoyé (Leet -> lettres): {cleaned}")

# Essayer aussi avec le préfixe nettoyé
cleaned_full = "csaw{" + cleaned + "}"
print(f"Flag nettoyé complet: {cleaned_full}")

# Autres variantes possibles
print(f"\nAutres variantes:")
print(f"Juste le contenu nettoyé: {cleaned}")
print(f"Contenu brut: {content}")