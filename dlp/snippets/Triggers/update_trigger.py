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

"""Sample app that sets up Data Loss Prevention API automation triggers."""

import argparse


# [START dlp_update_trigger]
from typing import List

import google.cloud.dlp


def update_trigger(
    project: str,
    info_types: List[str],
    trigger_id: str,
) -> None:
    """Uses the Data Loss Prevention API to update an existing job trigger.
    Args:
        project: The Google Cloud project id to use as a parent resource
        info_types: A list of strings representing infoTypes to update trigger with.
            A full list of infoType categories can be fetched from the API.
        trigger_id: The id of job trigger which needs to be updated.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries.
    info_types = [{"name": info_type} for info_type in info_types]

    # Specify fields of the jobTrigger resource to be updated when the
    # job trigger is modified.
    job_trigger = {
        "inspect_job": {
            "inspect_config": {
                "info_types": info_types,
                "min_likelihood": google.cloud.dlp_v2.Likelihood.LIKELY,
            }
        }
    }

    # Convert the project id into a full resource id.
    trigger_name = f"projects/{project}/jobTriggers/{trigger_id}"

    # Call the API.
    # Refer https://protobuf.dev/reference/protobuf/google.protobuf/#field-mask
    # for constructing the field mask paths.
    response = dlp.update_job_trigger(
        request={
            "name": trigger_name,
            "job_trigger": job_trigger,
            "update_mask": {
                "paths": [
                    "inspect_job.inspect_config.info_types",
                    "inspect_job.inspect_config.min_likelihood",
                ]
            },
        }
    )

    # Print out the result.
    print(f"Successfully updated trigger: {response.name}")
    print(
        f"Updated InfoType: {response.inspect_job.inspect_config.info_types[0].name}"
        f" \nUpdates Likelihood: {response.inspect_job.inspect_config.min_likelihood}\n",
    )


# [END dlp_update_trigger]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("trigger_id", help="The id of the trigger to delete.")
    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". ',
    )

    args = parser.parse_args()
    update_trigger(
        args.project,
        args.info_types,
        args.trigger_id,
    )
