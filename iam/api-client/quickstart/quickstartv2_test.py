# Copyright 2020 Google Inc. All Rights Reserved.
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
# limitations under the License.

"""Tests for quickstartv2."""

import os
import uuid

from google.oauth2 import service_account
from googleapiclient import errors
import googleapiclient.discovery
import pytest
import quickstartv2
from retrying import retry

# Setting up variables for testing
GCLOUD_PROJECT = os.environ["GCLOUD_PROJECT"]


def retry_if_conflict(exception):
    return (isinstance(exception, errors.HttpError)
            and 'There were concurrent policy changes' in str(exception))


@pytest.fixture(scope="module")
def test_member():
    # section to create service account to test policy updates.
    # we use the first portion of uuid4 because full version is too long.
    name = "python-test-" + str(uuid.uuid4()).split('-')[0]
    email = name + "@" + GCLOUD_PROJECT + ".iam.gserviceaccount.com"
    member = "serviceAccount:" + email
    create_service_account(
        GCLOUD_PROJECT, name, "Py Test Account"
    )

    yield member

    # deleting the service account created above
    delete_service_account(email)


def create_service_account(project_id, name, display_name):
    """Creates a service account."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    my_service_account = service.projects().serviceAccounts().create(
        name='projects/' + project_id,
        body={
            'accountId': name,
            'serviceAccount': {
                'displayName': display_name
            }
        }).execute()

    print('Created service account: ' + my_service_account['email'])
    return my_service_account


def delete_service_account(email):
    """Deletes a service account."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    service.projects().serviceAccounts().delete(
        name='projects/-/serviceAccounts/' + email).execute()

    print('Deleted service account: ' + email)


def test_quickstartv2(test_member, capsys):
    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000,
           stop_max_attempt_number=5, retry_on_exception=retry_if_conflict)
    def test_call():
        """Test follows the structure of quickstartv2 quickstart()"""

        project_id = GCLOUD_PROJECT
        role = "roles/logging.logWriter"

        """Initializes service."""
        crm_service = quickstartv2.initialize_service()

        """Grants your member the 'Log Writer' role for the project."""
        quickstartv2.modify_policy_add_role(
            crm_service, project_id, role, test_member)

        """Gets the project's policy and prints all members with the 'Log Writer' role."""
        policy = quickstartv2.get_policy(crm_service, project_id)
        binding = next(b for b in policy["bindings"] if b["role"] == role)
        print("Role: " + binding["role"])
        print("Members: ")
        for m in binding["members"]:
            print("[" + m + "] ")

        out, _ = capsys.readouterr()
        assert test_member in out

        """Removes the member from the 'Log Writer' role"""
        quickstartv2.modify_policy_remove_member(
            crm_service, project_id, role, test_member)
    test_call()
