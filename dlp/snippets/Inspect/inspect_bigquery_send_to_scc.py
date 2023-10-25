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

# [START dlp_inspect_bigquery_send_to_scc]
import time
from typing import List

import google.cloud.dlp


def inspect_bigquery_send_to_scc(
    project: str,
    info_types: List[str],
    max_findings: int = 100,
) -> None:
    """
    Uses the Data Loss Prevention API to inspect public bigquery dataset
    and send the results to Google Security Command Center.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        info_types: A list of strings representing infoTypes to inspect for.
            A full list of infoType categories can be fetched from the API.
        max_findings: The maximum number of findings to report; 0 = no maximum
    """
    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries.
    info_types = [{"name": info_type} for info_type in info_types]

    # Construct the configuration dictionary.
    inspect_config = {
        "info_types": info_types,
        "min_likelihood": google.cloud.dlp_v2.Likelihood.UNLIKELY,
        "limits": {"max_findings_per_request": max_findings},
        "include_quote": True,
    }

    # Construct a Cloud Storage Options dictionary with the big query options.
    storage_config = {
        "big_query_options": {
            "table_reference": {
                "project_id": "bigquery-public-data",
                "dataset_id": "usa_names",
                "table_id": "usa_1910_current",
            }
        }
    }

    # Tell the API where to send a notification when the job is complete.
    actions = [{"publish_summary_to_cscc": {}}]

    # Construct the job definition.
    job = {
        "inspect_config": inspect_config,
        "storage_config": storage_config,
        "actions": actions,
    }

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.create_dlp_job(
        request={
            "parent": parent,
            "inspect_job": job,
        }
    )
    print(f"Inspection Job started : {response.name}")

    job_name = response.name

    # Waiting for a maximum of 15 minutes for the job to get complete.
    no_of_attempts = 30
    while no_of_attempts > 0:
        # Get the DLP job status.
        job = dlp.get_dlp_job(request={"name": job_name})
        # Check if the job has completed.
        if job.state == google.cloud.dlp_v2.DlpJob.JobState.DONE:
            break
        if job.state == google.cloud.dlp_v2.DlpJob.JobState.FAILED:
            print("Job Failed, Please check the configuration.")
            return

        # Sleep for a short duration before checking the job status again.
        time.sleep(30)
        no_of_attempts -= 1

    # Print out the results.
    print(f"Job name: {job.name}")
    result = job.inspect_details.result
    if result.info_type_stats:
        for stats in result.info_type_stats:
            print(f"Info type: {stats.info_type.name}")
            print(f"Count: {stats.count}")
    else:
        print("No findings.")


# [END dlp_inspect_bigquery_send_to_scc]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "--info_types",
        action="append",
        help="Strings representing infoTypes to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS".',
    )
    parser.add_argument(
        "--max_findings",
        type=int,
        help="The maximum number of findings to report; 0 = no maximum.",
    )

    args = parser.parse_args()

    inspect_bigquery_send_to_scc(
        args.project,
        args.info_types,
        args.max_findings,
    )
