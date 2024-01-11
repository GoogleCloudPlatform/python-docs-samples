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


# [START dlp_create_job]

import google.cloud.dlp


def create_dlp_job(
    project: str,
    bucket: str,
    info_types: list[str],
    job_id: str = None,
    max_findings: int = 100,
    auto_populate_timespan: bool = True,
) -> None:
    """Uses the Data Loss Prevention API to create a DLP job.
    Args:
        project: The project id to use as a parent resource.
        bucket: The name of the GCS bucket to scan. This sample scans all
            files in the bucket.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        job_id: The id of the job. If omitted, an id will be randomly generated.
        max_findings: The maximum number of findings to report; 0 = no maximum.
        auto_populate_timespan: Automatically populates time span config start
            and end times in order to scan new content only.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries (protos are also accepted).
    info_types = [{"name": info_type} for info_type in info_types]

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    inspect_config = {
        "info_types": info_types,
        "min_likelihood": google.cloud.dlp_v2.Likelihood.UNLIKELY,
        "limits": {"max_findings_per_request": max_findings},
        "include_quote": True,
    }

    # Construct a cloud_storage_options dictionary with the bucket's URL.
    url = f"gs://{bucket}/*"
    storage_config = {
        "cloud_storage_options": {"file_set": {"url": url}},
        # Time-based configuration for each storage object.
        "timespan_config": {
            # Auto-populate start and end times in order to scan new objects
            # only.
            "enable_auto_population_of_timespan_config": auto_populate_timespan
        },
    }

    # Construct the job definition.
    job = {"inspect_config": inspect_config, "storage_config": storage_config}

    # Call the API.
    response = dlp.create_dlp_job(
        request={"parent": parent, "inspect_job": job, "job_id": job_id}
    )

    # Print out the result.
    print(f"Job : {response.name} status: {response.state}")


# [END dlp_create_job]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("project", help="The project id to use as a parent resource.")
    parser.add_argument(
        "bucket",
        help="The name of the GCS bucket to scan. This sample scans all files "
        "in the bucket.",
    )
    parser.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". ',
    )
    parser.add_argument(
        "--job_id",
        help="The id of the job. If omitted, an id will be randomly generated.",
    )
    parser.add_argument(
        "--max_findings",
        type=int,
        help="The maximum number of findings to report; 0 = no maximum.",
    )
    parser.add_argument(
        "--auto_populate_timespan",
        type=bool,
        help="Limit scan to new content only.",
    )

    args = parser.parse_args()

    create_dlp_job(
        args.project,
        args.bucket,
        args.info_types,
        job_id=args.job_id,
        max_findings=args.max_findings,
        auto_populate_timespan=args.auto_populate_timespan,
    )
