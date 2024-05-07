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


def generate_content(PROJECT_ID: str, REGION: str) -> object:
    # [START generativeaionvertexai_extension_basic]
    import vertexai
    from vertexai.preview import extensions

    vertexai.init(project=PROJECT_ID,location=REGION)

    extension_code_interpreter = extensions.Extension.create(
        display_name = "Code Interpreter",
        description = "This extension generates and executes code in the specified language",
        manifest = {
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
    # [END generativeaionvertexai_extension_basic]
    return extension_code_interpreter