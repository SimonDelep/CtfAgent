SCHEMA = {
  "name": "pcap_tcp_extractor",
  "description": "Extrait les données TCP d'un fichier pcap pour un port donné, en reconstituant les flux",
  "parameters": {
    "properties": {
      "pcap_file": {
        "description": "Chemin du fichier pcap",
        "type": "string"
      },
      "port": {
        "description": "Port à filtrer",
        "type": "integer"
      }
    },
    "required": [
      "pcap_file",
      "port"
    ],
    "type": "object"
  }
}

def main(args):
    import subprocess
    import re

    pcap_file = args['pcap_file']
    port = args['port']

    # Utiliser tcpdump pour extraire les données brutes du port spécifié
    cmd = f"tcpdump -r {pcap_file} -A -s 0 'tcp port {port}' 2>/dev/null"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    output = result.stdout
    print(f"=== Flux TCP sur port {port} ===")
    print(output[:5000] if len(output) > 5000 else output)

    # Chercher des patterns intéressants
    patterns = [r'csaw\{[^}]+\}', r'flag\{[^}]+\}', r'[A-Za-z0-9_]{20,}', r'HTTP/1\.[01]', r'POST|GET']
    for p in patterns:
        matches = re.findall(p, output)
        if matches:
            print(f"\nPattern '{p}': {matches[:5]}")

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
