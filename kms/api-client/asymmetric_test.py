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

from cryptography.hazmat.backends.openssl.ec import _EllipticCurvePublicKey
from cryptography.hazmat.backends.openssl.rsa import _RSAPublicKey
from googleapiclient import discovery
from googleapiclient.errors import HttpError
import sample


def create_key_helper(key_id, key_path, purpose, algorithm, t):
    try:
        t.client.projects() \
                .locations() \
                .keyRings() \
                .cryptoKeys() \
                .create(parent='{}/keyRings/{}'.format(t.parent, t.keyring),
                        body={'purpose': purpose,
                              'versionTemplate': {
                                  'algorithm': algorithm
                                  }
                              },
                        cryptoKeyId=key_id) \
                .execute()
        return True
    except HttpError:
        # key already exists
        return False


def setup_module(module):
    """
    Set up keys in project if needed
    """
    t = TestKMSSamples()
    try:
        # create keyring
        t.client.projects() \
                .locations() \
                .keyRings() \
                .create(parent=t.parent, body={}, keyRingId=t.keyring) \
                .execute()
    except HttpError:
        # keyring already exists
        pass
    s1 = create_key_helper(t.rsaDecryptId, t.rsaDecrypt, 'ASYMMETRIC_DECRYPT',
                           'RSA_DECRYPT_OAEP_2048_SHA256', t)
    s2 = create_key_helper(t.rsaSignId, t.rsaSign, 'ASYMMETRIC_SIGN',
                           'RSA_SIGN_PSS_2048_SHA256', t)
    s3 = create_key_helper(t.ecSignId, t.ecSign, 'ASYMMETRIC_SIGN',
                           'EC_SIGN_P256_SHA256', t)
    if s1 or s2 or s3:
        # leave time for keys to initialize
        sleep(20)


class TestKMSSamples:

    project_id = environ['GCLOUD_PROJECT']
    keyring = 'kms-asymmetric-samples4'
    parent = 'projects/{}/locations/global'.format(project_id)

    rsaSignId = 'rsa-sign'
    rsaDecryptId = 'rsa-decrypt'
    ecSignId = 'ec-sign'

    rsaSign = '{}/keyRings/{}/cryptoKeys/{}/cryptoKeyVersions/1' \
              .format(parent, keyring, rsaSignId)
    rsaDecrypt = '{}/keyRings/{}/cryptoKeys/{}/cryptoKeyVersions/1' \
                 .format(parent, keyring, rsaDecryptId)
    ecSign = '{}/keyRings/{}/cryptoKeys/{}/cryptoKeyVersions/1' \
             .format(parent, keyring, ecSignId)

    message = 'test message 123'

    client = discovery.build('cloudkms', 'v1')

    def test_get_public_key(self):
        rsa_key = sample.getAsymmetricPublicKey(self.client, self.rsaDecrypt)
        assert isinstance(rsa_key, _RSAPublicKey), 'expected RSA key'
        ec_key = sample.getAsymmetricPublicKey(self.client, self.ecSign)
        assert isinstance(ec_key, _EllipticCurvePublicKey), 'expected EC key'

    def test_rsa_encrypt_decrypt(self):
        ciphertext = sample.encryptRSA(self.message,
                                       self.client,
                                       self.rsaDecrypt)
        # ciphertext should be 344 characters with base64 and RSA 2048
        assert len(ciphertext) == 344, \
            'ciphertext should be 344 chars; got {}'.format(len(ciphertext))
        assert ciphertext[-2:] == '==', 'cipher text should end with =='
        plaintext = sample.decryptRSA(ciphertext, self.client, self.rsaDecrypt)
        assert plaintext == self.message

    def test_rsa_sign_verify(self):
        sig = sample.signAsymmetric(self.message, self.client, self.rsaSign)
        # ciphertext should be 344 characters with base64 and RSA 2048
        assert len(sig) == 344, \
            'sig should be 344 chars; got {}'.format(len(sig))
        assert sig[-2:] == '==', 'sig should end with =='
        success = sample.verifySignatureRSA(sig,
                                            self.message,
                                            self.client,
                                            self.rsaSign)
        assert success is True, 'RSA verification failed'
        success = sample.verifySignatureRSA(sig,
                                            self.message+'.',
                                            self.client,
                                            self.rsaSign)
        assert success is False, 'verify should fail with modified message'

    def test_ec_sign_verify(self):
        sig = sample.signAsymmetric(self.message, self.client, self.ecSign)
        assert len(sig) > 50 and len(sig) < 300, \
            'sig outside expected length range'
        success = sample.verifySignatureEC(sig,
                                           self.message,
                                           self.client,
                                           self.ecSign)
        assert success is True, 'EC verification failed'
        success = sample.verifySignatureEC(sig,
                                           self.message+'.',
                                           self.client,
                                           self.ecSign)
        assert success is False, 'verify should fail with modified message'
