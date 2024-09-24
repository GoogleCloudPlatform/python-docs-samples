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

from vertexai.tuning import sft

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"


def get_tuning_job() -> sft.SupervisedTuningJob:
    # [START generativeaionvertexai_get_tuning_job]
    import vertexai
    from vertexai.tuning import sft

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # LOCATION = "us-central1"
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    tuning_job_id = "4982013113894174720"
    response = sft.SupervisedTuningJob(
        f"projects/{PROJECT_ID}/locations/{LOCATION}/tuningJobs/{tuning_job_id}"
    )

    print(response)
    # Example response:
    # <vertexai.tuning._supervised_tuning.SupervisedTuningJob object at 0x7cc4bb20baf0>
    # resource name: projects/1234567890/locations/us-central1/tuningJobs/4982013113894174720

    # [END generativeaionvertexai_get_tuning_job]
    return response


if __name__ == "__main__":
    get_tuning_job()
