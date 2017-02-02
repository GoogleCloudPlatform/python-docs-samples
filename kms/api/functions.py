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

# Imports the Google APIs client library
from googleapiclient import discovery


# [START kms_create_keyring]
def create_keyring(project_id, location, keyring):

    # Creates an API client for the KMS API.
    kms_client = discovery.build('cloudkms', 'v1beta1')

    # The resource name of the location associated with the KeyRing.
    parent = 'projects/{}/locations/{}'.format(project_id, location)

    # Create KeyRing
    request = kms_client.projects().locations().keyRings().create(
        parent=parent, body={}, keyRingId=keyring)
    response = request.execute()

    print 'Created KeyRing {}.'.format(response["name"])
# [END kms_create_keyring]


# [START kms_create_cryptokey]
def create_cryptokey(project_id, location, keyring, cryptokey):

    # Creates an API client for the KMS API.
    kms_client = discovery.build('cloudkms', 'v1beta1')

    # The resource name of the KeyRing associated with the CryptoKey.
    parent = 'projects/{}/locations/{}/keyRings/{}'.format(
        project_id, location, keyring)

    # Create a CryptoKey for the given KeyRing.
    request = kms_client.projects().locations().keyRings().cryptoKeys().create(
        parent=parent, body={"purpose": 'ENCRYPT_DECRYPT'},
        cryptoKeyId=cryptokey)
    response = request.execute()

    print 'Created CryptoKey {}.'.format(response["name"])
# [END kms_create_cryptokey]


# [START kms_encrypt]
def encrypt(project_id, location, keyring, cryptokey, infile, outfile):

    # Creates an API client for the KMS API.
    kms_client = discovery.build('cloudkms', 'v1beta1')

    # The resource name of the CryptoKey.
    name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        project_id, location, keyring, cryptokey)

    # Read text from input file.
    i = open(infile, 'r')
    text = i.read()
    i.close()
    encoded_text = base64.b64encode(text)

    # Use the KMS API to encrypt the text.
    request = kms_client.projects().locations().keyRings().cryptoKeys().encrypt(name=name, body={"plaintext": encoded_text})
    response = request.execute()

    # Write the encrypted text to a file.
    o = open(outfile, 'w')
    o.write(response["ciphertext"])
    o.close()

    print 'Saved encrypted text to {}.'.format(outfile)
# [END kms_encrypt]


# [START kms_decrypt]
def decrypt(project_id, location, keyring, cryptokey, infile, outfile):

    # Creates an API client for the KMS API.
    kms_client = discovery.build('cloudkms', 'v1beta1')

    # The resource name of the CryptoKey.
    name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        project_id, location, keyring, cryptokey)

    # Read cipher text from input file.
    i = open(infile, 'r')
    cipher_text = i.read()
    i.close()

    # Use the KMS API to decrypt the text.
    request = kms_client.projects().locations().keyRings().cryptoKeys().decrypt(name=name, body={"ciphertext": cipher_text})
    response = request.execute()

    # Write the plain text to a file.
    o = open(outfile, 'w')
    plaintext_encoded = response["plaintext"]
    plaintext_decoded = base64.b64decode(plaintext_encoded)
    o.write(plaintext_decoded)
    o.close()

    print 'Saved decrypted text to {}.'.format(outfile)
# [END kms_decrypt]


# [START kms_disable_cryptokey_version]
def disable_cryptokey_version(project_id, location, keyring, cryptokey, version):
    # Creates an API client for the KMS API.
    kms_client = discovery.build('cloudkms', 'v1beta1')

    # The resource name of the CryptoKeyVersion.
    name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}/cryptoKeyVersions/{}'.format(project_id, location, keyring, cryptokey, version)

    # Use the KMS API to disable the CryptoKeyVersion.
    request = kms_client.projects().locations().keyRings().cryptoKeys().cryptoKeyVersions().patch(name=name, body={"state": 'DISABLED'}, updateMask="state")
    response = request.execute()

    print 'CryptoKeyVersion {}\'s state has been set to {}.'.format(
        name, response["state"])
# [END kms_disable_cryptokey_version]


# [START kms_destroy_cryptokey_version]
def destroy_cryptokey_version(
        project_id, location, keyring, cryptokey, version):
    # Creates an API client for the KMS API.
    kms_client = discovery.build('cloudkms', 'v1beta1')

    # The resource name of the CryptoKeyVersion.
    name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}/cryptoKeyVersions/{}'.format(project_id, location, keyring, cryptokey, version)

    # Use the KMS API to schedule the CryptoKeyVersion for destruction.
    request = kms_client.projects().locations().keyRings().cryptoKeys().cryptoKeyVersions().destroy(name=name, body={})
    response = request.execute()

    print 'CryptoKeyVersion {}\'s state has been set to {}.'.format(
        name, response["state"])
# [END kms_destroy_cryptokey_version]


# [START kms_add_member_to_cryptokey_policy]
def add_member_to_cryptokey_policy(
        project_id, location, keyring, cryptokey, member, role):
    # Creates an API client for the KMS API.
    kms_client = discovery.build('cloudkms', 'v1beta1')

    # The resource name of the CryptoKey.
    parent = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        project_id, location, keyring, cryptokey)

    # Get the current IAM policy and add the new member to it.
    policy_request = kms_client.projects().locations().keyRings().cryptoKeys().getIamPolicy(resource=parent)
    policy_response = policy_request.execute()
    if 'bindings' in policy_response.keys():
        role_already_exists = False
        for binding in policy_response['bindings']:
            if binding['role'] == role:
                role_already_exists = True
                member_already_exists = False
                for user in binding['members']:
                    if user == member:
                        member_already_exists = True
                if not member_already_exists:
                    binding['members'].append(member)
        if not role_already_exists:
            members = []
            members.append(member)
            binding = dict()
            binding['role'] = role
            binding['members'] = members
            policy_response['bindings'].append(binding)
    else:
        members = []
        members.append(member)
        binding = dict()
        binding['role'] = role
        binding['members'] = members
        bindings = []
        bindings.append(binding)
        policy_response['bindings'] = bindings

    # Set the new IAM Policy.
    request = kms_client.projects().locations().keyRings().cryptoKeys().setIamPolicy(resource=parent, body={"policy": policy_response})
    request.execute()

    print 'Member {} added with role {} to policy for CryptoKey {} in KeyRing {}'.format(member, role, cryptokey, keyring)
# [END kms_add_member_to_cryptokey_policy]


# [START kms_get_keyring_policy]
def get_keyring_policy(project_id, location, keyring):
    # Creates an API client for the KMS API.
    kms_client = discovery.build('cloudkms', 'v1beta1')

    # The resource name of the KeyRing.
    parent = 'projects/{}/locations/{}/keyRings/{}'.format(
        project_id, location, keyring)

    # Get the current IAM policy.
    request = kms_client.projects().locations().keyRings().getIamPolicy(
        resource=parent)
    response = request.execute()

    if 'bindings' in response.keys():
        print 'Printing IAM policy for resource {}:'.format(parent)
        for binding in response['bindings']:
            print ''
            print 'Role: {}'.format(binding['role'])
            print 'Members:'
            for member in binding['members']:
                print member
        print ''
    else:
        print 'No roles found for resource {}.'.format(parent)
# [END kms_get_keyring_policy]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

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

    other_parser = subparsers.add_parser('other')

    args = parser.parse_args()

    if args.command == 'encrypt':
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
