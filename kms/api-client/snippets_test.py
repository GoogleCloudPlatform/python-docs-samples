#!/usr/bin/env python

# Copyright 2017 Google, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

import os
import random
import string

import googleapiclient.discovery

import snippets

PROJECT = os.environ['GCLOUD_PROJECT']

# Your Google Cloud Platform Key Location
LOCATION = 'global'

# Your Google Cloud Platform KeyRing name
KEY_RING = ''.join(
    random.choice(string.ascii_lowercase + string.digits) for _ in range(12))

# Your Google Cloud Platform CryptoKey name
CRYPTO_KEY = ''.join(
    random.choice(string.ascii_lowercase + string.digits) for _ in range(12))

# Your Google Cloud Platform CryptoKeyVersion name
VERSION = 1

# A member to add to our IAM policy
MEMBER = 'user:ryanmats@google.com'

# The role we want our new member to have for our IAM policy
ROLE = 'roles/owner'


def test_create_key_ring(capsys):
    snippets.create_key_ring(PROJECT, LOCATION, KEY_RING)
    out, _ = capsys.readouterr()
    expected = 'Created KeyRing projects/{}/locations/{}/keyRings/{}.'.format(
        PROJECT, LOCATION, KEY_RING)
    assert expected in out


def test_create_crypto_key(capsys):
    snippets.create_crypto_key(
        PROJECT, LOCATION, KEY_RING, CRYPTO_KEY)
    out, _ = capsys.readouterr()
    expected = (
        'Created CryptoKey projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}.'
        .format(PROJECT, LOCATION, KEY_RING, CRYPTO_KEY))
    assert expected in out


def test_encrypt_decrypt(capsys, tmpdir):
    # Write to a plaintext file.
    tmpdir.join('in.txt').write('SampleText')

    # Construct temporary files.
    plaintext_file = tmpdir.join('in.txt')
    encrypted_file = tmpdir.join('out.txt')
    decrypted_file = tmpdir.join('out2.txt')

    # Encrypt text and then decrypt it.
    snippets.encrypt(
        PROJECT, LOCATION, KEY_RING, CRYPTO_KEY,
        str(plaintext_file), str(encrypted_file))
    snippets.decrypt(
        PROJECT, LOCATION, KEY_RING, CRYPTO_KEY,
        str(encrypted_file), str(decrypted_file))

    # Make sure the decrypted text matches the original text.
    decrypted_text = decrypted_file.read()
    assert decrypted_text == 'SampleText'

    # Make sure other output is as expected.
    out, _ = capsys.readouterr()
    assert 'Saved ciphertext to {}.'.format(str(encrypted_file)) in out
    assert 'Saved plaintext to {}.'.format(str(decrypted_file)) in out


def test_disable_crypto_key_version(capsys):
    snippets.disable_crypto_key_version(
        PROJECT, LOCATION, KEY_RING, CRYPTO_KEY, VERSION)
    out, _ = capsys.readouterr()
    expected = (
        'CryptoKeyVersion projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}/'
        'cryptoKeyVersions/{}\'s state has been set to {}.'
        .format(
            PROJECT, LOCATION, KEY_RING, CRYPTO_KEY, VERSION,
            'DISABLED'))
    assert expected in out


def test_destroy_crypto_key_version(capsys):
    snippets.destroy_crypto_key_version(
        PROJECT, LOCATION, KEY_RING, CRYPTO_KEY, VERSION)
    out, _ = capsys.readouterr()
    expected = (
        'CryptoKeyVersion projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}/'
        'cryptoKeyVersions/{}\'s state has been set to {}.'
        .format(
            PROJECT, LOCATION, KEY_RING, CRYPTO_KEY, VERSION,
            'DESTROY_SCHEDULED'))
    assert expected in out


def test_add_member_to_crypto_key_policy(capsys):
    snippets.add_member_to_crypto_key_policy(
        PROJECT, LOCATION, KEY_RING, CRYPTO_KEY, MEMBER, ROLE)
    out, _ = capsys.readouterr()
    expected = (
        'Member {} added with role {} to policy for CryptoKey {} in KeyRing {}'
        .format(MEMBER, ROLE, CRYPTO_KEY, KEY_RING))
    assert expected in out

    kms_client = googleapiclient.discovery.build('cloudkms', 'v1')
    parent = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        PROJECT, LOCATION, KEY_RING, CRYPTO_KEY)
    crypto_keys = kms_client.projects().locations().keyRings().cryptoKeys()
    policy_request = crypto_keys.getIamPolicy(resource=parent)
    policy_response = policy_request.execute()
    assert 'bindings' in policy_response.keys()
    bindings = policy_response['bindings']
    found_member_role_pair = False
    for binding in bindings:
        if binding['role'] == ROLE:
            for user in binding['members']:
                if user == MEMBER:
                    found_member_role_pair = True
    assert found_member_role_pair


def test_get_key_ring_policy(capsys):
    snippets.get_key_ring_policy(PROJECT, LOCATION, KEY_RING)
    out, _ = capsys.readouterr()
    expected_roles_exist = (
        'Printing IAM policy for resource projects/{}/locations/{}/keyRings/{}'
        ':'.format(PROJECT, LOCATION, KEY_RING))
    expected_no_roles = (
        'No roles found for resource projects/{}/locations/{}/keyRings/{}.'
        .format(PROJECT, LOCATION, KEY_RING))
    assert (expected_roles_exist in out) or (expected_no_roles in out)
