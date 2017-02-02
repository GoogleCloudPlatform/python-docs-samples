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

import subprocess

from googleapiclient import discovery

import functions


# Your Google Cloud Platform project ID
PROJECT_ID = 'your-project-id'

# Your Google Cloud Platform Key Location
LOCATION = 'global'

# Your Google Cloud Platform KeyRing name
KEYRING = 'sample-keyring-4'

# Your Google Cloud Platform CryptoKey name
CRYPTOKEY = 'sample-key-4'

# An infile for text to be encrypted
INFILE = 'infile.txt'

# An outfile for text that has been encrypted
OUTFILE = 'outfile.txt'

# An outfile for text that has been decrypted
DECRYPTEDFILE = 'outfile2.txt'

# Your Google Cloud Platform CryptoKeyVersion name
VERSION = 1

# A member to add to our IAM policy
MEMBER = 'user:ryanmats@google.com'

# The role we want our new member to have for our IAM policy
ROLE = 'roles/owner'


def test_create_keyring(capsys):
    functions.create_keyring(PROJECT_ID, LOCATION, KEYRING)
    out, _ = capsys.readouterr()
    expected = 'Created KeyRing projects/{}/locations/{}/keyRings/{}.'.format(
        PROJECT_ID, LOCATION, KEYRING)
    assert expected in out


def test_create_cryptokey(capsys):
    functions.create_cryptokey(PROJECT_ID, LOCATION, KEYRING, CRYPTOKEY)
    out, _ = capsys.readouterr()
    expected = 'Created CryptoKey projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}.'.format(PROJECT_ID, LOCATION, KEYRING, CRYPTOKEY)
    assert expected in out


def test_encrypt_decrypt(capsys):
    # Read text from input file.
    i = open(INFILE, 'r')
    text = i.read()
    i.close()

    # Encrypt text and then decrypt it.
    functions.encrypt(
        PROJECT_ID, LOCATION, KEYRING, CRYPTOKEY, INFILE, OUTFILE)
    functions.decrypt(
        PROJECT_ID, LOCATION, KEYRING, CRYPTOKEY, OUTFILE, DECRYPTEDFILE)

    # Make sure the decrypted text matches the original text
    o = open(DECRYPTEDFILE, 'r')
    decrypted_text = o.read()
    assert decrypted_text == text
    o.close()

    # Make sure other output is as expected.
    out, _ = capsys.readouterr()
    assert 'Saved encrypted text to {}.'.format(OUTFILE) in out
    assert 'Saved decrypted text to {}.'.format(DECRYPTEDFILE) in out


def test_encrypt_decrypt_cli(capsys):
    # Read text from input file.
    i = open(INFILE, 'r')
    text = i.read()
    i.close()

    # Encrypt text and then decrypt it.
    encrypt_output = subprocess.check_output(
        "python functions.py encrypt {} {} {} {} {} {}".format(
            PROJECT_ID, LOCATION, KEYRING, CRYPTOKEY, INFILE, OUTFILE),
        shell=True)
    decrypt_output = subprocess.check_output(
        "python functions.py decrypt {} {} {} {} {} {}".format(
            PROJECT_ID, LOCATION, KEYRING, CRYPTOKEY, OUTFILE, DECRYPTEDFILE),
        shell=True)

    # Make sure the decrypted text matches the original text
    o = open(DECRYPTEDFILE, 'r')
    decrypted_text = o.read()
    assert decrypted_text == text
    o.close()

    # Make sure other output is as expected.
    expected_encrypt_out = 'Saved encrypted text to {}.'.format(OUTFILE)
    assert expected_encrypt_out in encrypt_output
    expected_decrypt_out = 'Saved decrypted text to {}.'.format(DECRYPTEDFILE)
    assert expected_decrypt_out in decrypt_output


def test_disable_cryptokey_version(capsys):
    functions.disable_cryptokey_version(
        PROJECT_ID, LOCATION, KEYRING, CRYPTOKEY, VERSION)
    out, _ = capsys.readouterr()
    expected = 'CryptoKeyVersion projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}/cryptoKeyVersions/{}\'s state has been set to {}.'.format(PROJECT_ID, LOCATION, KEYRING, CRYPTOKEY, VERSION, 'DISABLED')
    assert expected in out


def test_destroy_cryptokey_version(capsys):
    functions.destroy_cryptokey_version(
        PROJECT_ID, LOCATION, KEYRING, CRYPTOKEY, VERSION)
    out, _ = capsys.readouterr()
    expected = 'CryptoKeyVersion projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}/cryptoKeyVersions/{}\'s state has been set to {}.'.format(PROJECT_ID, LOCATION, KEYRING, CRYPTOKEY, VERSION, 'DESTROY_SCHEDULED')
    assert expected in out


def test_add_member_to_cryptokey_policy(capsys):
    functions.add_member_to_cryptokey_policy(
        PROJECT_ID, LOCATION, KEYRING, CRYPTOKEY, MEMBER, ROLE)
    out, _ = capsys.readouterr()
    expected = 'Member {} added with role {} to policy for CryptoKey {} in KeyRing {}'.format(MEMBER, ROLE, CRYPTOKEY, KEYRING)
    assert expected in out

    # Creates an API client for the KMS API.
    kms_client = discovery.build('cloudkms', 'v1beta1')

    # The resource name of the CryptoKey.
    parent = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        PROJECT_ID, LOCATION, KEYRING, CRYPTOKEY)

    # Get the current IAM policy and verify that the new member has been added
    # with the correct role.
    policy_request = kms_client.projects().locations().keyRings().cryptoKeys().getIamPolicy(resource=parent)
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


def test_get_keyring_policy(capsys):
    functions.get_keyring_policy(PROJECT_ID, LOCATION, KEYRING)
    out, _ = capsys.readouterr()
    expected_roles_exist = 'Printing IAM policy for resource projects/{}/locations/{}/keyRings/{}:'.format(PROJECT_ID, LOCATION, KEYRING)
    expected_no_roles = 'No roles found for resource projects/{}/locations/{}/keyRings/{}.'.format(PROJECT_ID, LOCATION, KEYRING)
    assert (expected_roles_exist in out) or (expected_no_roles in out)
