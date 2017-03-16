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

import argparse
import base64
import io

import googleapiclient.discovery


# [START kms_create_keyring]
def create_keyring(project_id, location, keyring):
    """Creates a KeyRing in the given location (e.g. global)."""

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build('cloudkms', 'v1')

    # The resource name of the location associated with the KeyRing.
    parent = 'projects/{}/locations/{}'.format(project_id, location)

    # Create KeyRing
    request = kms_client.projects().locations().keyRings().create(
        parent=parent, body={}, keyRingId=keyring)
    response = request.execute()

    print('Created KeyRing {}.'.format(response['name']))
# [END kms_create_keyring]


# [START kms_create_cryptokey]
def create_cryptokey(project_id, location, keyring, cryptokey):
    """Creates a CryptoKey within a KeyRing in the given location."""

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build('cloudkms', 'v1')

    # The resource name of the KeyRing associated with the CryptoKey.
    parent = 'projects/{}/locations/{}/keyRings/{}'.format(
        project_id, location, keyring)

    # Create a CryptoKey for the given KeyRing.
    request = kms_client.projects().locations().keyRings().cryptoKeys().create(
        parent=parent, body={'purpose': 'ENCRYPT_DECRYPT'},
        cryptoKeyId=cryptokey)
    response = request.execute()

    print('Created CryptoKey {}.'.format(response['name']))
# [END kms_create_cryptokey]


# [START kms_encrypt]
def encrypt(project_id, location, keyring, cryptokey, plaintext_file_name,
            encrypted_file_name):
    """Encrypts data from a plaintext_file_name using the provided CryptoKey
    and saves it to an encrypted_file_name so it can only be recovered with a
    call to decrypt."""

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build('cloudkms', 'v1')

    # The resource name of the CryptoKey.
    name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        project_id, location, keyring, cryptokey)

    # Read text from the input file.
    with io.open(plaintext_file_name, 'rb') as plaintext_file:
        plaintext = plaintext_file.read()
    encoded_text = base64.b64encode(plaintext)

    # Use the KMS API to encrypt the text.
    cryptokeys = kms_client.projects().locations().keyRings().cryptoKeys()
    request = cryptokeys.encrypt(
        name=name, body={'plaintext': encoded_text.decode('utf-8')})
    response = request.execute()

    # Write the encrypted text to a file.
    with io.open(encrypted_file_name, 'wb') as encrypted_file:
        encrypted_file.write(response['ciphertext'].encode('utf-8'))

    print('Saved encrypted text to {}.'.format(encrypted_file_name))
# [END kms_encrypt]


# [START kms_decrypt]
def decrypt(project_id, location, keyring, cryptokey, encrypted_file_name,
            decrypted_file_name):
    """Decrypts data from encrypted_file_name that was previously encrypted
    using the CryptoKey with a call to encrypt. Outputs decrypted data to
    decrpyted_file_name."""

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build('cloudkms', 'v1')

    # The resource name of the CryptoKey.
    name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        project_id, location, keyring, cryptokey)

    # Read cipher text from the input file.
    with io.open(encrypted_file_name, 'rb') as encrypted_file:
        cipher_text = encrypted_file.read()

    # Use the KMS API to decrypt the text.
    cryptokeys = kms_client.projects().locations().keyRings().cryptoKeys()
    request = cryptokeys.decrypt(
        name=name, body={'ciphertext': cipher_text.decode('utf-8')})
    response = request.execute()

    # Write the plain text to a file.
    with io.open(decrypted_file_name, 'wb') as decrypted_file:
        plaintext_encoded = response['plaintext']
        plaintext_decoded = base64.b64decode(plaintext_encoded)
        decrypted_file.write(plaintext_decoded)

    print('Saved decrypted text to {}.'.format(decrypted_file_name))
# [END kms_decrypt]


# [START kms_disable_cryptokey_version]
def disable_cryptokey_version(project_id, location, keyring, cryptokey,
                              version):
    """Disables a CryptoKeyVersion associated with a given CryptoKey and
    KeyRing."""

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build('cloudkms', 'v1')

    # Construct the resource name of the CryptoKeyVersion.
    name = (
        'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}/'
        'cryptoKeyVersions/{}'
        .format(project_id, location, keyring, cryptokey, version))

    # Use the KMS API to disable the CryptoKeyVersion.
    cryptokeys = kms_client.projects().locations().keyRings().cryptoKeys()
    request = cryptokeys.cryptoKeyVersions().patch(
        name=name, body={'state': 'DISABLED'}, updateMask='state')
    response = request.execute()

    print('CryptoKeyVersion {}\'s state has been set to {}.'.format(
        name, response['state']))
# [END kms_disable_cryptokey_version]


# [START kms_destroy_cryptokey_version]
def destroy_cryptokey_version(
        project_id, location, keyring, cryptokey, version):
    """Schedules a CryptoKeyVersion associated with a given CryptoKey and
    KeyRing for destruction 24 hours in the future."""

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build('cloudkms', 'v1')

    # Construct the resource name of the CryptoKeyVersion.
    name = (
        'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}/'
        'cryptoKeyVersions/{}'
        .format(project_id, location, keyring, cryptokey, version))

    # Use the KMS API to schedule the CryptoKeyVersion for destruction.
    cryptokeys = kms_client.projects().locations().keyRings().cryptoKeys()
    request = cryptokeys.cryptoKeyVersions().destroy(name=name, body={})
    response = request.execute()

    print('CryptoKeyVersion {}\'s state has been set to {}.'.format(
        name, response['state']))
# [END kms_destroy_cryptokey_version]


# [START kms_add_member_to_cryptokey_policy]
def add_member_to_cryptokey_policy(
        project_id, location, keyring, cryptokey, member, role):
    """Adds a member with a given role to the Identity and Access Management
    (IAM) policy for a given CryptoKey associated with a KeyRing."""

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build('cloudkms', 'v1')

    # The resource name of the CryptoKey.
    parent = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        project_id, location, keyring, cryptokey)

    # Get the current IAM policy and add the new member to it.
    cryptokeys = kms_client.projects().locations().keyRings().cryptoKeys()
    policy_request = cryptokeys.getIamPolicy(resource=parent)
    policy_response = policy_request.execute()
    bindings = []
    if 'bindings' in policy_response.keys():
        bindings = policy_response['bindings']
    members = []
    members.append(member)
    new_binding = dict()
    new_binding['role'] = role
    new_binding['members'] = members
    bindings.append(new_binding)
    policy_response['bindings'] = bindings

    # Set the new IAM Policy.
    cryptokeys = kms_client.projects().locations().keyRings().cryptoKeys()
    request = cryptokeys.setIamPolicy(
        resource=parent, body={'policy': policy_response})
    request.execute()

    print_msg = (
        'Member {} added with role {} to policy for CryptoKey {} in KeyRing {}'
        .format(member, role, cryptokey, keyring))
    print(print_msg)
# [END kms_add_member_to_cryptokey_policy]


# [START kms_get_keyring_policy]
def get_keyring_policy(project_id, location, keyring):
    """Gets the Identity and Access Management (IAM) policy for a given KeyRing
    and prints out roles and the members assigned to those roles."""

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build('cloudkms', 'v1')

    # The resource name of the KeyRing.
    parent = 'projects/{}/locations/{}/keyRings/{}'.format(
        project_id, location, keyring)

    # Get the current IAM policy.
    request = kms_client.projects().locations().keyRings().getIamPolicy(
        resource=parent)
    response = request.execute()

    if 'bindings' in response.keys():
        print('Printing IAM policy for resource {}:'.format(parent))
        for binding in response['bindings']:
            print('')
            print('Role: {}'.format(binding['role']))
            print('Members:')
            for member in binding['members']:
                print(member)
        print('')
    else:
        print('No roles found for resource {}.'.format(parent))
# [END kms_get_keyring_policy]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    create_keyring_parser = subparsers.add_parser('create_keyring')
    create_keyring_parser.add_argument('project_id')
    create_keyring_parser.add_argument('location')
    create_keyring_parser.add_argument('keyring')

    create_cryptokey_parser = subparsers.add_parser('create_cryptokey')
    create_cryptokey_parser.add_argument('project_id')
    create_cryptokey_parser.add_argument('location')
    create_cryptokey_parser.add_argument('keyring')
    create_cryptokey_parser.add_argument('cryptokey')

    encrypt_parser = subparsers.add_parser('encrypt')
    encrypt_parser.add_argument('project_id')
    encrypt_parser.add_argument('location')
    encrypt_parser.add_argument('keyring')
    encrypt_parser.add_argument('cryptokey')
    encrypt_parser.add_argument('infile')
    encrypt_parser.add_argument('outfile')

    decrypt_parser = subparsers.add_parser('decrypt')
    decrypt_parser.add_argument('project_id')
    decrypt_parser.add_argument('location')
    decrypt_parser.add_argument('keyring')
    decrypt_parser.add_argument('cryptokey')
    decrypt_parser.add_argument('infile')
    decrypt_parser.add_argument('outfile')

    disable_cryptokey_version_parser = subparsers.add_parser(
        'disable_cryptokey_version')
    disable_cryptokey_version_parser.add_argument('project_id')
    disable_cryptokey_version_parser.add_argument('location')
    disable_cryptokey_version_parser.add_argument('keyring')
    disable_cryptokey_version_parser.add_argument('cryptokey')
    disable_cryptokey_version_parser.add_argument('version')

    destroy_cryptokey_version_parser = subparsers.add_parser(
        'destroy_cryptokey_version')
    destroy_cryptokey_version_parser.add_argument('project_id')
    destroy_cryptokey_version_parser.add_argument('location')
    destroy_cryptokey_version_parser.add_argument('keyring')
    destroy_cryptokey_version_parser.add_argument('cryptokey')
    destroy_cryptokey_version_parser.add_argument('version')

    add_member_to_cryptokey_policy_parser = subparsers.add_parser(
        'add_member_to_cryptokey_policy')
    add_member_to_cryptokey_policy_parser.add_argument('project_id')
    add_member_to_cryptokey_policy_parser.add_argument('location')
    add_member_to_cryptokey_policy_parser.add_argument('keyring')
    add_member_to_cryptokey_policy_parser.add_argument('cryptokey')
    add_member_to_cryptokey_policy_parser.add_argument('member')
    add_member_to_cryptokey_policy_parser.add_argument('role')

    get_keyring_policy_parser = subparsers.add_parser('get_keyring_policy')
    get_keyring_policy_parser.add_argument('project_id')
    get_keyring_policy_parser.add_argument('location')
    get_keyring_policy_parser.add_argument('keyring')

    args = parser.parse_args()

    if args.command == 'create_keyring':
        create_keyring(
            args.project_id,
            args.location,
            args.keyring)
    elif args.command == 'create_cryptokey':
        create_cryptokey(
            args.project_id,
            args.location,
            args.keyring,
            args.cryptokey)
    elif args.command == 'encrypt':
        encrypt(
            args.project_id,
            args.location,
            args.keyring,
            args.cryptokey,
            args.infile,
            args.outfile)
    elif args.command == 'decrypt':
        decrypt(
            args.project_id,
            args.location,
            args.keyring,
            args.cryptokey,
            args.infile,
            args.outfile)
    elif args.command == 'disable_cryptokey_version':
        disable_cryptokey_version(
            args.project_id,
            args.location,
            args.keyring,
            args.cryptokey,
            args.version)
    elif args.command == 'destroy_cryptokey_version':
        destroy_cryptokey_version(
            args.project_id,
            args.location,
            args.keyring,
            args.cryptokey,
            args.version)
    elif args.command == 'add_member_to_cryptokey_policy':
        add_member_to_cryptokey_policy(
            args.project_id,
            args.location,
            args.keyring,
            args.cryptokey,
            args.member,
            args.role)
    elif args.command == 'get_keyring_policy':
        get_keyring_policy(
            args.project_id,
            args.location,
            args.keyring)
