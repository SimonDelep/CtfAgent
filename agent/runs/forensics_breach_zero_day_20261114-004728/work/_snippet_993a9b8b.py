# Construisons quelques candidats de flag
indicator = "PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j"
service = "Windows Update"
backdoor = "WindowsUpdate.exe"

# Différentes variantes
candidates = [
    f"csaw{{{indicator}_{service}_{backdoor}}}",
    f"csaw{{{indicator.replace('=', '_')}_{service}_{backdoor}}}",
    f"csaw{{SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j_{service}_{backdoor}}}",
    f"csaw{{PDQ_SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j_{service.replace(' ', '_')}_{backdoor}}}",
    f"csaw{{PDQ=SXrPVed5HjrAoV-rtyzpnVs+i4K9gVVk9j_{service.replace(' ', '_')}_{backdoor}}}",
]

for c in candidates:
    print(c)