import base64
from Cryptodome.PublicKey import RSA
import requests
from base64 import urlsafe_b64decode
# from Crypto.PublicKey import RSA
import subprocess
from base64 import urlsafe_b64decode

def base64url_decode(data):
    return urlsafe_b64decode(data + b'=' * (-len(data) % 4))
# Download the JWK (public key)
def download_jwk():
    print(f"[*] Attempting to download JWK...")
    response = requests.get("https://catclub-8.ctf.intigriti.io/jwks.json")

    if response.status_code == 200:
        print("[*] JWK download successful")
        print(f"[*] JWK Response: {response.json()}")
        return response.json()['keys'][0]
    else:
        print(f"[!] Failed to download JWK: {response.text}")
        return None

# Recreate the RSA public key from JWK components (n and e) and save it to a file
def rsa_public_key_from_jwk(jwk):
    print(f"[*] Recreating RSA Public Key from JWK...")

    n = base64url_decode(jwk['n'].encode('utf-8'))
    e = base64url_decode(jwk['e'].encode('utf-8'))

    n_int = int.from_bytes(n, 'big')
    e_int = int.from_bytes(e, 'big')

    rsa_key = RSA.construct((n_int, e_int))
    public_key_pem = rsa_key.export_key('PEM')

    # Save the public key to a file with a newline at the end
    with open("recovered_public.key", "wb") as f:
        f.write(public_key_pem)
        if not public_key_pem.endswith(b'\n'):
            f.write(b"\n")

    print(
        f"[*] Recreated RSA Public Key saved to 'recovered_public.key':\n{public_key_pem.decode()}")
    return

if __name__ == "__main__":
    jwk = download_jwk()
    if jwk:
        rsa_public_key_from_jwk(jwk)