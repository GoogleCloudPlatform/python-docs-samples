# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import uuid

import google.auth
import google.auth.transport.requests
from google.cloud.functions_v2 import FunctionServiceClient
from google.iam.v1 import iam_policy_pb2, policy_pb2
import google.oauth2.id_token
import pytest
import requests

from deploy_function import (
    create_and_upload_function,
    create_cloud_function,
    delete_bucket,
    delete_function,
)


def test_create_cloud_function(capsys: "pytest.CaptureFixture[str]"):
    PROJECT = google.auth.default()[1]
    BUCKET_NAME = f"samples-functions-test-bucket-{uuid.uuid4().hex[:10]}"
    FOLDER_NAME = f"samples-functions-test-folder-{uuid.uuid4().hex[:10]}"
    FILE_NAME = "my_function.zip"
    object_name = f"{FOLDER_NAME}/{FILE_NAME}"
    function_id = f"test-function-{uuid.uuid4()}"
    RUNTIME = "python310"
    LOCATION_ID = "us-central1"
    resource_name = (
        f"projects/{PROJECT}/locations/{LOCATION_ID}/functions/{function_id}"
    )

    try:
        create_and_upload_function(BUCKET_NAME, object_name)
        create_cloud_function(
            project_id=PROJECT,
            bucket_name=BUCKET_NAME,
            location_id=LOCATION_ID,
            function_id=function_id,
            entry_point="my_function_entry",
            function_archive=object_name,
            runtime=RUNTIME,
        )

        client = FunctionServiceClient()

        get_policy_request = iam_policy_pb2.GetIamPolicyRequest(resource=resource_name)
        current_policy = client.get_iam_policy(request=get_policy_request)

        new_binding = policy_pb2.Binding(
            role="roles/cloudfunctions.invoker", members=["allUsers"]
        )
        current_policy.bindings.append(new_binding)

        set_policy_request = iam_policy_pb2.SetIamPolicyRequest(
            resource=resource_name, policy=current_policy
        )
        client.set_iam_policy(request=set_policy_request)

        function_url = (
            f"https://{LOCATION_ID}-{PROJECT}.cloudfunctions.net/{function_id}"
        )
        response = requests.get(function_url)

        assert response.status_code == 200
        assert response.text == "ok"
    finally:
        delete_function(PROJECT, LOCATION_ID, function_id)
        delete_bucket(PROJECT, BUCKET_NAME)
