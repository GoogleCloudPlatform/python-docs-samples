# Copyright 2020 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import pytest
import subprocess
from urllib import request

import os

from google.oauth2 import service_account
import googleapiclient.discovery

# Setting up variables for testing
GCLOUD_PROJECT = os.environ["GCLOUD_PROJECT"]
ACCOUNTS = ["renderer-identity", "editor-identity"]

@pytest.fixture(scope="module")
def services():
    #Get credentials
    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

    #Create the Cloud IAM service
    iam_service = googleapiclient.discovery.build('iam', 'v1', 
            credentials=credentials) 

    # Create service accounts for editor and renderer
    try:
        # Note: Will fail if service accounts already exist
        for account in ACCOUNTS:
            iam_service.projects().serviceAccounts().create(
                name=f"projects/{GCLOUD_PROJECT}",
                body={
                "accountId": account,
                "serviceAccount": {
                    "displayName": account
                     }
                }).execute()
    except Exception as e:
        print(e)

    # Build and Deploy Cloud Run Services
    subprocess.run(["gcloud", "builds", "submit", "--config", 
        "test_setup.yaml", "--quiet"])

    # Get the URL for the editor and the token
    editor = subprocess.run(["gcloud", "run", "--platform=managed", 
                    "--region=us-central1", "services", 
                    "describe", "editor", 
                    "--format=value(status.url)"], 
                    stdout=subprocess.PIPE).stdout.strip()
    token = subprocess.run(["gcloud", "auth", "print-identity-token"], 
                    stdout=subprocess.PIPE).stdout.strip()

    yield editor, token, iam_service


def test_end_to_end(services):
    editor = services[0].decode() + '/render'
    token = services[1].decode()
    data = json.dumps({"data": "**strong text**"})

    print(token)
    print(editor)

    req = request.Request(editor, data=data.encode(),  
        headers={"Authorization": f"Bearer {token}", 
                 "Content-Type": "application/json"})
    
    response = request.urlopen(req)
    assert response.status == 200

    body = response.read()
    assert "<p><strong>strong text</strong></p>" in body.decode()

    tear_down(services[2])


def tear_down(service):
    # Delete the service accounts for editor and renderer
    for account in ACCOUNTS:
        email = account + f"@{GCLOUD_PROJECT}.iam.gserviceaccount.com"
        service.projects().serviceAccounts().delete(
            name=f'projects/{GCLOUD_PROJECT}/serviceAccounts/{email}').execute()
        print(f"Deleted service-account: {account}")

    subprocess.run(
        ["gcloud", "run", "services", "delete", "editor", "--quiet"])
    subprocess.run(
        ["gcloud", "run", "services", "delete", "renderer", "--quiet"])


