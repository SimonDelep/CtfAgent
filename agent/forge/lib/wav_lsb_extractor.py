SCHEMA = {
  "name": "wav_lsb_extractor",
  "description": "Extrait les bits de poids faible (LSB) des échantillons audio d'un fichier WAV et les convertit en chaîne de caractères",
  "parameters": {
    "properties": {
      "bits_per_char": {
        "default": 8,
        "description": "Nombre de bits par caractère (par défaut 8)",
        "type": "integer"
      },
      "wav_file": {
        "description": "Chemin du fichier WAV",
        "type": "string"
      }
    },
    "required": [
      "wav_file"
    ],
    "type": "object"
  }
}

import struct
import wave

def main(args):
    wav_file = args.get("wav_file", "12345678 (1).wav")
    bits_per_char = args.get("bits_per_char", 8)
    
    try:
        with wave.open(wav_file, 'rb') as wf:
            params = wf.getparams()
            n_channels = params.nchannels
            sampwidth = params.sampwidth
            n_frames = params.nframes
            
            # Lire tous les frames
            frames = wf.readframes(n_frames)
            
            # Extraire les LSB
            lsb_bits = []
            for byte in frames:
                lsb_bits.append(byte & 1)
            
            # Convertir en bytes
            result = []
            for i in range(0, len(lsb_bits) - bits_per_char + 1, bits_per_char):
                byte_val = 0
                for j in range(bits_per_char):
                    byte_val = (byte_val << 1) | lsb_bits[i + j]
                if byte_val > 0 and byte_val < 128:  # ASCII imprimable
                    result.append(chr(byte_val))
                elif byte_val == 0:
                    result.append(' ')
            
            message = ''.join(result)
            print(f"Longueur des bits LSB: {len(lsb_bits)}")
            print(f"Message extrait (premier 500 chars): {message[:500]}")
            print(f"Message complet: {message}")
            
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
