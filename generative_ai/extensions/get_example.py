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

from vertexai.preview import extensions

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def get_extension(extension_id: str) -> extensions.Extension:
    # [START generativeaionvertexai_get_extension]
    import vertexai
    from vertexai.preview import extensions

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # extension_id = "your-extension-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    extension = extensions.Extension(extension_id)
    print(extension.resource_name)
    # Example response:
    # projects/[PROJECT_ID]/locations/us-central1/extensions/12345678901234567

    # [END generativeaionvertexai_get_extension]
    return extension


if __name__ == "__main__":
    get_extension("12345678901234567")
