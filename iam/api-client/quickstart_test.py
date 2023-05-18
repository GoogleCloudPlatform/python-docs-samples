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

"""Tests for quickstart."""

import os
from typing import Iterator
import uuid

import google.auth
from googleapiclient import errors  # type: ignore
import googleapiclient.discovery  # type: ignore
import pytest
from retrying import retry

import quickstart

# Setting up variables for testing
GCLOUD_PROJECT = os.environ["GCLOUD_PROJECT"]


def retry_if_conflict(exception: Exception) -> bool:
    return isinstance(
        exception, errors.HttpError
    ) and "There were concurrent policy changes" in str(exception)


@pytest.fixture(scope="module")
def test_member() -> Iterator[str]:
    # section to create service account to test policy updates.
    # we use the first portion of uuid4 because full version is too long.
    name = f"test-{uuid.uuid4().hex[:25]}"
    email = name + "@" + GCLOUD_PROJECT + ".iam.gserviceaccount.com"
    member = "serviceAccount:" + email
    create_service_account(GCLOUD_PROJECT, name, "Py Test Account")

    yield member

    # deleting the service account created above
    delete_service_account(email)


def create_service_account(project_id: str, name: str, display_name: str) -> dict:
    """Creates a service account."""

    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    service = googleapiclient.discovery.build("iam", "v1", credentials=credentials)

    my_service_account = (
        service.projects()
        .serviceAccounts()
        .create(
            name="projects/" + project_id,
            body={"accountId": name, "serviceAccount": {"displayName": display_name}},
        )
        .execute()
    )

    print("Created service account: " + my_service_account["email"])
    return my_service_account


def delete_service_account(email: str) -> None:
    """Deletes a service account."""

    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    service = googleapiclient.discovery.build("iam", "v1", credentials=credentials)

    service.projects().serviceAccounts().delete(
        name="projects/-/serviceAccounts/" + email
    ).execute()

    print("Deleted service account: " + email)


def test_quickstart(test_member: str, capsys: pytest.CaptureFixture) -> None:
    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=5,
        retry_on_exception=retry_if_conflict,
    )
    def test_call() -> None:
        quickstart.quickstart(GCLOUD_PROJECT, test_member)
        out, _ = capsys.readouterr()
        assert test_member in out

    test_call()
