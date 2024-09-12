# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# TODO: Delete this file after aproving /extensions folder
import os

from typing import List

from vertexai.preview import extensions

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def create_extension() -> extensions.Extension:
    # [START generativeaionvertexai_create_extension]
    import vertexai
    from vertexai.preview import extensions

    # TODO (developer): update project_id
    vertexai.init(project=PROJECT_ID, location="us-central1")

    extension = extensions.Extension.create(
        display_name="Code Interpreter",
        description="This extension generates and executes code in the specified language",
        manifest={
            "name": "code_interpreter_tool",
            "description": "Google Code Interpreter Extension",
            "api_spec": {
                "open_api_gcs_uri": "gs://vertex-extension-public/code_interpreter.yaml"
            },
            "auth_config": {
                "google_service_account_config": {},
                "auth_type": "GOOGLE_SERVICE_ACCOUNT_AUTH",
            },
        },
    )
    # [END generativeaionvertexai_create_extension]

    return extension


def execute_extension(extension_id: str) -> object:
    # [START generativeaionvertexai_execute_extension]
    import vertexai
    from vertexai.preview import extensions

    # TODO (developer): update project_id
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # TODO(developer): Update and un-comment below line
    # extension_id = "EXTENSION_ID"
    extension = extensions.Extension(extension_id)
    response = extension.execute(
        operation_id="generate_and_execute",
        operation_params={"query": "find the max value in the list: [1,2,3,4,-5]"},
    )
    print(response)
    # [END generativeaionvertexai_execute_extension]

    return response


def get_extension(extension_id: str) -> extensions.Extension:
    # [START generativeaionvertexai_get_extension]
    import vertexai
    from vertexai.preview import extensions

    # TODO (developer): update project_id
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # TODO(developer): Update and un-comment below line
    # extension_id = "EXTENSION_ID"
    extension = extensions.Extension(extension_id)
    print(extension)
    # [END generativeaionvertexai_get_extension]
    return extension


def list_extensions() -> List[extensions.Extension]:
    # [START generativeaionvertexai_list_extensions]
    import vertexai
    from vertexai.preview import extensions

    # TODO (developer): update project_id
    vertexai.init(project=PROJECT_ID, location="us-central1")

    extensions = extensions.Extension.list()
    print(extensions)
    # [END generativeaionvertexai_list_extensions]
    return extensions


def delete_extension(extension_id: str) -> None:
    # [START generativeaionvertexai_delete_extension]
    import vertexai
    from vertexai.preview import extensions

    # TODO (developer): update project_id
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # TODO(developer): Update and un-comment below line
    # extension_id = "EXTENSION_ID"
    extension = extensions.Extension(extension_id)
    extension.delete()
    # [END generativeaionvertexai_delete_extension]


if __name__ == "__main__":
    list_extensions()
