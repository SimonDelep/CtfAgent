SCHEMA = {
  "name": "wav_analyzer",
  "description": "Extrait et analyse les données d'un fichier WAV : échantillons bruts, LSB, canaux séparés, recherche de patterns",
  "parameters": {
    "properties": {
      "mode": {
        "description": "Mode d'analyse",
        "enum": [
          "raw",
          "lsb",
          "channels",
          "silence"
        ],
        "type": "string"
      },
      "wav_file": {
        "description": "Chemin du fichier WAV",
        "type": "string"
      }
    },
    "type": "object"
  }
}

import struct
import os

def main(args):
    wav_file = args.get('wav_file', 'audio.wav')
    mode = args.get('mode', 'raw')
    
    # Lire le fichier WAV
    with open(wav_file, 'rb') as f:
        # RIFF header
        riff = f.read(4)
        if riff != b'RIFF':
            return f"Error: Not a RIFF file (got {riff})"
        
        file_size = struct.unpack('<I', f.read(4))[0]
        wave = f.read(4)
        if wave != b'WAVE':
            return f"Error: Not a WAVE file"
        
        # Trouver le chunk fmt
        while True:
            chunk_id = f.read(4)
            if len(chunk_id) < 4:
                return "Error: No fmt chunk found"
            chunk_size = struct.unpack('<I', f.read(4))[0]
            if chunk_id == b'fmt ':
                fmt_data = f.read(chunk_size)
                audio_format, num_channels, sample_rate, _, _, bits_per_sample = struct.unpack('<HHIIHH', fmt_data)
                break
            else:
                f.seek(chunk_size, 1)
        
        # Trouver le chunk data
        while True:
            chunk_id = f.read(4)
            if len(chunk_id) < 4:
                return "Error: No data chunk found"
            chunk_size = struct.unpack('<I', f.read(4))[0]
            if chunk_id == b'data':
                break
            else:
                f.seek(chunk_size, 1)
        
        # Lire les données audio
        data = f.read(chunk_size)
    
    result = f"WAV Info: {num_channels} channels, {sample_rate} Hz, {bits_per_sample} bits, {len(data)} bytes\n"
    
    if mode == 'raw':
        # Afficher les premiers bytes bruts
        result += f"First 100 bytes (hex): {data[:100].hex()}\n"
        result += f"First 100 bytes (repr): {repr(data[:100])}\n"
        
    elif mode == 'lsb':
        # Extraire les LSB de chaque échantillon
        if bits_per_sample == 16:
            samples = struct.unpack('<' + 'h' * (len(data) // 2), data)
        else:
            samples = struct.unpack('<' + 'b' * len(data), data)
        
        # Extraire LSB de chaque échantillon
        lsb_bits = [s & 1 for s in samples]
        
        # Regrouper par 8 pour former des bytes
        lsb_bytes = []
        for i in range(0, len(lsb_bits) - 7, 8):
            byte_val = 0
            for j in range(8):
                byte_val |= (lsb_bits[i + j] << j)
            lsb_bytes.append(byte_val)
        
        # Afficher les premiers bytes LSB
        result += f"LSB bytes (first 200): {bytes(lsb_bytes[:200])}\n"
        result += f"LSB bytes (hex first 200): {bytes(lsb_bytes[:200]).hex()}\n"
        
        # Essayer de trouver des chaînes imprimables
        printable = ''.join(chr(b) if 32 <= b < 127 else '.' for b in lsb_bytes[:500])
        result += f"LSB printable (first 500): {printable}\n"
        
    elif mode == 'channels':
        if num_channels == 2:
            # Séparer les canaux
            left = data[0::2]
            right = data[1::2]
            result += f"Left channel first 100 bytes: {left[:100].hex()}\n"
            result += f"Right channel first 100 bytes: {right[:100].hex()}\n"
            
            # Extraire LSB de chaque canal séparément
            left_samples = struct.unpack('<' + 'h' * (len(left) // 2), left)
            right_samples = struct.unpack('<' + 'h' * (len(right) // 2), right)
            
            left_lsb = bytes([s & 1 for s in left_samples])
            right_lsb = bytes([s & 1 for s in right_samples])
            
            result += f"Left LSB first 100: {left_lsb[:100]}\n"
            result += f"Right LSB first 100: {right_lsb[:100]}\n"
            
    elif mode == 'silence':
        # Trouver les zones de silence (valeurs proches de 0)
        if bits_per_sample == 16:
            samples = struct.unpack('<' + 'h' * (len(data) // 2), data)
        else:
            samples = struct.unpack('<' + 'b' * len(data), data)
        
        # Compter les échantillons silencieux (|sample| < 100)
        silent_count = sum(1 for s in samples if abs(s) < 100)
        result += f"Total samples: {len(samples)}, Silent samples (<100): {silent_count} ({100*silent_count/len(samples):.2f}%)\n"
        
        # Trouver les positions des silences
        silent_positions = [i for i, s in enumerate(samples) if abs(s) < 100]
        result += f"First 50 silent positions: {silent_positions[:50]}\n"
    
    return result

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
