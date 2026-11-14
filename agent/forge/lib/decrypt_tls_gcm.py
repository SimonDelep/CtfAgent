SCHEMA = {
  "name": "decrypt_tls_gcm",
  "description": "Décrypte les paquets TLS 1.2 AES-GCM à partir de capture.pcapng en utilisant les clés du fichier vcheck.log",
  "parameters": {
    "properties": {
      "session_id": {
        "description": "Session 1 ou 2",
        "type": "string"
      }
    },
    "required": [
      "session_id"
    ],
    "type": "object"
  }
}

from scapy.all import rdpcap, TCP, Raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
import struct

def main(args):
    # Charger le pcap
    packets = rdpcap('capture.pcapng')

    # Définir les sessions
    session1_client_random = '6aa4f15c976aa8e351b7fe1246ca34d77983e3a2340aafaa6b28502f04e0895a'
    session2_client_random = '6aa4f15e9f5793cf966ea28bc7635164064d751c19a6eb36fa4695672798d4fd'

    # Master secrets
    session1_master = '7843e5988faf198cc4c2c10d20e6af50fd868e2f712d86f2cca808c67fab8d77f8b268eca9d3f6fb66786a78158ebd05'
    session2_master = '4c47398320e2b2d40eac1b86168a7cb854d15e49d7c086a63307c25a01d2d1b75f1817f7f3a31dccab08dba5e106f31c'

    def generate_key_block(master_secret, label, seed, length):
        """Génère le key_block pour TLS 1.2 avec SHA256"""
        def prf_hmac_sha256(secret, data):
            h = hmac.HMAC(secret, hashes.SHA256(), backend=default_backend())
            h.update(data)
            return h.finalize()
        
        A = prf_hmac_sha256(master_secret, label + seed)
        result = b''
        current_A = A
        while len(result) < length:
            result += prf_hmac_sha256(master_secret, current_A + label + seed)
            current_A = prf_hmac_sha256(master_secret, current_A)
        return result[:length]

    def hex_to_bytes(h):
        return bytes.fromhex(h)

    # Sélectionner la session
    if args['session_id'] == '1':
        master_secret_hex = session1_master
    else:
        master_secret_hex = session2_master

    master_secret = hex_to_bytes(master_secret_hex)

    # Générer key_block (40 bytes pour AES-GCM: 16+16+4+4)
    # Le seed pour "key expansion" est client_random + server_random
    # Mais on n'a pas le server_random facilement... 
    # En TLS 1.2, le seed est client_random || server_random
    # Pour le key_block, on utilise le master_secret et le seed = client_random + server_random
    
    # On doit extraire le server_random du pcap
    # Pour simplifier, on va essayer avec un seed vide ou dériver autrement
    
    # En fait, le key_block est généré avec: PRF(master_secret, "key expansion", client_random + server_random)
    # On a besoin du server_random
    
    # Pour l'instant, essayons avec seed = client_random (approximation)
    # Ou mieux: on peut extraire le server_random du Server Hello
    
    # Laissons une implémentation qui essaie de trouver les paquets
    # et décode avec les clés dérivées
    
    # Pour TLS 1.2, la structure du key_block est:
    # client_write_key (16) + server_write_key (16) + client_write_iv (4) + server_write_iv (4)
    # Mais le seed doit être client_random || server_random
    
    # On va extraire le server_random du pcap
    server_random = None
    for pkt in packets:
        if TCP in pkt and Raw in pkt:
            payload = bytes(pkt[Raw].load)
            if len(payload) > 43:  # Client Hello ou Server Hello
                # Server Hello: type=0x02, version, random(32), ...
                if payload[0] == 0x16:  # Handshake
                    # Handshake header: type(1) + version(2) + length(2)
                    if len(payload) >= 43:
                        # Server Hello random est aux bytes 43-74 (32 bytes)
                        # Mais c'est dans le record TLS
                        # Record: type(1) + version(2) + length(2) + handshake
                        # Handshake: type(1) + length(3) + version(2) + random(32)
                        if payload[5] == 0x02:  # Server Hello
                            server_random = payload[43:75]
                            break
    
    if server_random is None:
        # Fallback: utiliser un seed par défaut
        seed = bytes.fromhex('19f6457f') + b'\x00' * 28  # Session 1 Server Random partiel
    else:
        seed = bytes.fromhex('6aa4f15c976aa8e351b7fe1246ca34d77983e3a2340aafaa6b28502f04e0895a') + server_random
        # Attends, seed = client_random || server_random
        # Pour session 1, client_random = 6aa4f15c...
        if args['session_id'] == '1':
            client_rand = bytes.fromhex('6aa4f15c976aa8e351b7fe1246ca34d77983e3a2340aafaa6b28502f04e0895a')
        else:
            client_rand = bytes.fromhex('6aa4f15e9f5793cf966ea28bc7635164064d751c19a6eb36fa4695672798d4fd')
        seed = client_rand + server_random
    
    key_block = generate_key_block(master_secret, b'key expansion', seed, 40)
    
    client_write_key = key_block[0:16]
    server_write_key = key_block[16:32]
    client_write_iv = key_block[32:36]
    server_write_iv = key_block[36:40]
    
    print(f"Session {args['session_id']}")
    print(f"client_write_key: {client_write_key.hex()}")
    print(f"server_write_key: {server_write_key.hex()}")
    print(f"client_write_iv: {client_write_iv.hex()}")
    print(f"server_write_iv: {server_write_iv.hex()}")
    
    # Maintenant décrypter les Application Data
    decrypted_results = []
    
    # Compteurs de séquence séparés pour client->server et server->client
    client_seq = 0
    server_seq = 0
    
    for i, pkt in enumerate(packets):
        if TCP in pkt and Raw in pkt:
            payload = bytes(pkt[Raw].load)
            if len(payload) >= 5:
                record_type = payload[0]
                if record_type == 0x17:  # Application Data
                    length = struct.unpack('>H', payload[3:5])[0]
                    if len(payload) >= 5 + length:
                        encrypted_data = payload[5:5+length]
                        
                        if len(encrypted_data) >= 8:
                            explicit_nonce = encrypted_data[:8]
                            ciphertext_with_tag = encrypted_data[8:]
                            
                            # Essayer client->server
                            nonce = client_write_iv + explicit_nonce
                            try:
                                aesgcm = AESGCM(client_write_key)
                                decrypted = aesgcm.decrypt(nonce, ciphertext_with_tag, None)
                                decrypted_results.append(f"C->S seq={client_seq}: {decrypted}")
                                client_seq += 1
                            except Exception as e1:
                                # Essayer server->client
                                nonce = server_write_iv + explicit_nonce
                                try:
                                    aesgcm = AESGCM(server_write_key)
                                    decrypted = aesgcm.decrypt(nonce, ciphertext_with_tag, None)
                                    decrypted_results.append(f"S->C seq={server_seq}: {decrypted}")
                                    server_seq += 1
                                except:
                                    decrypted_results.append(f"seq? échec: {ciphertext_with_tag[:20].hex()}")
    
    print("\n--- Données déchiffrées ---")
    for d in decrypted_results:
        print(d)
    
    return decrypted_results

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
