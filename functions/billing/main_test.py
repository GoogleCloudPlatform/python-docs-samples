# Copyright 2023 Google LLC
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

import base64
import json

from unittest.mock import MagicMock, patch

import main


@patch("main.slack_client")
def test_notify_slack(slack_client):
    slack_client.api_call = MagicMock()

    data = {"budgetAmount": 400, "costAmount": 500}
    attrs = {"foo": "bar"}

    pubsub_message = {
        "data": base64.b64encode(bytes(json.dumps(data), "utf-8")),
        "attributes": attrs,
    }

    main.notify_slack(pubsub_message, None)

    assert slack_client.api_call.called


@patch("main.PROJECT_ID", "my-project")
@patch("main.PROJECT_NAME", "projects/my-project")
@patch("main.discovery")
def test_disable_billing(discovery_mock):
    PROJECT_NAME = f"projects/{main.PROJECT_ID}"

    data = {"budgetAmount": 400, "costAmount": 500}

    pubsub_message = {
        "data": base64.b64encode(bytes(json.dumps(data), "utf-8")),
        "attributes": {},
    }

    projects_mock = MagicMock()
    projects_mock.projects = MagicMock(return_value=projects_mock)
    projects_mock.getBillingInfo = MagicMock(return_value=projects_mock)
    projects_mock.updateBillingInfo = MagicMock(return_value=projects_mock)
    projects_mock.execute = MagicMock(return_value={"billingEnabled": True})

    discovery_mock.build = MagicMock(return_value=projects_mock)

    main.stop_billing(pubsub_message, None)

    projects_mock.getBillingInfo.assert_called_with(name=PROJECT_NAME)
    projects_mock.updateBillingInfo.assert_called_with(
        name=PROJECT_NAME, body={"billingAccountName": ""}
    )
    assert projects_mock.execute.call_count == 2


@patch("main.PROJECT_ID", "my-project")
@patch("main.PROJECT_NAME", "projects/my-project")
@patch("main.ZONE", "my-zone")
@patch("main.discovery")
def test_limit_use(discovery_mock):
    data = {"budgetAmount": 400, "costAmount": 500}

    pubsub_message = {
        "data": base64.b64encode(bytes(json.dumps(data), "utf-8")),
        "attributes": {},
    }

    instances_list = {
        "items": [
            {"name": "instance-1", "status": "RUNNING"},
            {"name": "instance-2", "status": "TERMINATED"},
        ]
    }

    instances_mock = MagicMock()
    instances_mock.instances = MagicMock(return_value=instances_mock)
    instances_mock.list = MagicMock(return_value=instances_mock)
    instances_mock.stop = MagicMock(return_value=instances_mock)
    instances_mock.execute = MagicMock(return_value=instances_list)

    projects_mock = MagicMock()
    projects_mock.projects = MagicMock(return_value=projects_mock)
    projects_mock.getBillingInfo = MagicMock(return_value=projects_mock)
    projects_mock.execute = MagicMock(return_value={"billingEnabled": True})

    def discovery_mocker(x, *args, **kwargs):
        if x == "compute":
            return instances_mock
        else:
            return projects_mock

    discovery_mock.build = MagicMock(side_effect=discovery_mocker)

    main.limit_use(pubsub_message, None)

    instances_mock.list.assert_called_with(project=main.PROJECT_ID, zone=main.ZONE)
    assert instances_mock.stop.call_count == 1
    assert instances_mock.execute.call_count == 2


@patch("main.PROJECT_ID", "my-project")
@patch("main.APP_NAME", "my-project")
@patch("main.PROJECT_NAME", "projects/my-project")
@patch("main.ZONE", "my-zone")
@patch("main.discovery")
def test_limit_use_appengine(discovery_mock):
    PROJECT_ID = main.PROJECT_ID

    data = {"budgetAmount": 400, "costAmount": 500}

    pubsub_message = {
        "data": base64.b64encode(bytes(json.dumps(data), "utf-8")),
        "attributes": {},
    }

    projects_mock = MagicMock()
    projects_mock.projects = MagicMock(return_value=projects_mock)
    projects_mock.getBillingInfo = MagicMock(return_value=projects_mock)
    projects_mock.updateBillingInfo = MagicMock(return_value=projects_mock)

    apps_list = {"servingStatus": "SERVING"}
    app_patch_mock = MagicMock()
    apps_mock = MagicMock()
    apps_mock.get.return_value.execute.return_value = apps_list
    apps_mock.patch.return_value.execute.return_value = app_patch_mock
    appengine_mock = MagicMock()
    appengine_mock.apps.return_value = apps_mock

    def discovery_mocker(x, *args, **kwargs):
        if x == "appengine":
            return appengine_mock
        else:
            return projects_mock

    discovery_mock.build = MagicMock(side_effect=discovery_mocker)

    main.limit_use_appengine(pubsub_message, None)

    patch_body = {"servingStatus": "USER_DISABLED"}

    apps_mock.get.assert_called_with(appsId=PROJECT_ID)
    apps_mock.patch.assert_called_with(
        appsId=PROJECT_ID, updateMask="serving_status", body=patch_body
    )
