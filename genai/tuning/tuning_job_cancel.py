# Copyright 2026 Google LLC
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

# [START googlegenaisdk_tuning_job_cancel]

from google import genai
from google.genai.types import HttpOptions
def cancel_tuning_job(tuning_job_name: str) -> None:

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    # Cancel the tuning job.
    # Eg. tuning_job_name = "projects/123456789012/locations/us-central1/tuningJobs/123456789012345"
    client.tunings.cancel(name=tuning_job_name)

    # [END googlegenaisdk_tuning_job_cancel]