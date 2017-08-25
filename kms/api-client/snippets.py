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
def create_key_ring(project_id, location_id, key_ring_id):
    """Creates a KeyRing in the given location (e.g. global)."""

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build('cloudkms', 'v1')

    # The resource name of the location associated with the KeyRing.
    parent = 'projects/{}/locations/{}'.format(project_id, location_id)

    # Create KeyRing
    request = kms_client.projects().locations().keyRings().create(
        parent=parent, body={}, keyRingId=key_ring_id)
    response = request.execute()

    print('Created KeyRing {}.'.format(response['name']))
# [END kms_create_keyring]


# [START kms_create_cryptokey]
def create_crypto_key(project_id, location_id, key_ring_id, crypto_key_id):
    """Creates a CryptoKey within a KeyRing in the given location."""

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build('cloudkms', 'v1')

    # The resource name of the KeyRing associated with the CryptoKey.
    parent = 'projects/{}/locations/{}/keyRings/{}'.format(
        project_id, location_id, key_ring_id)

    # Create a CryptoKey for the given KeyRing.
    request = kms_client.projects().locations().keyRings().cryptoKeys().create(
        parent=parent, body={'purpose': 'ENCRYPT_DECRYPT'},
        cryptoKeyId=crypto_key_id)
    response = request.execute()

    print('Created CryptoKey {}.'.format(response['name']))
# [END kms_create_cryptokey]


# [START kms_encrypt]
def encrypt(project_id, location_id, key_ring_id, crypto_key_id,
            plaintext_file_name, ciphertext_file_name):
    """Encrypts data from plaintext_file_name using the provided CryptoKey and
    saves it to ciphertext_file_name so it can only be recovered with a call to
    decrypt.
    """

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build('cloudkms', 'v1')

    # The resource name of the CryptoKey.
    name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        project_id, location_id, key_ring_id, crypto_key_id)

    # Read data from the input file.
    with io.open(plaintext_file_name, 'rb') as plaintext_file:
        plaintext = plaintext_file.read()

    # Use the KMS API to encrypt the data.
    crypto_keys = kms_client.projects().locations().keyRings().cryptoKeys()
    request = crypto_keys.encrypt(
        name=name,
        body={'plaintext': base64.b64encode(plaintext).decode('ascii')})
    response = request.execute()
    ciphertext = base64.b64decode(response['ciphertext'].encode('ascii'))

    # Write the encrypted data to a file.
    with io.open(ciphertext_file_name, 'wb') as ciphertext_file:
        ciphertext_file.write(ciphertext)

    print('Saved ciphertext to {}.'.format(ciphertext_file_name))
# [END kms_encrypt]


# [START kms_decrypt]
def decrypt(project_id, location_id, key_ring_id, crypto_key_id,
            ciphertext_file_name, plaintext_file_name):
    """Decrypts data from ciphertext_file_name that was previously encrypted
    using the provided CryptoKey and saves it to plaintext_file_name."""

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build('cloudkms', 'v1')

    # The resource name of the CryptoKey.
    name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        project_id, location_id, key_ring_id, crypto_key_id)

    # Read encrypted data from the input file.
    with io.open(ciphertext_file_name, 'rb') as ciphertext_file:
        ciphertext = ciphertext_file.read()

    # Use the KMS API to decrypt the data.
    crypto_keys = kms_client.projects().locations().keyRings().cryptoKeys()
    request = crypto_keys.decrypt(
        name=name,
        body={'ciphertext': base64.b64encode(ciphertext).decode('ascii')})
    response = request.execute()
    plaintext = base64.b64decode(response['plaintext'].encode('ascii'))

    # Write the decrypted data to a file.
    with io.open(plaintext_file_name, 'wb') as plaintext_file:
        plaintext_file.write(plaintext)

    print('Saved plaintext to {}.'.format(plaintext_file_name))
# [END kms_decrypt]


# [START kms_disable_cryptokey_version]
def disable_crypto_key_version(project_id, location_id, key_ring_id,
                               crypto_key_id, version_id):
    """Disables a CryptoKeyVersion associated with a given CryptoKey and
    KeyRing."""

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build('cloudkms', 'v1')

    # Construct the resource name of the CryptoKeyVersion.
    name = (
        'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}/'
        'cryptoKeyVersions/{}'
        .format(
            project_id, location_id, key_ring_id, crypto_key_id, version_id))

    # Use the KMS API to disable the CryptoKeyVersion.
    crypto_keys = kms_client.projects().locations().keyRings().cryptoKeys()
    request = crypto_keys.cryptoKeyVersions().patch(
        name=name, body={'state': 'DISABLED'}, updateMask='state')
    response = request.execute()

    print('CryptoKeyVersion {}\'s state has been set to {}.'.format(
        name, response['state']))
# [END kms_disable_cryptokey_version]


# [START kms_destroy_cryptokey_version]
def destroy_crypto_key_version(
        project_id, location_id, key_ring_id, crypto_key_id, version_id):
    """Schedules a CryptoKeyVersion associated with a given CryptoKey and
    KeyRing for destruction 24 hours in the future."""

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build('cloudkms', 'v1')

    # Construct the resource name of the CryptoKeyVersion.
    name = (
        'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}/'
        'cryptoKeyVersions/{}'
        .format(
            project_id, location_id, key_ring_id, crypto_key_id, version_id))

    # Use the KMS API to schedule the CryptoKeyVersion for destruction.
    crypto_keys = kms_client.projects().locations().keyRings().cryptoKeys()
    request = crypto_keys.cryptoKeyVersions().destroy(name=name, body={})
    response = request.execute()

    print('CryptoKeyVersion {}\'s state has been set to {}.'.format(
        name, response['state']))
# [END kms_destroy_cryptokey_version]


# [START kms_add_member_to_cryptokey_policy]
def add_member_to_crypto_key_policy(
        project_id, location_id, key_ring_id, crypto_key_id, member, role):
    """Adds a member with a given role to the Identity and Access Management
    (IAM) policy for a given CryptoKey associated with a KeyRing."""

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build('cloudkms', 'v1')

    # The resource name of the CryptoKey.
    parent = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        project_id, location_id, key_ring_id, crypto_key_id)

    # Get the current IAM policy and add the new member to it.
    crypto_keys = kms_client.projects().locations().keyRings().cryptoKeys()
    policy_request = crypto_keys.getIamPolicy(resource=parent)
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
    crypto_keys = kms_client.projects().locations().keyRings().cryptoKeys()
    request = crypto_keys.setIamPolicy(
        resource=parent, body={'policy': policy_response})
    request.execute()

    print_msg = (
        'Member {} added with role {} to policy for CryptoKey {} in KeyRing {}'
        .format(member, role, crypto_key_id, key_ring_id))
    print(print_msg)
# [END kms_add_member_to_cryptokey_policy]


# [START kms_get_keyring_policy]
def get_key_ring_policy(project_id, location_id, key_ring_id):
    """Gets the Identity and Access Management (IAM) policy for a given KeyRing
    and prints out roles and the members assigned to those roles."""

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build('cloudkms', 'v1')

    # The resource name of the KeyRing.
    parent = 'projects/{}/locations/{}/keyRings/{}'.format(
        project_id, location_id, key_ring_id)

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

    create_key_ring_parser = subparsers.add_parser('create_key_ring')
    create_key_ring_parser.add_argument('project')
    create_key_ring_parser.add_argument('location')
    create_key_ring_parser.add_argument('key_ring')

    create_crypto_key_parser = subparsers.add_parser('create_crypto_key')
    create_crypto_key_parser.add_argument('project')
    create_crypto_key_parser.add_argument('location')
    create_crypto_key_parser.add_argument('key_ring')
    create_crypto_key_parser.add_argument('crypto_key')

    encrypt_parser = subparsers.add_parser('encrypt')
    encrypt_parser.add_argument('project')
    encrypt_parser.add_argument('location')
    encrypt_parser.add_argument('key_ring')
    encrypt_parser.add_argument('crypto_key')
    encrypt_parser.add_argument('infile')
    encrypt_parser.add_argument('outfile')

    decrypt_parser = subparsers.add_parser('decrypt')
    decrypt_parser.add_argument('project')
    decrypt_parser.add_argument('location')
    decrypt_parser.add_argument('key_ring')
    decrypt_parser.add_argument('crypto_key')
    decrypt_parser.add_argument('infile')
    decrypt_parser.add_argument('outfile')

    disable_crypto_key_version_parser = subparsers.add_parser(
        'disable_crypto_key_version')
    disable_crypto_key_version_parser.add_argument('project')
    disable_crypto_key_version_parser.add_argument('location')
    disable_crypto_key_version_parser.add_argument('key_ring')
    disable_crypto_key_version_parser.add_argument('crypto_key')
    disable_crypto_key_version_parser.add_argument('version')

    destroy_crypto_key_version_parser = subparsers.add_parser(
        'destroy_crypto_key_version')
    destroy_crypto_key_version_parser.add_argument('project')
    destroy_crypto_key_version_parser.add_argument('location')
    destroy_crypto_key_version_parser.add_argument('key_ring')
    destroy_crypto_key_version_parser.add_argument('crypto_key')
    destroy_crypto_key_version_parser.add_argument('version')

    add_member_to_crypto_key_policy_parser = subparsers.add_parser(
        'add_member_to_crypto_key_policy')
    add_member_to_crypto_key_policy_parser.add_argument('project')
    add_member_to_crypto_key_policy_parser.add_argument('location')
    add_member_to_crypto_key_policy_parser.add_argument('key_ring')
    add_member_to_crypto_key_policy_parser.add_argument('crypto_key')
    add_member_to_crypto_key_policy_parser.add_argument('member')
    add_member_to_crypto_key_policy_parser.add_argument('role')

    get_key_ring_policy_parser = subparsers.add_parser('get_key_ring_policy')
    get_key_ring_policy_parser.add_argument('project')
    get_key_ring_policy_parser.add_argument('location')
    get_key_ring_policy_parser.add_argument('key_ring')

    args = parser.parse_args()

    if args.command == 'create_key_ring':
        create_key_ring(
            args.project,
            args.location,
            args.key_ring)
    elif args.command == 'create_crypto_key':
        create_crypto_key(
            args.project,
            args.location,
            args.key_ring,
            args.crypto_key)
    elif args.command == 'encrypt':
        encrypt(
            args.project,
            args.location,
            args.key_ring,
            args.crypto_key,
            args.infile,
            args.outfile)
    elif args.command == 'decrypt':
        decrypt(
            args.project,
            args.location,
            args.key_ring,
            args.crypto_key,
            args.infile,
            args.outfile)
    elif args.command == 'disable_crypto_key_version':
        disable_crypto_key_version(
            args.project,
            args.location,
            args.key_ring,
            args.crypto_key,
            args.version)
    elif args.command == 'destroy_crypto_key_version':
        destroy_crypto_key_version(
            args.project,
            args.location,
            args.key_ring,
            args.crypto_key,
            args.version)
    elif args.command == 'add_member_to_crypto_key_policy':
        add_member_to_crypto_key_policy(
            args.project,
            args.location,
            args.key_ring,
            args.crypto_key,
            args.member,
            args.role)
    elif args.command == 'get_key_ring_policy':
        get_key_ring_policy(
            args.project,
            args.location,
            args.key_ring)
