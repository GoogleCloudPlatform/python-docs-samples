# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Sample app to list and delete DLP jobs using the Data Loss Prevent API. """

from __future__ import annotations

import argparse


# [START dlp_get_job]

import google.cloud.dlp


def get_dlp_job(project: str, job_name: str) -> None:
    """Uses the Data Loss Prevention API to retrieve a DLP job.
    Args:
        project: The project id to use as a parent resource.
        job_name: The name of the DlpJob resource to be retrieved.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id and job name into a full resource id.
    job_name = f"projects/{project}/locations/global/dlpJobs/{job_name}"

    # Call the API
    response = dlp.get_dlp_job(request={"name": job_name})

    print(f"Job: {response.name} Status: {response.state}")


# [END dlp_get_job]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="The project id to use as a parent resource.")
    parser.add_argument(
        "job_name",
        help="The name of the DlpJob resource to be retrieved. " "Example: X-#####",
    )

    args = parser.parse_args()

    get_dlp_job(args.project, args.job_name)
