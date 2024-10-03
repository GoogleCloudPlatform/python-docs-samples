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

from vertexai.tuning import sft

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def list_tuning_jobs() -> List[sft.SupervisedTuningJob]:
    # [START generativeaionvertexai_list_tuning_jobs]
    import vertexai
    from vertexai.tuning import sft

    # TODO(developer): Update and un-comment below line
    # PROJECT_ID = "your-project-id"
    vertexai.init(project=PROJECT_ID, location="us-central1")

    responses = sft.SupervisedTuningJob.list()

    for response in responses:
        print(response)
    # Example response:
    # <vertexai.tuning._supervised_tuning.SupervisedTuningJob object at 0x7c85287b2680>
    # resource name: projects/12345678/locations/us-central1/tuningJobs/123456789012345

    # [END generativeaionvertexai_list_tuning_jobs]
    return responses


if __name__ == "__main__":
    list_tuning_jobs()
