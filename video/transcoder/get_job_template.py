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

"""Google Cloud Transcoder sample for getting a job template.

Example usage:
    python get_job_template.py --project_id <project-id> --location <location> --template_id <template-id>
"""

# [START transcoder_get_job_template]

import argparse

from google.cloud.video.transcoder_v1.services.transcoder_service import (
    TranscoderServiceClient,
)


def get_job_template(project_id, location, template_id):
    """Gets a job template.

    Args:
        project_id: The GCP project ID.
        location: The location of the template.
        template_id: The user-defined template ID."""

    client = TranscoderServiceClient()

    name = f"projects/{project_id}/locations/{location}/jobTemplates/{template_id}"
    response = client.get_job_template(name=name)
    print(f"Job template: {response.name}")
    return response


# [END transcoder_get_job_template]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location", help="The location of the template.", required=True
    )
    parser.add_argument("--template_id", help="The job template ID.", required=True)
    args = parser.parse_args()
    get_job_template(args.project_id, args.location, args.template_id)
