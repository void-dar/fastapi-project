from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from base64 import b64encode

# Generate EC private key
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# Export keys to PEM (bytes)
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Encode to base64 so they can be safely saved in .env
private_b64 = b64encode(private_pem).decode('utf-8')
public_b64 = b64encode(public_pem).decode('utf-8')

# Save to .env file
with open("key.txt", "w") as f:
    f.write(f"PRIVATE_KEY={private_b64}\n")
    f.write(f"PUBLIC_KEY={public_b64}\n")

print("✅ Keys generated and saved to .env")
