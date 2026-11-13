payload = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"

# Convertir en hex
hex_payload = payload.encode('utf-8').hex()
print("Hex:", hex_payload)

# Peut-être que c'est un XOR avec une clé courte
# Essayons de XOR avec différentes clés pour voir si on obtient du texte lisible

target = "doc_"  # Ce que nous espérons voir au début (par exemple "doc_" ou "the_")
target_bytes = target.encode('utf-8')
payload_bytes = payload.encode('utf-8')

# Trouver la clé XOR qui transforme payload en target
key = []
for i in range(len(target_bytes)):
    if i < len(payload_bytes):
        k = payload_bytes[i] ^ target_bytes[i]
        key.append(k)
        print(f"payload[{i}]={payload_bytes[i]} ^ target[{i}]={target_bytes[i]} = {k} ('{chr(k) if 32 <= k < 127 else '?'}')")

print("Clé XOR potentielle:", key)