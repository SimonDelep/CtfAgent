import sys
print(sys.path)
try:
    import scapy.all
    print("scapy found")
except Exception as e:
    print(f"scapy error: {e}")