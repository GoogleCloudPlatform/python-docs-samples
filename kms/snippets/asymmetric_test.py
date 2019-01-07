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
# limitations under the License.

from os import environ
from time import sleep

import asymmetric

from cryptography.hazmat.backends.openssl.ec import _EllipticCurvePublicKey
from cryptography.hazmat.backends.openssl.rsa import _RSAPublicKey

from google.api_core.exceptions import GoogleAPICallError
from google.cloud.kms_v1 import enums

from snippets import create_key_ring

from snippets_test import create_key_helper


def setup_module(module):
    """
    Set up keys in project if needed
    """
    t = TestKMSAsymmetric()
    try:
        # create keyring
        create_key_ring(t.project_id, t.location, t.keyring_id)
    except GoogleAPICallError:
        # keyring already exists
        pass
    s1 = create_key_helper(t.rsaDecryptId,
                           enums.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_DECRYPT,
                           enums.CryptoKeyVersion.CryptoKeyVersionAlgorithm.
                           RSA_DECRYPT_OAEP_2048_SHA256,
                           t)
    s2 = create_key_helper(t.rsaSignId,
                           enums.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_SIGN,
                           enums.CryptoKeyVersion.CryptoKeyVersionAlgorithm.
                           RSA_SIGN_PSS_2048_SHA256,
                           t)
    s3 = create_key_helper(t.ecSignId,
                           enums.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_SIGN,
                           enums.CryptoKeyVersion.CryptoKeyVersionAlgorithm.
                           EC_SIGN_P256_SHA256,
                           t)

    if s1 or s2 or s3:
        # leave time for keys to initialize
        sleep(20)


class TestKMSAsymmetric:
    project_id = environ['GCLOUD_PROJECT']
    keyring_id = 'kms-samples'
    location = 'global'
    parent = 'projects/{}/locations/{}'.format(project_id, location)

    rsaSignId = 'rsa-sign'
    rsaDecryptId = 'rsa-decrypt'
    ecSignId = 'ec-sign'

    rsaSign = '{}/keyRings/{}/cryptoKeys/{}/cryptoKeyVersions/1' \
              .format(parent, keyring_id, rsaSignId)
    rsaDecrypt = '{}/keyRings/{}/cryptoKeys/{}/cryptoKeyVersions/1' \
                 .format(parent, keyring_id, rsaDecryptId)
    ecSign = '{}/keyRings/{}/cryptoKeys/{}/cryptoKeyVersions/1' \
             .format(parent, keyring_id, ecSignId)

    message = 'test message 123'
    message_bytes = message.encode('utf-8')

    def test_get_public_key(self):
        rsa_key = asymmetric.get_asymmetric_public_key(self.rsaDecrypt)
        assert isinstance(rsa_key, _RSAPublicKey), 'expected RSA key'
        rsa_key = asymmetric.get_asymmetric_public_key(self.rsaSign)
        assert isinstance(rsa_key, _RSAPublicKey), 'expected RSA key'
        ec_key = asymmetric.get_asymmetric_public_key(self.ecSign)
        assert isinstance(ec_key, _EllipticCurvePublicKey), 'expected EC key'

    def test_rsa_encrypt_decrypt(self):
        ciphertext = asymmetric.encrypt_rsa(self.message_bytes,
                                            self.rsaDecrypt)
        # signature should be 256 bytes for RSA 2048
        assert len(ciphertext) == 256, \
            'ciphertext should be 256 chars; got {}'.format(len(ciphertext))
        plaintext_bytes = asymmetric.decrypt_rsa(ciphertext,
                                                 self.rsaDecrypt)
        assert plaintext_bytes == self.message_bytes
        plaintext = plaintext_bytes.decode('utf-8')
        assert plaintext == self.message

    def test_rsa_sign_verify(self):
        sig = asymmetric.sign_asymmetric(self.message_bytes,
                                         self.rsaSign)
        # signature should be 256 bytes for RSA 2048
        assert len(sig) == 256, \
            'sig should be 256 chars; got {}'.format(len(sig))
        success = asymmetric.verify_signature_rsa(sig,
                                                  self.message_bytes,
                                                  self.rsaSign)
        assert success is True, 'RSA verification failed'
        changed_bytes = self.message_bytes + b'.'
        success = asymmetric.verify_signature_rsa(sig,
                                                  changed_bytes,
                                                  self.rsaSign)
        assert success is False, 'verify should fail with modified message'

    def test_ec_sign_verify(self):
        sig = asymmetric.sign_asymmetric(self.message_bytes,
                                         self.ecSign)
        assert len(sig) > 50 and len(sig) < 300, \
            'sig outside expected length range'
        success = asymmetric.verify_signature_ec(sig,
                                                 self.message_bytes,
                                                 self.ecSign)
        assert success is True, 'EC verification failed'
        changed_bytes = self.message_bytes + b'.'
        success = asymmetric.verify_signature_ec(sig,
                                                 changed_bytes,
                                                 self.ecSign)
        assert success is False, 'verify should fail with modified message'
