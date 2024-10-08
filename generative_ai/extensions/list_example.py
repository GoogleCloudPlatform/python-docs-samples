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

from typing import List

from vertexai.preview import extensions

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def list_extensions() -> List[extensions.Extension]:
    # [START generativeaionvertexai_list_extensions]
    import vertexai
    from vertexai.preview import extensions

    # TODO (developer):Update project_id
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    extensions_list = extensions.Extension.list()
    print(extensions_list)
    # Example response:
    # [<vertexai.extensions._extensions.Extension object at 0x76e8ced37af0>
    # resource name: projects/[PROJECT_ID]/locations/us-central1/extensions/1234567890123456]

    # [END generativeaionvertexai_list_extensions]
    return extensions_list


if __name__ == "__main__":
    list_extensions()
