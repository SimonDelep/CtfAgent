SCHEMA = {
  "name": "list_files",
  "description": "Liste les fichiers du workdir en Python pour éviter les problèmes UTF-8",
  "parameters": {
    "properties": {
      "path": {
        "description": "Chemin à lister",
        "type": "string"
      }
    },
    "type": "object"
  }
}

def main(args):
    import os
    path = args.get("path", ".")
    try:
        entries = os.listdir(path)
        for e in sorted(entries):
            full = os.path.join(path, e)
            if os.path.isfile(full):
                size = os.path.getsize(full)
                print(f"{e} ({size} bytes)")
            else:
                print(f"{e}/")
    except Exception as ex:
        print(f"Error: {ex}")

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
