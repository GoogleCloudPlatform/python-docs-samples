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


def generate_content(PROJECT_ID: str, EXTENSION_ID: str) -> str:
    # [START generativeaionvertexai_delete_extension]
    import vertexai
    from vertexai.preview import extensions

    vertexai.init(project=PROJECT_ID)

    extension_code_interpreter = extensions.Extension(EXTENSION_ID)
    delete_response = extension_code_interpreter.delete()
    # [END generativeaionvertexai_delete_extension]

    return str(delete_response)
