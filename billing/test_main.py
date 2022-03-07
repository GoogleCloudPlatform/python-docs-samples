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
from unittest import mock

import google.auth
from google.cloud import billing

from main import stop_billing


PROJECT_ID = google.auth.default()[1]


def test_stop_billing_under_budget(capsys):
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


def test_stop_billing_over_budget(capsys):
    billing_data = {
        "costAmount": 120,
        "budgetAmount": 100.1,
    }

    encoded_data = base64.b64encode(json.dumps(billing_data).encode("utf-8")).decode(
        "utf-8"
    )

    pubsub_message = {"data": encoded_data}

    # NOTE(busunkim): The service account doesn't have sufficient permissions
    # to disable billing on projects. Mock the call that disables billing on
    # the project.
    with mock.patch(
        "google.cloud.billing.CloudBillingClient.update_project_billing_info",
        autospec=True,
    ) as update_billing:
        stop_billing(pubsub_message, None)
        update_billing.assert_called_once()
        assert update_billing.call_args.args[1].name == f"projects/{PROJECT_ID}"
        assert (
            update_billing.call_args.args[1].project_billing_info.billing_account_name
            == ""
        )
    stdout, _ = capsys.readouterr()
    assert "Billing disabled" in stdout


def test_stop_billing_already_disabled(capsys, project: str):
    billing_data = {
        "costAmount": 120,
        "budgetAmount": 100.1,
    }

    encoded_data = base64.b64encode(json.dumps(billing_data).encode("utf-8")).decode(
        "utf-8"
    )

    pubsub_message = {"data": encoded_data}

    # NOTE(busunkim): The service account doesn't have sufficient permissions
    # to disable billing on projects. Here we use a mock to test the case where
    # billing is alredy disabled.
    with mock.patch(
        "google.cloud.billing.CloudBillingClient.get_project_billing_info",
        autospec=True,
        return_value=billing.ProjectBillingInfo(billing_enabled=False),
    ):
        stop_billing(pubsub_message, None)

    stdout, _ = capsys.readouterr()
    assert "Billing already disabled" in stdout
