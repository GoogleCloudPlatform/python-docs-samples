# Copyright 2025 Google LLC
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


def list_tuning_jobs() -> None:
    # [START googlegenaisdk_tuning_job_list]
    from google import genai
    from google.genai.types import HttpOptions

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    responses = client.tunings.list()
    for response in responses:
        print(response.name)
        # Example response:
        # projects/123456789012/locations/us-central1/tuningJobs/123456789012345

    # [END googlegenaisdk_tuning_job_list]
    return


if __name__ == "__main__":
    tuning_job_name = input("Tuning job name: ")
    list_tuning_jobs()
