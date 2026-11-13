SCHEMA = {
  "name": "substitution_solver",
  "description": "Teste différentes substitutions monoalphabétiques sur un payload donné (leetspeak, ROT, Atbash, etc.)",
  "parameters": {
    "properties": {
      "payload": {
        "description": "Le payload à décoder",
        "type": "string"
      }
    },
    "required": [
      "payload"
    ],
    "type": "object"
  }
}

def main(args):
    payload = args['payload']
    
    results = []
    
    # 1. Leetspeak simple
    leetspeak_map = {
        '0': 'o', '1': 'i', '2': 'z', '3': 'e', '4': 'a', '5': 's', 
        '6': 'g', '7': 't', '8': 'b', '9': 'q', '@': 'a', '!': 'i'
    }
    decoded = "".join(leetspeak_map.get(c, c) for c in payload)
    results.append(("Leetspeak simple", decoded))
    
    # 2. Atbash
    atbash_result = ""
    for c in payload:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            atbash_result += chr(base + (25 - (ord(c) - base)))
        else:
            atbash_result += c
    results.append(("Atbash", atbash_result))
    
    # 3. ROT1-25
    for rot in range(1, 26):
        result = ""
        for c in payload:
            if c.isalpha():
                base = ord('a') if c.islower() else ord('A')
                result += chr((ord(c) - base + rot) % 26 + base)
            else:
                result += c
        results.append((f"ROT{rot}", result))
    
    # 4. XOR avec clés courantes
    for key in [6, 7, 13, 32, 64, 128]:
        result = "".join(chr(ord(c) ^ key) for c in payload)
        results.append((f"XOR {key}", result))
    
    # 5. Inverse de la transformation esnp -> csaw
    # e->c (-2), s->s (0), n->a (-13), p->w (+7)
    # Appliquer cette transformation sur tout le payload
    transform = [-2, 0, -13, 7]
    result = ""
    for i, c in enumerate(payload):
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            shift = transform[i % len(transform)]
            result += chr((ord(c) - base + shift) % 26 + base)
        else:
            result += c
    results.append(("Transform esnp->csaw", result))
    
    return results

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
