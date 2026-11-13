SCHEMA = {
  "name": "vigenere_decrypt",
  "description": "Déchiffre un texte avec Vigenère et une clé donnée. Retourne le plaintext.",
  "parameters": {
    "properties": {
      "ciphertext": {
        "description": "texte chiffré",
        "type": "string"
      },
      "key": {
        "description": "clé Vigenère",
        "type": "string"
      }
    },
    "required": [
      "ciphertext",
      "key"
    ],
    "type": "object"
  }
}

def vigenere_decrypt(ciphertext, key):
    result = []
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')
            shift = ord(key[key_index % len(key)].lower()) - ord('a')
            decrypted_char = chr((ord(char) - base - shift) % 26 + base)
            result.append(decrypted_char)
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

def main(args):
    ciphertext = args['ciphertext']
    key = args['key']
    print(vigenere_decrypt(ciphertext, key))

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
