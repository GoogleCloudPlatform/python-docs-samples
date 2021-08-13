#!/usr/bin/env python

# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Transcoder sample for creating a job based on a job preset.

Example usage:
    python create_job_from_preset.py --project_id <project-id> --location <location> --input_uri <uri> --output_uri <uri> [--preset <preset>]
"""

# [START transcoder_create_job_from_preset]

import argparse

from google.cloud.video import transcoder_v1
from google.cloud.video.transcoder_v1.services.transcoder_service import (
    TranscoderServiceClient,
)


def create_job_from_preset(project_id, location, input_uri, output_uri, preset):
    """Creates a job based on a job preset.

    Args:
        project_id: The GCP project ID.
        location: The location to start the job in.
        input_uri: Uri of the video in the Cloud Storage bucket.
        output_uri: Uri of the video output folder in the Cloud Storage bucket.
        preset: The preset template."""

    client = TranscoderServiceClient()

    parent = f"projects/{project_id}/locations/{location}"
    job = transcoder_v1.types.Job()
    job.input_uri = input_uri
    job.output_uri = output_uri
    job.template_id = preset

    response = client.create_job(parent=parent, job=job)
    print(f"Job: {response.name}")
    return response


# [END transcoder_create_job_from_preset]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location to start this job in.",
        default="us-central1",
    )
    parser.add_argument(
        "--input_uri",
        help="Uri of the video in the Cloud Storage bucket.",
        required=True,
    )
    parser.add_argument(
        "--output_uri",
        help="Uri of the video output folder in the Cloud Storage bucket. Must end in '/'.",
        required=True,
    )
    parser.add_argument(
        "--preset",
        help="The preset template.",
        default="preset/web-hd",
    )
    args = parser.parse_args()
    create_job_from_preset(
        args.project_id,
        args.location,
        args.input_uri,
        args.output_uri,
        args.preset,
    )
