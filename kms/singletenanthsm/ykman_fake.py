#!/usr/bin/env python

# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_rsa_keys(key_size=2048):
    """Generates a private and public RSA key pair with the specified key size."""
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
    signature = private_key.sign(data, padding.PKCS1v15(), hash_algorithm)
    return signature


def verify_signature(public_key, data, signature, hash_algorithm=hashes.SHA256()):
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
    private_key, public_key = generate_rsa_keys()

    # Data to sign (as bytes)
    data_to_sign = b"This is the data to be signed."
    signature = sign_data(private_key, data_to_sign)
    print(f"Signature generated: {signature.hex()}")
    is_valid = verify_signature(public_key, data_to_sign, signature)
    if is_valid:
        print("Signature is VALID.")
    else:
        print("Signature is INVALID.")
