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

import base64
import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, utils


# [START kms_get_asymmetric_public]
def getAsymmetricPublicKey(client, key_path):
    """Retrieves the public key from a saved asymmetric key pair on Cloud KMS
    """
    request = client.projects() \
                    .locations() \
                    .keyRings() \
                    .cryptoKeys() \
                    .cryptoKeyVersions() \
                    .getPublicKey(name=key_path)
    response = request.execute()
    key_txt = response['pem'].encode('ascii')
    key = serialization.load_pem_public_key(key_txt, default_backend())
    return key
# [END kms_get_asymmetric_public]


# [START kms_decrypt_rsa]
def decryptRSA(ciphertext, client, key_path):
    """Decrypt a given ciphertext using an RSA private key stored on Cloud KMS
    """
    request = client.projects() \
                    .locations() \
                    .keyRings() \
                    .cryptoKeys() \
                    .cryptoKeyVersions() \
                    .asymmetricDecrypt(name=key_path,
                                       body={'ciphertext': ciphertext})
    response = request.execute()
    plaintext = base64.b64decode(response['plaintext']).decode('utf-8')
    return plaintext
# [END kms_decrypt_rsa]


# [START kms_encrypt_rsa]
def encryptRSA(message, client, key_path):
    """Encrypt message locally using an RSA public key retrieved from Cloud KMS
    """
    public_key = getAsymmetricPublicKey(client, key_path)
    pad = padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                       algorithm=hashes.SHA256(),
                       label=None)
    ciphertext = public_key.encrypt(message.encode('ascii'), pad)
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    return ciphertext
# [END kms_encrypt_rsa]


# [START kms_sign_asymmetric]
def signAsymmetric(message, client, key_path):
    """Create a signature for a message using a private key stored on Cloud KMS
    """
    digest_bytes = hashlib.sha256(message.encode('ascii')).digest()
    digest64 = base64.b64encode(digest_bytes)

    digest_JSON = {'sha256': digest64.decode('utf-8')}
    request = client.projects() \
                    .locations() \
                    .keyRings() \
                    .cryptoKeys() \
                    .cryptoKeyVersions() \
                    .asymmetricSign(name=key_path,
                                    body={'digest': digest_JSON})
    response = request.execute()
    return response.get('signature', None)
# [END kms_sign_asymmetric]


# [START kms_verify_signature_rsa]
def verifySignatureRSA(signature, message, client, key_path):
    """Verify the validity of an 'RSA_SIGN_PSS_2048_SHA256' signature
    for the specified plaintext message
    """
    public_key = getAsymmetricPublicKey(client, key_path)

    digest_bytes = hashlib.sha256(message.encode('ascii')).digest()
    sig_bytes = base64.b64decode(signature)

    try:
        # Attempt verification
        public_key.verify(sig_bytes,
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
def verifySignatureEC(signature, message, client, key_path):
    """Verify the validity of an 'EC_SIGN_P224_SHA256' signature
    for the specified plaintext message
    """
    public_key = getAsymmetricPublicKey(client, key_path)

    digest_bytes = hashlib.sha256(message.encode('ascii')).digest()
    sig_bytes = base64.b64decode(signature)

    try:
        # Attempt verification
        public_key.verify(sig_bytes,
                          digest_bytes,
                          ec.ECDSA(utils.Prehashed(hashes.SHA256())))
        # No errors were thrown. Verification was successful
        return True
    except InvalidSignature:
        return False
# [END kms_verify_signature_ec]
