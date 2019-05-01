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


from google.cloud import kms_v1
from google.cloud.kms_v1 import enums


# [START kms_create_keyring]
def create_key_ring(project_id, location_id, key_ring_id):
    """Creates a KeyRing in the given location (e.g. global)."""

    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # The resource name of the location associated with the KeyRing.
    parent = client.location_path(project_id, location_id)

    # The keyring object template
    keyring_name = client.key_ring_path(project_id, location_id, key_ring_id)
    keyring = {'name': keyring_name}

    # Create a KeyRing
    response = client.create_key_ring(parent, key_ring_id, keyring)

    print('Created KeyRing {}.'.format(response.name))
    return response
# [END kms_create_keyring]


# [START kms_create_cryptokey]
def create_crypto_key(project_id, location_id, key_ring_id, crypto_key_id):
    """Creates a CryptoKey within a KeyRing in the given location."""

    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # The resource name of the KeyRing associated with the CryptoKey.
    parent = client.key_ring_path(project_id, location_id, key_ring_id)

    # Create the CryptoKey object template
    purpose = enums.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    crypto_key = {'purpose': purpose}

    # Create a CryptoKey for the given KeyRing.
    response = client.create_crypto_key(parent, crypto_key_id, crypto_key)

    print('Created CryptoKey {}.'.format(response.name))
    return response
# [END kms_create_cryptokey]


# [START kms_encrypt]
def encrypt_symmetric(project_id, location_id, key_ring_id, crypto_key_id,
                      plaintext):
    """Encrypts input plaintext data using the provided symmetric CryptoKey."""

    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # The resource name of the CryptoKey.
    name = client.crypto_key_path_path(project_id, location_id, key_ring_id,
                                       crypto_key_id)

    # Use the KMS API to encrypt the data.
    response = client.encrypt(name, plaintext)
    return response.ciphertext
# [END kms_encrypt]


# [START kms_decrypt]
def decrypt_symmetric(project_id, location_id, key_ring_id, crypto_key_id,
                      ciphertext):
    """Decrypts input ciphertext using the provided symmetric CryptoKey."""

    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # The resource name of the CryptoKey.
    name = client.crypto_key_path_path(project_id, location_id, key_ring_id,
                                       crypto_key_id)
    # Use the KMS API to decrypt the data.
    response = client.decrypt(name, ciphertext)
    return response.plaintext
# [END kms_decrypt]


# [START kms_disable_cryptokey_version]
def disable_crypto_key_version(project_id, location_id, key_ring_id,
                               crypto_key_id, version_id):
    """Disables a CryptoKeyVersion associated with a given CryptoKey and
    KeyRing."""

    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # Construct the resource name of the CryptoKeyVersion.
    name = client.crypto_key_version_path(project_id, location_id, key_ring_id,
                                          crypto_key_id, version_id)

    # Use the KMS API to disable the CryptoKeyVersion.
    new_state = enums.CryptoKeyVersion.CryptoKeyVersionState.DISABLED
    version = {'name': name, 'state': new_state}
    update_mask = {'paths': ["state"]}

    # Print results
    response = client.update_crypto_key_version(version, update_mask)
    print('CryptoKeyVersion {}\'s state has been set to {}.'.format(
        name, response.state))
# [END kms_disable_cryptokey_version]


# [START kms_enable_cryptokey_version]
def enable_crypto_key_version(project_id, location_id, key_ring_id,
                              crypto_key_id, version_id):
    """Enables a CryptoKeyVersion associated with a given CryptoKey and
    KeyRing."""

    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # Construct the resource name of the CryptoKeyVersion.
    name = client.crypto_key_version_path(project_id, location_id, key_ring_id,
                                          crypto_key_id, version_id)

    # Use the KMS API to enable the CryptoKeyVersion.
    new_state = enums.CryptoKeyVersion.CryptoKeyVersionState.ENABLED
    version = {'name': name, 'state': new_state}
    update_mask = {'paths': ["state"]}

    # Print results
    response = client.update_crypto_key_version(version, update_mask)
    print('CryptoKeyVersion {}\'s state has been set to {}.'.format(
        name, response.state))
# [END kms_enable_cryptokey_version]


# [START kms_destroy_cryptokey_version]
def destroy_crypto_key_version(
        project_id, location_id, key_ring_id, crypto_key_id, version_id):
    """Schedules a CryptoKeyVersion associated with a given CryptoKey and
    KeyRing for destruction 24 hours in the future."""

    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # Construct the resource name of the CryptoKeyVersion.
    name = client.crypto_key_version_path(project_id, location_id, key_ring_id,
                                          crypto_key_id, version_id)

    # Use the KMS API to mark the CryptoKeyVersion for destruction.
    response = client.destroy_crypto_key_version(name)

    # Print results
    print('CryptoKeyVersion {}\'s state has been set to {}.'.format(
        name, response.state))
# [END kms_destroy_cryptokey_version]


# [START kms_restore_cryptokey_version]
def restore_crypto_key_version(
        project_id, location_id, key_ring_id, crypto_key_id, version_id):
    """Restores a CryptoKeyVersion that is scheduled for destruction."""

    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # Construct the resource name of the CryptoKeyVersion.
    name = client.crypto_key_version_path(project_id, location_id, key_ring_id,
                                          crypto_key_id, version_id)

    # Use the KMS API to restore the CryptoKeyVersion.
    response = client.restore_crypto_key_version(name)

    # Print results
    print('CryptoKeyVersion {}\'s state has been set to {}.'.format(
        name, response.state))


# [END kms_restore_cryptokey_version]


# [START kms_add_member_to_cryptokey_policy]
def add_member_to_crypto_key_policy(
        project_id, location_id, key_ring_id, crypto_key_id, member, role):
    """Adds a member with a given role to the Identity and Access Management
    (IAM) policy for a given CryptoKey associated with a KeyRing."""

    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # The resource name of the CryptoKey.
    resource = client.crypto_key_path_path(project_id, location_id,
                                           key_ring_id, crypto_key_id)
    # Get the current IAM policy.
    policy = client.get_iam_policy(resource)

    # Add member
    policy.bindings.add(
        role=role,
        members=[member])

    # Update the IAM Policy.
    client.set_iam_policy(resource, policy)

    # Print results
    print('Member {} added with role {} to policy for CryptoKey {} \
           in KeyRing {}'.format(member, role, crypto_key_id, key_ring_id))
# [END kms_add_member_to_cryptokey_policy]


# [START kms_add_member_to_keyring_policy]
def add_member_to_key_ring_policy(
        project_id, location_id, key_ring_id, member, role):
    """Adds a member with a given role to the Identity and Access Management
    (IAM) policy for a given KeyRing."""

    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # The resource name of the KeyRing.
    resource = client.key_ring_path(project_id, location_id, key_ring_id)

    # Get the current IAM policy.
    policy = client.get_iam_policy(resource)

    # Add member
    policy.bindings.add(
        role=role,
        members=[member])

    # Update the IAM Policy.
    client.set_iam_policy(resource, policy)

    # Print results
    print('Member {} added with role {} to policy in KeyRing {}'
          .format(member, role, key_ring_id))

# [END kms_add_member_to_keyring_policy]


# [START kms_remove_member_from_cryptokey_policy]
def remove_member_from_crypto_key_policy(
        project_id, location_id, key_ring_id, crypto_key_id, member, role):
    """Removes a member with a given role from the Identity and Access
    Management (IAM) policy for a given CryptoKey associated with a KeyRing."""

    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # The resource name of the CryptoKey.
    resource = client.crypto_key_path_path(project_id, location_id,
                                           key_ring_id, crypto_key_id)
    # Get the current IAM policy.
    policy = client.get_iam_policy(resource)

    # Remove member
    for b in list(policy.bindings):
        if b.role == role and member in b.members:
            b.members.remove(member)

    # Update the IAM Policy.
    client.set_iam_policy(resource, policy)

    # Print results
    print('Member {} removed from role {} for CryptoKey in KeyRing {}'
          .format(member, role, crypto_key_id, key_ring_id))
# [END kms_remove_member_from_cryptokey_policy]


def remove_member_from_key_ring_policy(project_id, location_id, key_ring_id,
                                       member, role):
    """Removes a member with a given role from the Identity and Access
    Management (IAM) policy for a given KeyRing."""

    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # The resource name of the KeyRing.
    resource = client.key_ring_path(project_id, location_id, key_ring_id)

    # Get the current IAM policy.
    policy = client.get_iam_policy(resource)

    # Remove member
    for b in list(policy.bindings):
        if b.role == role and member in b.members:
            b.members.remove(member)

    # Update the IAM Policy.
    client.set_iam_policy(resource, policy)

    # Print results
    print('Member {} removed from role {} for KeyRing {}'
          .format(member, role, key_ring_id))


# [START kms_get_keyring_policy]
def get_key_ring_policy(project_id, location_id, key_ring_id):
    """Gets the Identity and Access Management (IAM) policy for a given KeyRing
    and prints out roles and the members assigned to those roles."""

    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # The resource name of the KeyRing.
    resource = client.key_ring_path(project_id, location_id, key_ring_id)

    # Get the current IAM policy.
    policy = client.get_iam_policy(resource)

    # Print results
    print('Printing IAM policy for resource {}:'.format(resource))
    for b in policy.bindings:
        for m in b.members:
            print('Role: {} Member: {}'.format(b.role, m))
    return policy
# [END kms_get_keyring_policy]


def get_crypto_key_policy(project_id, location_id, key_ring_id, crypto_key_id):
    """Gets the Identity and Access Management (IAM) policy for a given KeyRing
    and prints out roles and the members assigned to those roles."""

    # Creates an API client for the KMS API.
    client = kms_v1.KeyManagementServiceClient()

    # The resource name of the CryptoKey.
    resource = client.crypto_key_path_path(project_id, location_id,
                                           key_ring_id, crypto_key_id)

    # Get the current IAM policy.
    policy = client.get_iam_policy(resource)

    # Print results
    print('Printing IAM policy for resource {}:'.format(resource))
    for b in policy.bindings:
        for m in b.members:
            print('Role: {} Member: {}'.format(b.role, m))
    return policy
