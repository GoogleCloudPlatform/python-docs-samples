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

"""Sample app that uses the Data Loss Prevention API to inspect a string, a
local file or a file on Google Cloud Storage."""


import argparse

# [START dlp_inspect_send_data_to_hybrid_job_trigger]
import time

import google.cloud.dlp


def inspect_data_to_hybrid_job_trigger(
    project: str,
    trigger_id: str,
    content_string: str,
) -> None:
    """
    Uses the Data Loss Prevention API to inspect sensitive information
    using Hybrid jobs trigger that scans payloads of data sent from
    virtually any source and stores findings in Google Cloud.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        trigger_id: The job trigger identifier for hybrid job trigger.
        content_string: The string to inspect.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Construct the `item` to inspect.
    item = {"value": content_string}

    # Construct the container details that contains metadata to be
    # associated with the content. For more details, please refer to
    # https://cloud.google.com/dlp/docs/reference/rest/v2/Container
    container_details = {
        "full_path": "10.0.0.2:logs1:app1",
        "relative_path": "app1",
        "root_path": "10.0.0.2:logs1",
        "type_": "logging_sys",
        "version": "1.2",
    }

    # Construct hybrid inspection configuration.
    hybrid_config = {
        "item": item,
        "finding_details": {
            "container_details": container_details,
            "labels": {
                "env": "prod",
                "appointment-bookings-comments": "",
            },
        },
    }

    # Convert the trigger id into a full resource id.
    trigger_id = f"projects/{project}/jobTriggers/{trigger_id}"

    # Activate the job trigger.
    dlp_job = dlp.activate_job_trigger(request={"name": trigger_id})

    # Call the API.
    dlp.hybrid_inspect_job_trigger(
        request={
            "name": trigger_id,
            "hybrid_item": hybrid_config,
        }
    )

    # Get inspection job details.
    job = dlp.get_dlp_job(request={"name": dlp_job.name})

    # Wait for dlp job to get finished.
    while job.inspect_details.result.processed_bytes <= 0:
        time.sleep(5)
        job = dlp.get_dlp_job(request={"name": dlp_job.name})

    # Print the results.
    print(f"Job name: {dlp_job.name}")
    if job.inspect_details.result.info_type_stats:
        for finding in job.inspect_details.result.info_type_stats:
            print(f"Info type: {finding.info_type.name}; Count: {finding.count}")
    else:
        print("No findings.")


# [END dlp_inspect_send_data_to_hybrid_job_trigger]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "--trigger_id",
        help="The job trigger identifier for hybrid job trigger.",
    )
    parser.add_argument("content_string", help="The string to inspect.")

    args = parser.parse_args()

    inspect_data_to_hybrid_job_trigger(
        args.project,
        args.trigger_id,
        args.content_string,
    )
