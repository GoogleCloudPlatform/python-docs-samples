#!/bin/python
# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.rom googleapiclient import discovery

import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, utils

from google.cloud import kms_v1
from google.cloud.kms_v1 import enums


# [START kms_create_asymmetric_key]
def create_asymmetric_key(project_id, location_id, key_ring_id, crypto_key_id):
    """Creates an RSA encrypt/decrypt key pair within a specified KeyRing."""

    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # The resource name of the KeyRing associated with the CryptoKey.
    parent = client.key_ring_path(project_id, location_id, key_ring_id)

    # Create the CryptoKey object template
    purpose = enums.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_DECRYPT
    algorithm = enums.CryptoKeyVersion.CryptoKeyVersionAlgorithm.\
        RSA_DECRYPT_OAEP_2048_SHA256
    crypto_key = {'purpose': purpose,
                  'version_template': {'algorithm': algorithm}}

    # Create a CryptoKey for the given KeyRing.
    response = client.create_crypto_key(parent, crypto_key_id, crypto_key)

    print('Created CryptoKey {}.'.format(response.name))
    return response
# [END kms_create_asymmetric_key]


# [START kms_get_asymmetric_public]
def get_asymmetric_public_key(key_name):
    """
    Retrieves the public key from a saved asymmetric key pair on Cloud KMS

    Example key_name:
      "projects/PROJECT_ID/locations/global/keyRings/RING_ID/cryptoKeys\
              /KEY_ID/cryptoKeyVersions/1"

    Requires:
      cryptography.hazmat.backends.default_backend
      cryptography.hazmat.primitives.serialization
    """

    client = kms_v1.KeyManagementServiceClient()
    response = client.get_public_key(key_name)

    key_txt = response.pem.encode('ascii')
    key = serialization.load_pem_public_key(key_txt, default_backend())
    return key
# [END kms_get_asymmetric_public]


# [START kms_decrypt_rsa]
def decrypt_rsa(ciphertext, key_name):
    """
    Decrypt the input ciphertext (bytes) using an
    'RSA_DECRYPT_OAEP_2048_SHA256' private key stored on Cloud KMS

    Example key_name:
      "projects/PROJECT_ID/locations/global/keyRings/RING_ID/cryptoKeys\
              /KEY_ID/cryptoKeyVersions/1"
    """

    client = kms_v1.KeyManagementServiceClient()
    response = client.asymmetric_decrypt(key_name, ciphertext)
    return response.plaintext
# [END kms_decrypt_rsa]


# [START kms_encrypt_rsa]
def encrypt_rsa(plaintext, key_name):
    """
    Encrypt the input plaintext (bytes) locally using an
    'RSA_DECRYPT_OAEP_2048_SHA256' public key retrieved from Cloud KMS

    Example key_name:
      "projects/PROJECT_ID/locations/global/keyRings/RING_ID/cryptoKeys\
              /KEY_ID/cryptoKeyVersions/1"

    Requires:
      cryptography.hazmat.primitives.asymmetric.padding
      cryptography.hazmat.primitives.hashes
    """
    # get the public key
    client = kms_v1.KeyManagementServiceClient()
    response = client.get_public_key(key_name)
    key_txt = response.pem.encode('ascii')
    public_key = serialization.load_pem_public_key(key_txt, default_backend())

    # encrypt plaintext
    pad = padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                       algorithm=hashes.SHA256(),
                       label=None)
    return public_key.encrypt(plaintext, pad)
# [END kms_encrypt_rsa]


# [START kms_sign_asymmetric]
def sign_asymmetric(message, key_name):
    """
    Create a signature for a message using a private key stored on Cloud KMS

    Example key_name:
      "projects/PROJECT_ID/locations/global/keyRings/RING_ID/cryptoKeys\
              /KEY_ID/cryptoKeyVersions/1"

    Requires:
      hashlib
    """
    # Note: some key algorithms will require a different hash function
    # For example, EC_SIGN_P384_SHA384 requires SHA384
    client = kms_v1.KeyManagementServiceClient()
    digest_bytes = hashlib.sha256(message).digest()

    digest_json = {'sha256': digest_bytes}

    response = client.asymmetric_sign(key_name, digest_json)
    return response.signature
# [END kms_sign_asymmetric]


# [START kms_verify_signature_rsa]
def verify_signature_rsa(signature, message, key_name):
    """
    Verify the validity of an 'RSA_SIGN_PSS_2048_SHA256' signature for the
    specified message

    Example key_name:
      "projects/PROJECT_ID/locations/global/keyRings/RING_ID/cryptoKeys\
              /KEY_ID/cryptoKeyVersions/1"

    Requires:
      cryptography.exceptions.InvalidSignature
      cryptography.hazmat.primitives.asymmetric.padding
      cryptography.hazmat.primitives.asymmetric.utils
      cryptography.hazmat.primitives.hashes
      hashlib
    """
    # get the public key
    client = kms_v1.KeyManagementServiceClient()
    response = client.get_public_key(key_name)
    key_txt = response.pem.encode('ascii')
    public_key = serialization.load_pem_public_key(key_txt, default_backend())

    # get the digest of the message
    digest_bytes = hashlib.sha256(message).digest()

    try:
        # Attempt verification
        public_key.verify(signature,
                          digest_bytes,
                          padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                      salt_length=32),
                          utils.Prehashed(hashes.SHA256()))
        # No errors were thrown. Verification was successful
        return True
    except InvalidSignature:
        return False
# [END kms_verify_signature_rsa]


# [START kms_verify_signature_ec]
def verify_signature_ec(signature, message, key_name):
    """
    Verify the validity of an 'EC_SIGN_P256_SHA256' signature
    for the specified message

    Example key_name:
      "projects/PROJECT_ID/locations/global/keyRings/RING_ID/cryptoKeys\
              /KEY_ID/cryptoKeyVersions/1"

    Requires:
      cryptography.exceptions.InvalidSignature
      cryptography.hazmat.primitives.asymmetric.ec
      cryptography.hazmat.primitives.asymmetric.utils
      cryptography.hazmat.primitives.hashes
      hashlib
    """
    # get the public key
    client = kms_v1.KeyManagementServiceClient()
    response = client.get_public_key(key_name)
    key_txt = response.pem.encode('ascii')
    public_key = serialization.load_pem_public_key(key_txt, default_backend())

    # get the digest of the message
    digest_bytes = hashlib.sha256(message).digest()

    try:
        # Attempt verification
        public_key.verify(signature,
                          digest_bytes,
                          ec.ECDSA(utils.Prehashed(hashes.SHA256())))
        # No errors were thrown. Verification was successful
        return True
    except InvalidSignature:
        return False
# [END kms_verify_signature_ec]
