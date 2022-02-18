# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import json

import google.auth
from google.cloud import billing
import pytest

from main import stop_billing


PROJECT_ID = google.auth.default()[1]


@pytest.fixture
def project() -> str:
    # This test assumes billing is enabled on the project
    project_name = f"projects/{PROJECT_ID}"

    cloud_billing_client = billing.CloudBillingClient()
    request = billing.GetProjectBillingInfoRequest(name=project_name)
    project_billing_info = cloud_billing_client.get_project_billing_info(request)

    yield PROJECT_ID

    # Re-enable billing in teardown
    request = billing.UpdateProjectBillingInfoRequest(
        name=project_name,
        project_billing_info=billing.ProjectBillingInfo(
            billing_account_name=project_billing_info.billing_account_name
        ),
    )
    cloud_billing_client.update_project_billing_info(request)


def test_stop_billing_under_budget(capsys, project: str):
    billing_data = {
        "costAmount": 10,
        "budgetAmount": 100.1,
    }

    encoded_data = base64.b64encode(json.dumps(billing_data).encode("utf-8")).decode(
        "utf-8"
    )

    pubsub_message = {"data": encoded_data}
    stop_billing(pubsub_message, None)
    stdout, _ = capsys.readouterr()

    assert "No action necessary" in stdout


def test_stop_billing_over_budget(capsys, project: str):
    billing_data = {
        "costAmount": 120,
        "budgetAmount": 100.1,
    }

    encoded_data = base64.b64encode(json.dumps(billing_data).encode("utf-8")).decode(
        "utf-8"
    )

    pubsub_message = {"data": encoded_data}
    stop_billing(pubsub_message, None)
    stdout, _ = capsys.readouterr()
    assert "Billing disabled" in stdout

    # Stop billing again.
    stop_billing(pubsub_message, None)
    stdout, _ = capsys.readouterr()
    assert "Billing already disabled" in stdout
