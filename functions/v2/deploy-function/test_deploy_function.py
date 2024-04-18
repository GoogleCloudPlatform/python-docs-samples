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


import os
import uuid

import pytest
from google.cloud.functions_v2 import FunctionServiceClient

from deploy_function import create_cloud_function, create_and_upload_function

from google.cloud.functions_v2.types import ListFunctionsRequest


def test_create_cloud_function(capsys: "pytest.CaptureFixture[str]"):
    PROJECT_ID = os.environ["IAM_PROJECT_ID"]
    BUCKET_NAME = "samples-functions-test-practice-bucket-111"
    FOLDER_NAME = "samples-functions-test-practice-folder-111"
    FILE_NAME = "my_function.zip"
    object_name = f"{FOLDER_NAME}/{FILE_NAME}"
    function_id = f"test-function-{uuid.uuid4()}"
    RUNTIME = "python310"
    LOCATION_ID = "us-central1"

    create_and_upload_function(BUCKET_NAME, object_name)

    create_cloud_function(
        project_id=PROJECT_ID,
        bucket_name=BUCKET_NAME,
        location_id=LOCATION_ID,
        function_id=function_id,
        entry_point="my_function_entry",
        function_archive=object_name,
        runtime=RUNTIME,
    )

    client = FunctionServiceClient()
    parent = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}"
    request = ListFunctionsRequest(parent=parent)
    functions = list(client.list_functions(request=request))
    assert any(f.name == f"{parent}/functions/{function_id}" for f in functions)
