# Copyright 2020 Google LLC
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

import datetime
import os
import uuid

from google.api_core import client_options
import google.api_core.exceptions
import google.auth
from google.cloud import bigquery
from google.cloud import bigquery_datatransfer
import pytest


def temp_suffix():
    now = datetime.datetime.now()
    return f"{now.strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"


@pytest.fixture(scope="session")
def bigquery_client(default_credentials):
    credentials, project_id = default_credentials
    return bigquery.Client(credentials=credentials, project=project_id)


@pytest.fixture(scope="session")
def dataset_id(bigquery_client, project_id):
    dataset_id = f"bqdts_{temp_suffix()}"
    bigquery_client.create_dataset(f"{project_id}.{dataset_id}")
    yield dataset_id
    bigquery_client.delete_dataset(dataset_id, delete_contents=True)


@pytest.fixture(scope="session")
def default_credentials():
    return google.auth.default(["https://www.googleapis.com/auth/cloud-platform"])


@pytest.fixture(scope="session")
def project_id():
    return os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture(scope="session")
def service_account_name(default_credentials):
    credentials, _ = default_credentials
    # Note: this property is not available when running with user account
    # credentials, but only service account credentials are used in our test
    # infrastructure.
    return credentials.service_account_email


@pytest.fixture(scope="session")
def transfer_client(default_credentials, project_id):
    credentials, _ = default_credentials
    options = client_options.ClientOptions(quota_project_id=project_id)

    transfer_client = bigquery_datatransfer.DataTransferServiceClient(
        credentials=credentials, client_options=options
    )

    # Ensure quota is always attributed to the correct project.
    bigquery_datatransfer.DataTransferServiceClient = lambda: transfer_client

    return transfer_client


@pytest.fixture(scope="session")
def transfer_config_name(transfer_client, project_id, dataset_id, service_account_name):
    from . import manage_transfer_configs, scheduled_query

    # Use the transfer_client fixture so we know quota is attributed to the
    # correct project.
    assert transfer_client is not None

    # To conserve limited BQ-DTS quota, this fixture creates only one transfer
    # config for a whole session and is used to test the scheduled_query.py and
    # the delete operation in manage_transfer_configs.py.
    transfer_config = scheduled_query.create_scheduled_query(
        {
            "project_id": project_id,
            "dataset_id": dataset_id,
            "service_account_name": service_account_name,
        }
    )
    yield transfer_config.name
    manage_transfer_configs.delete_config(
        {"transfer_config_name": transfer_config.name}
    )


@pytest.fixture
def to_delete_configs(transfer_client):
    to_delete = []
    yield to_delete
    for config_name in to_delete:
        try:
            transfer_client.delete_transfer_config(name=config_name)
        except google.api_core.exceptions.GoogleAPICallError:
            pass
