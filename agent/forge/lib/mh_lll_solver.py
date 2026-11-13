SCHEMA = {
  "name": "mh_lll_solver",
  "description": "Résout Merkle-Hellman subset-sum avec LLL : construit matrice, réduit, extrait vecteur binaire et convertit en message",
  "parameters": {
    "properties": {
      "ciphertext": {
        "description": "Ciphertext à décrypter",
        "type": "integer"
      },
      "pubkey": {
        "description": "Clé publique (liste d'entiers)",
        "items": {
          "type": "integer"
        },
        "type": "array"
      }
    },
    "required": [
      "pubkey",
      "ciphertext"
    ],
    "type": "object"
  }
}

def main(args):
    pubkey = args["pubkey"]
    ciphertext = args["ciphertext"]
    n = len(pubkey)
    
    # Construire matrice LLL pour subset-sum
    # Matrice (n+1) x (n+1)
    # Lignes 0..n-1: 1 sur diagonale, -pubkey[i] en dernière colonne
    # Ligne n: ciphertext en dernière colonne
    
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        matrix[i][i] = 1
        matrix[i][n] = -pubkey[i]
    matrix[n][n] = ciphertext
    
    # LLL implementation
    def lll(B, delta=0.99):
        n_rows = len(B)
        n_cols = len(B[0])
        
        # Convertir en float
        B = [[float(x) for x in row] for row in B]
        
        # Gram-Schmidt
        def gs(B):
            m = len(B)
            n = len(B[0])
            Q = [[0.0]*n for _ in range(m)]
            mu = [[0.0]*m for _ in range(m)]
            for i in range(m):
                for j in range(n):
                    Q[i][j] = B[i][j]
                for k in range(i):
                    dot = sum(Q[i][j]*Q[k][j] for j in range(n))
                    norm2 = sum(Q[k][j]**2 for j in range(n))
                    if norm2 > 1e-10:
                        mu[i][k] = dot / norm2
                        for j in range(n):
                            Q[i][j] -= mu[i][k] * Q[k][j]
            return Q, mu
        
        Q, mu = gs(B)
        k = 1
        max_iter = n_rows * 200
        it = 0
        
        while k < n_rows and it < max_iter:
            it += 1
            
            # Size reduction
            for j in range(k-1, -1, -1):
                if abs(mu[k][j]) > 0.5:
                    q = round(mu[k][j])
                    for col in range(n_cols):
                        B[k][col] -= q * B[j][col]
            
            Q, mu = gs(B)
            
            # Lovasz condition
            norm_km1 = sum(Q[k-1][j]**2 for j in range(n_cols))
            norm_k = sum(Q[k][j]**2 for j in range(n_cols))
            
            if delta * norm_km1 <= norm_k + 1e-10:
                k += 1
            else:
                B[k], B[k-1] = B[k-1], B[k]
                k = max(k-1, 1)
                Q, mu = gs(B)
        
        return [[int(round(x)) for x in row] for row in B]
    
    reduced = lll(matrix)
    
    # Chercher vecteur solution
    for row in reduced:
        bits = row[:n]
        # Vérifier binaire
        if all(b in [0, 1] for b in bits):
            s = sum(bits[i] * pubkey[i] for i in range(n))
            if s == ciphertext:
                # Convertir en bytes (72 bits = 9 octets, MSB-first)
                msg_bytes = []
                for i in range(0, 72, 8):
                    byte_val = 0
                    for j in range(8):
                        if i+j < len(bits) and bits[i+j] == 1:
                            byte_val |= (1 << (7-j))
                    msg_bytes.append(byte_val)
                return f"SUCCESS: bytes={msg_bytes}, chars={bytes(msg_bytes)}"
        
        # Essayer conversion positive
        bits_pos = [1 if b > 0 else 0 for b in bits]
        s = sum(bits_pos[i] * pubkey[i] for i in range(n))
        if s == ciphertext:
            msg_bytes = []
            for i in range(0, 72, 8):
                byte_val = 0
                for j in range(8):
                    if i+j < len(bits_pos) and bits_pos[i+j] == 1:
                        byte_val |= (1 << (7-j))
                msg_bytes.append(byte_val)
            return f"SUCCESS (pos): bytes={msg_bytes}, chars={bytes(msg_bytes)}"
    
    # Retourner info sur la matrice réduite
    sample = reduced[0][:10]
    return f"No direct solution. Sample row: {sample}, norm={sum(x**2 for x in reduced[0])}"

# Test avec premier ciphertext
pubkey = [65363128684447571132776241699, 11274630258057967396026665723, 60559222278375482447330083794, 70238185910865550789020602007, 78077025115892356117353286514, 68689714170530501420950259719, 29127755965063579516555824180, 32796713726379898017330479743, 45519033311461958996652579847, 59481922183281857526171199789, 55495084400556906381284478613, 14576717810183300603139843389, 68589281729516899808716443746, 20296909478473654757282621208, 30537953005493837032599666770, 50700906734420621772366528392, 58720389817577647385263517768, 14929982408329983159745130411, 78957868028931941741179820628, 31015553887459374066166570979, 6479387240029285522500789709, 44834052244814211323002768825, 68880768174885210134417155701, 70728065516536734229876378887, 19940352925118383021332476475, 11926610039430690869353776248, 44284085306881906513505933290, 65961141103798053905550707203, 79222330366488147095589071397, 57716218939764421264346243444, 7143427741922311277425019977, 40102124774314571307421209726, 31106346336357167193152859646, 9869211918329061407583377438, 23696943552216795845779539234, 57055944207555268510811881306, 3327580670445191612826287616, 10613681056449056256265359590, 59950266048603035641387473838, 58927069738258076769247034796, 64441245461962817349401724273, 49297856532179662020349932300, 45182819049805987851607519281, 35526859738167888566962688623, 69627835129445026186765372626, 42091939332905056814598857452, 13191888117017754559626998031, 45745228201887970683682373391, 62110476246079115246893565460, 34936923235681473070158040183, 21488885432536346192206522870, 71644808849324143031304224752, 68376445195906361888347719926, 51783851937617327120469134628, 65557742112975106585661516908, 54063485202872162576322297308, 74075528359043450527980626626, 42713815274261871699013795581, 67529400689171140706681990106, 21066253853172746373456494821, 56109555611748530333568577993, 18657428926348050402028051389, 13281943995839590735434938781, 41966820243972970004685470533, 42715438945182202722984178323, 58189724253003705746237182254, 74448304789798298732507599455, 10158206024125176882906547212, 45737872490388506855671491388, 52889203964129866973885109, 50666903728700094028720106297, 51522962071682837162170650478]
ct = 1599051655305089304826823929251
print(mh_lll_solver({"pubkey": pubkey, "ciphertext": ct}))

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
