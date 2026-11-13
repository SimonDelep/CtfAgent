# Le contenu entre accolades est: d0c_@yz@gl_mn0j_pm3z3_g0_o00s
# Essayons de remplacer @ par _
content = "d0c_@yz@gl_mn0j_pm3z3_g0_o00s"
content_underscore = content.replace("@", "_")
print("Avec @ = _:")
print(content_underscore)

# Et si @ est un espace ?
content_space = content.replace("@", " ")
print("\nAvec @ = espace:")
print(content_space)