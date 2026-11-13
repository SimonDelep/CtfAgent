SCHEMA = {
  "name": "vigenere_bruteforce",
  "description": "Teste plusieurs clés Vigenère sur un ciphertext et affiche les résultats déchiffrés",
  "parameters": {
    "properties": {
      "ciphertext": {
        "description": "Le ciphertext à déchiffrer",
        "type": "string"
      },
      "keys": {
        "description": "Liste des clés à tester",
        "items": {
          "type": "string"
        },
        "type": "array"
      }
    },
    "required": [
      "ciphertext",
      "keys"
    ],
    "type": "object"
  }
}

def main(args):
    def vigenere_decrypt(ciphertext, key):
        result = []
        key_index = 0
        for char in ciphertext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                key_char = key[key_index % len(key)]
                key_shift = ord(key_char.lower()) - ord('a')
                decrypted = chr((ord(char) - base - key_shift) % 26 + base)
                result.append(decrypted)
                key_index += 1
            else:
                result.append(char)
        return ''.join(result)

    ciphertext = args["ciphertext"]
    keys = args["keys"]

    for key in keys:
        decrypted = vigenere_decrypt(ciphertext, key)
        print(f"Clé '{key}': {decrypted}")

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
