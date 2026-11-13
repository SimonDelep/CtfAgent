import urllib.request
import urllib.error

# Test de base sans User-Agent
url = "http://low-tide-lb.ctf.csaw.io:8080/station/checkin"

user_agents = [
    "StationSync-Agent/2.1",
    "FieldSync-Client/3.0",
    "MonitorAgent/2.2",
    "StationSync-Agent/2.0",
    "RelayCheck-Bot/1.9"
]

for ua in user_agents:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        with urllib.request.urlopen(req, timeout=5) as response:
            print(f"[{ua}] Status: {response.status}")
            print(f"Response: {response.read().decode()[:500]}")
    except urllib.error.HTTPError as e:
        print(f"[{ua}] HTTP Error: {e.code}")
    except Exception as e:
        print(f"[{ua}] Error: {e}")