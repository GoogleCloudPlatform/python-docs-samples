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


def generate_content(PROJECT_ID: str, REGION: str, EXTENSION_ID: str) -> object:
    # [START generativeaionvertexai_execute_extension]
    import vertexai
    from vertexai.preview import extensions

    vertexai.init(project=PROJECT_ID, location=REGION)

    code_interpreter_extensions = extensions.Extension(EXTENSION_ID)
    response = code_interpreter_extensions.execute(
        operation_id = "generate_and_execute",
        operation_params = {"query": "find the max value in the list: [1,2,3,4,-5]"},
    )
    # [END generativeaionvertexai_execute_extension]
    return response