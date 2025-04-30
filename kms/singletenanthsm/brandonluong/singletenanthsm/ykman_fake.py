from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_rsa_keys(key_size=2048):
  """Generates an RSA key pair with the specified key size."""
  private_key = rsa.generate_private_key(
      public_exponent=65537,
      key_size=key_size,
  )
  public_key = private_key.public_key()
  return private_key, public_key


def sign_data(private_key, data, hash_algorithm=hashes.SHA256()):
  """Signs the provided data using the private key with PKCS#1.5 padding."""
  if not isinstance(data, bytes):
    raise TypeError("Data must be of type bytes")
  signature_bytes = private_key.sign(data, padding.PKCS1v15(), hash_algorithm)
  return signature_bytes


def verify_signature(
    public_key, data, signature, hash_algorithm=hashes.SHA256()
):
  """Verifies the signature of the data using the public key."""
  if not isinstance(data, bytes):
    raise TypeError("Data must be of type bytes")
  if not isinstance(signature, bytes):
    raise TypeError("Signature must be of type bytes")
  try:
    public_key.verify(signature, data, padding.PKCS1v15(), hash_algorithm)
    return True  # Signature is valid
  except InvalidSignature:
    return False  # Signature is invalid


if __name__ == "__main__":
  private_key_instance, public_key_instance = generate_rsa_keys()

  # Data to sign (as bytes)
  data_to_sign = b"This is the data to be signed."
  signature_bytes = sign_data(private_key_instance, data_to_sign)
  print(f"Signature generated: {signature_bytes.hex()}")
  is_valid = verify_signature(
      public_key_instance, data_to_sign, signature_bytes
  )
  if is_valid:
    print("Signature is VALID.")
  else:
    print("Signature is INVALID.")
