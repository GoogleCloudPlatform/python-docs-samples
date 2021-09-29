#!/usr/bin/env python

# Copyright 2021 Google Inc. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module rotates the user-managed SA key in the google cloud platform and
syncs/updates it in Github secret"""

from base64 import b64encode
import json
import os
import subprocess
from typing import Tuple

from google.oauth2 import service_account
import googleapiclient.discovery
from nacl import encoding, public
import requests


api_public_key = os.environ.get('API_PUBLIC_KEY')
api_secret = os.environ.get('API_SECRET')
service_acc = os.environ.get('SERVICE_ACCOUNT')
personal_access_token = os.environ.get('GIT_PAT')
project = os.environ.get('GCP_PROJECT')

sakeys = list()


def create_key() -> None:
    """Creates a service account key"""
    subprocess.run(["gcloud", "iam", "service-accounts", "keys", "create", "sakey.json", "--iam-account=" + service_acc], check=True)


# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/HEAD/iam/api-client/service_account_keys.py#L77
def delete_key(full_key_name: str) -> None:
    """Deletes service account keys"""
    credentials = service_account.Credentials.from_service_account_file(
        filename="sakey.json",
        scopes=['https://www.googleapis.com/auth/cloud-platform'])
    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)
    service.projects().serviceAccounts().keys().delete(
        name=full_key_name).execute()
    print(f"Deleted key: {full_key_name}")


def delete_sa_keys() -> None:
    """Deletes old service account keys if the new key is synced in Github secrets
    successfully. Otherwise, it deletes the newly created service account key and
    leaves the old keys untouched"""
    list_keys(service_acc)
    path = "projects/" + project + "/serviceAccounts/" + service_acc + "/keys/"
    with open('sakey.json', 'r') as sa_key:
        data = json.load(sa_key)
        latest = data['private_key_id']
        status_code = github_sync(api_secret, personal_access_token)
        if status_code == 204:
            for key in sakeys:
                if key != latest:
                    full_key_name = path + key
                    delete_key(full_key_name)
        else:
            latest_key_name = path + latest
            delete_key(latest_key_name)
    subprocess.run(["rm", "sakey.json"], check=True)


# https://docs.github.com/en/rest/reference/actions#example-encrypting-a-secret-using-python
def encrypt(public_key: str, secret_value: str) -> str:
    """Encrypts a Unicode string using the public key"""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


def encrypt_with_key() -> str:
    """Encrypts new service account key"""
    with open('sakey.json', 'r') as sa_key:
        data = json.load(sa_key)
        dump = json.dumps(data)
        result = get_key(api_public_key, personal_access_token)
        key = result[1]
        encrypted_value = encrypt(key, dump)
        return encrypted_value


# https://docs.github.com/en/rest/reference/actions#get-a-repository-public-key
def get_key(url: str, token: str) -> Tuple[str, str]:
    """Fetches the key_id and key"""
    headers = {
        "Authorization": "token " + token
    }
    response = requests.get(url, headers=headers)
    root = response.json()
    key_id = root['key_id']
    key = root['key']
    return key_id, key


def github_sync(url: str, token: str) -> int:
    """Syncs the new service account key in Github secrets"""
    headers = {
        "Authorization": "token " + token
    }
    result = get_key(api_public_key, personal_access_token)
    key_id = result[0]
    payload = {'encrypted_value': encrypt_with_key(), 'key_id': key_id}
    update = requests.put(url, headers=headers, json=payload)
    if update.status_code == 204:
        print("***** New SA key synced in github secrets *****")
    else:
        print("***** Problem in Syncing. Please check the configuration *****")
    return update.status_code


# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/HEAD/iam/api-client/service_account_keys.py#L58
def list_keys(service_account_email: str) -> None:
    """Lists all keys for a service account and appends the user-managed keys in a separate list"""
    credentials = service_account.Credentials.from_service_account_file(
        filename="sakey.json",
        scopes=['https://www.googleapis.com/auth/cloud-platform'])
    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)
    keys = service.projects().serviceAccounts().keys().list(
        name='projects/-/serviceAccounts/' + service_account_email).execute()
    for key in keys['keys']:
        if key['keyType'] != "SYSTEM_MANAGED":
            sakeys.append(key['name'].split('/')[-1])


if __name__ == '__main__':
    create_key()
    delete_sa_keys()
