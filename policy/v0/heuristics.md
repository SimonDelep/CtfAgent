# Heuristiques de recherche (v0)

- Toujours commencer par `file` et `strings` sur chaque fichier fourni.
- Un service `nc` + binaire → penser exploitation (pwn) ; binaire seul → reverse.
- `.pcap` → analyse réseau ; image → métadonnées puis stéganographie.
- Énoncé mentionnant RSA / clés / chiffrement → crypto : chercher les paramètres
  faibles (petit exposant, module factorisable).
- URL / cookie / login → web : explorer endpoints, paramètres, en-têtes.
- Préférer une vérification peu coûteuse avant une attaque lourde.
- Noter chaque piste déjà essayée pour ne pas la refaire.
