# Copyright 2019 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Samples to illustrate management of HMAC keys via the python client library.
"""


from google.cloud import storage


def list_keys(project_id):
    """
    List all HMAC keys associated with the project.
    """
    # [START storage_list_hmac_keys]
    # project_id = 'Your Google Cloud project ID'
    storage_client = storage.Client(project=project_id)
    hmac_keys = storage_client.list_hmac_keys(project_id=project_id)
    print('HMAC Keys:')
    for hmac_key in hmac_keys:
        print('Service Account Email: {}'.format(
            hmac_key.service_account_email))
        print('Access ID: {}'.format(hmac_key.access_id))
    # [END storage_list_hmac_keys]
    return hmac_keys


def create_key(project_id, service_account_email):
    """
    Create a new HMAC key using the given project and service account.
    """
    # [START storage_create_hmac_key]
    # project_id = 'Your Google Cloud project ID'
    # service_account_email = 'Service account used to generate HMAC key'
    storage_client = storage.Client(project=project_id)
    hmac_key, secret = storage_client.create_hmac_key(
        service_account_email=service_account_email,
        project_id=project_id)
    print('The base64 encoded secret is {}'.format(secret))
    print('Do not miss that secret, there is no API to recover it.')
    print('The HMAC key metadata is:')
    print('Service Account Email: {}'.format(hmac_key.service_account_email))
    print('Key ID: {}'.format(hmac_key.id))
    print('Access ID: {}'.format(hmac_key.access_id))
    print('Project ID: {}'.format(hmac_key.project))
    print('State: {}'.format(hmac_key.state))
    print('Created At: {}'.format(hmac_key.time_created))
    print('Updated At: {}'.format(hmac_key.updated))
    print('Etag: {}'.format(hmac_key.etag))
    # [END storage_create_hmac_key]
    return hmac_key


def get_key(access_id, project_id):
    """
    Retrieve the HMACKeyMetadata with the given access id.
    """
    # [START storage_get_hmac_key]
    # project_id = 'Your Google Cloud project ID'
    # access_id = 'ID of an HMAC key'
    storage_client = storage.Client(project=project_id)
    hmac_key = storage_client.get_hmac_key_metadata(
        access_id,
        project_id=project_id)
    print('The HMAC key metadata is:')
    print('Service Account Email: {}'.format(hmac_key.service_account_email))
    print('Key ID: {}'.format(hmac_key.id))
    print('Access ID: {}'.format(hmac_key.access_id))
    print('Project ID: {}'.format(hmac_key.project))
    print('State: {}'.format(hmac_key.state))
    print('Created At: {}'.format(hmac_key.time_created))
    print('Updated At: {}'.format(hmac_key.updated))
    print('Etag: {}'.format(hmac_key.etag))
    # [END storage_get_hmac_key]
    return hmac_key


def activate_key(access_id, project_id):
    """
    Activate the HMAC key with the given access ID.
    """
    # [START storage_activate_hmac_key]
    # project_id = 'Your Google Cloud project ID'
    # access_id = 'ID of an inactive HMAC key'
    storage_client = storage.Client(project=project_id)
    hmac_key = storage_client.get_hmac_key_metadata(
        access_id,
        project_id=project_id)
    hmac_key.state = 'ACTIVE'
    hmac_key.update()
    print('The HMAC key metadata is:')
    print('Service Account Email: {}'.format(hmac_key.service_account_email))
    print('Key ID: {}'.format(hmac_key.id))
    print('Access ID: {}'.format(hmac_key.access_id))
    print('Project ID: {}'.format(hmac_key.project))
    print('State: {}'.format(hmac_key.state))
    print('Created At: {}'.format(hmac_key.time_created))
    print('Updated At: {}'.format(hmac_key.updated))
    print('Etag: {}'.format(hmac_key.etag))
    # [END storage_activate_hmac_key]
    return hmac_key


def deactivate_key(access_id, project_id):
    """
    Deactivate the HMAC key with the given access ID.
    """
    # [START storage_deactivate_hmac_key]
    # project_id = 'Your Google Cloud project ID'
    # access_id = 'ID of an active HMAC key'
    storage_client = storage.Client(project=project_id)
    hmac_key = storage_client.get_hmac_key_metadata(
        access_id,
        project_id=project_id)
    hmac_key.state = 'INACTIVE'
    hmac_key.update()
    print('The HMAC key is now inactive.')
    print('The HMAC key metadata is:')
    print('Service Account Email: {}'.format(hmac_key.service_account_email))
    print('Key ID: {}'.format(hmac_key.id))
    print('Access ID: {}'.format(hmac_key.access_id))
    print('Project ID: {}'.format(hmac_key.project))
    print('State: {}'.format(hmac_key.state))
    print('Created At: {}'.format(hmac_key.time_created))
    print('Updated At: {}'.format(hmac_key.updated))
    print('Etag: {}'.format(hmac_key.etag))
    # [END storage_deactivate_hmac_key]
    return hmac_key


def delete_key(access_id, project_id):
    """
    Delete the HMAC key with the given access ID. Key must have state INACTIVE
    in order to succeed.
    """
    # [START storage_delete_hmac_key]
    # project_id = 'Your Google Cloud project ID'
    # access_id = 'ID of an HMAC key (must be in INACTIVE state)'
    storage_client = storage.Client(project=project_id)
    hmac_key = storage_client.get_hmac_key_metadata(
        access_id,
        project_id=project_id)
    hmac_key.delete()
    print('The key is deleted, though it may still appear in list_hmac_keys()'
          ' results.')
    # [END storage_delete_hmac_key]
