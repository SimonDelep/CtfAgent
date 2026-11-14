# Taille de la structure chorister_t
# name[0x38] = 56 bytes
# sing = 8 bytes
# transcript = 8 bytes  
# transcript_len = 8 bytes
# active = 4 bytes
# Total = 56 + 8 + 8 + 8 + 4 = 84 bytes

# malloc aligne sur 16 bytes, donc 84 -> 96 bytes (0x60)
# Mais avec les headers malloc, on obtient des chunks de taille spécifique

# Pour l'UAF, on veut:
# 1. alloc A (taille X)
# 2. free A
# 3. alloc B (même taille X) - B réutilise l'emplacement de A
# 4. Via l'ancien pointeur A, on modifie quelque chose dans B

# Le transcript est alloué séparément. Si on peut écraser le pointeur transcript
# de A (qui pointe maintenant vers B via UAF), on peut faire pointer transcript
# vers une adresse intéressante.

# Structure:
# - choir[idx] pointe vers la structure chorister_t
# - Après retire(), choir[idx] pointe toujours vers la même mémoire (libérée)
# - Après restore(), on réactive le même index
# - Si on recrute un nouveau choriste à un autre index, on peut avoir des interactions

# Stratégie:
# 1. Recruter choriste 0 avec transcript de taille 0x20 (32 bytes)
# 2. Retirer choriste 0 (libère structure ET transcript)
# 3. Recruter choriste 1 avec transcript de taille 0x20 (réutilise l'emplacement du transcript de 0)
# 4. Restaurer choriste 0 (maintenant choir[0] pointe vers mémoire libérée)
# 5. Via rename ou inscribe sur choriste 0, on peut écraser le pointeur transcript de choriste 1

# En fait, la structure chorister_t est libérée, pas juste le transcript.
# Donc après retire, choir[idx] pointe vers une structure libérée.
# Si on recrute un nouveau choriste, il peut réutiliser cette mémoire.

# Pour l'UAF classique:
# 1. A = malloc(size)
# 2. free(A)
# 3. B = malloc(size)  # B réutilise l'emplacement de A
# 4. Utiliser A (maintenant pointe vers B)

# Ici:
# 1. Recruter choriste 0 -> malloc(sizeof(chorister_t)) + malloc(transcript_len)
# 2. Retirer choriste 0 -> free(transcript) + free(chorister_t)
# 3. Recruter choriste 1 -> malloc(sizeof(chorister_t)) + malloc(transcript_len)
#    Si les tailles sont identiques, le malloc peut réutiliser les mêmes emplacements
# 4. Restaurer choriste 0 -> active = 1 sur la structure libérée (qui est maintenant choriste 1)
# 5. Maintenant choir[0] et choir[1] pointent vers la même structure!

# En écrivant via rename/inscribe sur choriste 0, on modifie choriste 1

print("Analyse de la structure:")
print("sizeof(chorister_t) = 56 + 8 + 8 + 8 + 4 =", 56 + 8 + 8 + 8 + 4)
print("Aligné sur 16: 84 -> 96 bytes (0x60)")
print("Pour transcript, si on utilise 0x20 (32), le chunk sera 0x40 (64) ou 0x30 (48)")