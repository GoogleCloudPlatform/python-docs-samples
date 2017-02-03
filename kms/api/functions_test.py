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


# Your Google Cloud Platform Key Location
LOCATION = 'global'

# Your Google Cloud Platform KeyRing name
KEYRING = 'sample-keyring-28'

# Your Google Cloud Platform CryptoKey name
CRYPTOKEY = 'sample-key-28'

# Your Google Cloud Platform CryptoKeyVersion name
VERSION = 1

# A member to add to our IAM policy
MEMBER = 'user:ryanmats@google.com'

# The role we want our new member to have for our IAM policy
ROLE = 'roles/owner'


def test_create_keyring(capsys, cloud_config):
    functions.create_keyring(cloud_config.project, LOCATION, KEYRING)
    out, _ = capsys.readouterr()
    expected = 'Created KeyRing projects/{}/locations/{}/keyRings/{}.'.format(
        cloud_config.project, LOCATION, KEYRING)
    assert expected in out


def test_create_cryptokey(capsys, cloud_config):
    functions.create_cryptokey(
        cloud_config.project, LOCATION, KEYRING, CRYPTOKEY)
    out, _ = capsys.readouterr()
    expected = 'Created CryptoKey projects/{}/'.format(cloud_config.project)
    expected += 'locations/{}/keyRings/{}/'.format(LOCATION, KEYRING)
    expected += 'cryptoKeys/{}.'.format(CRYPTOKEY)
    assert expected in out


def test_encrypt_decrypt(capsys, cloud_config, tmpdir):
    # Write to a plaintext file.
    tmpdir.join("in.txt").write('SampleText')

    # Construct temporary file names.
    plaintext_file_name = str(tmpdir.join("in.txt"))
    encrypted_file_name = str(tmpdir.join("out.txt"))
    decrypted_file_name = str(tmpdir.join("out2.txt"))

    # Encrypt text and then decrypt it.
    functions.encrypt(
        cloud_config.project, LOCATION, KEYRING, CRYPTOKEY,
        plaintext_file_name, encrypted_file_name)
    functions.decrypt(
        cloud_config.project, LOCATION, KEYRING, CRYPTOKEY,
        encrypted_file_name, decrypted_file_name)

    # Make sure the decrypted text matches the original text.
    decrypted_text = open(decrypted_file_name).read()
    assert decrypted_text == 'SampleText'

    # Make sure other output is as expected.
    out, _ = capsys.readouterr()
    assert 'Saved encrypted text to {}.'.format(encrypted_file_name) in out
    assert 'Saved decrypted text to {}.'.format(decrypted_file_name) in out


def test_encrypt_decrypt_cli(capsys, cloud_config, tmpdir):
    # Write to a plaintext file.
    tmpdir.join("in.txt").write('SampleText')

    # Construct temporary file names.
    plaintext_file_name = str(tmpdir.join("in.txt"))
    encrypted_file_name = str(tmpdir.join("out.txt"))
    decrypted_file_name = str(tmpdir.join("out2.txt"))

    # Encrypt text and then decrypt it.
    project_id = cloud_config.project
    encrypt_output = subprocess.check_output(
        "python functions.py encrypt {} {} {} {} {} {}".format(
            project_id, LOCATION, KEYRING, CRYPTOKEY, plaintext_file_name,
            encrypted_file_name),
        shell=True)
    decrypt_output = subprocess.check_output(
        "python functions.py decrypt {} {} {} {} {} {}".format(
            project_id, LOCATION, KEYRING, CRYPTOKEY, encrypted_file_name,
            decrypted_file_name),
        shell=True)

    # Make sure the decrypted text matches the original text.
    decrypted_text = open(decrypted_file_name).read()
    assert decrypted_text == 'SampleText'

    # Make sure other output is as expected.
    expected_encrypt_out = 'Saved encrypted text to {}.'.format(
        encrypted_file_name)
    assert expected_encrypt_out in encrypt_output.decode('utf-8')
    expected_decrypt_out = 'Saved decrypted text to {}.'.format(
        decrypted_file_name)
    assert expected_decrypt_out in decrypt_output.decode('utf-8')


def test_disable_cryptokey_version(capsys, cloud_config):
    functions.disable_cryptokey_version(
        cloud_config.project, LOCATION, KEYRING, CRYPTOKEY, VERSION)
    out, _ = capsys.readouterr()
    expected = 'CryptoKeyVersion projects/{}/'.format(cloud_config.project)
    expected += 'locations/{}/keyRings/{}/'.format(LOCATION, KEYRING)
    expected += 'cryptoKeys/{}/cryptoKeyVersions/{}'.format(CRYPTOKEY, VERSION)
    expected += '\'s state has been set to {}.'.format('DISABLED')
    assert expected in out


def test_destroy_cryptokey_version(capsys, cloud_config):
    functions.destroy_cryptokey_version(
        cloud_config.project, LOCATION, KEYRING, CRYPTOKEY, VERSION)
    out, _ = capsys.readouterr()
    expected = 'CryptoKeyVersion projects/{}/'.format(cloud_config.project)
    expected += 'locations/{}/keyRings/{}/'.format(LOCATION, KEYRING)
    expected += 'cryptoKeys/{}/cryptoKeyVersions/{}'.format(CRYPTOKEY, VERSION)
    expected += '\'s state has been set to {}.'.format('DESTROY_SCHEDULED')
    assert expected in out


def test_add_member_to_cryptokey_policy(capsys, cloud_config):
    functions.add_member_to_cryptokey_policy(
        cloud_config.project, LOCATION, KEYRING, CRYPTOKEY, MEMBER, ROLE)
    out, _ = capsys.readouterr()
    expected = 'Member {} added with role {} to policy '.format(MEMBER, ROLE)
    expected += 'for CryptoKey {} in KeyRing {}'.format(CRYPTOKEY, KEYRING)
    assert expected in out

    # Creates an API client for the KMS API.
    kms_client = discovery.build('cloudkms', 'v1beta1')

    # The resource name of the CryptoKey.
    parent = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        cloud_config.project, LOCATION, KEYRING, CRYPTOKEY)

    # Get the current IAM policy and verify that the new member has been added
    # with the correct role.
    cryptokeys = kms_client.projects().locations().keyRings().cryptoKeys()
    policy_request = cryptokeys.getIamPolicy(resource=parent)
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


def test_get_keyring_policy(capsys, cloud_config):
    project_id = cloud_config.project
    functions.get_keyring_policy(project_id, LOCATION, KEYRING)
    out, _ = capsys.readouterr()
    expected_roles_exist = 'Printing IAM policy for resource projects/'
    expected_roles_exist += '{}/locations/{}/'.format(project_id, LOCATION)
    expected_roles_exist += 'keyRings/{}:'.format(KEYRING)
    expected_no_roles = 'No roles found for resource projects/'
    expected_no_roles += '{}/locations/{}/'.format(project_id, LOCATION)
    expected_no_roles += 'keyRings/{}.'.format(KEYRING)
    assert (expected_roles_exist in out) or (expected_no_roles in out)
