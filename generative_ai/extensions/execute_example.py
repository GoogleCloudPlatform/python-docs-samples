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
import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def execute_extension(extension_id: str) -> object:
    # [START generativeaionvertexai_execute_extension]
    import vertexai
    from vertexai.preview import extensions

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # extension_id = "your-extension-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    extension = extensions.Extension(extension_id)

    response = extension.execute(
        operation_id="generate_and_execute",
        operation_params={"query": "find the max value in the list: [1,2,3,4,-5]"},
    )
    print(response)
    # Example response:
    # {
    #     "generated_code": "```python\n# Find the maximum value in the list\ndata = [1, 2,..", ..
    #     "execution_result": "The maximum value in the list is: 4\n",
    #     "execution_error": "",
    #     "output_files": [],
    # }

    # [END generativeaionvertexai_execute_extension]

    return response


if __name__ == "__main__":
    execute_extension("12345678901234567")
