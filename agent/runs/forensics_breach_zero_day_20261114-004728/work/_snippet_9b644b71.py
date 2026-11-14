import re

# Lire le XML pour confirmer le service et le backdoor
with open('fenwick_security.xml', 'r') as f:
    xml_content = f.read()

# Chercher les EventID 7045 (création de service)
# Le format XML contient des balises Event
events = re.findall(r'<Event[^>]*>.*?</Event>', xml_content, re.DOTALL)

print("Services falsifiés (EventID 7045):")
for event in events:
    if '7045' in event:
        # Extraire le nom du service et le chemin
        service_match = re.search(r'<Data[^>]*>([^<]*Windows[^<]*)</Data>', event)
        path_match = re.search(r'<Data[^>]*>([^<]*\.exe[^<]*)</Data>', event)
        if service_match:
            print(f"  Service: {service_match.group(1).strip()}")
        if path_match:
            print(f"  Path: {path_match.group(1).strip()}")
        print()