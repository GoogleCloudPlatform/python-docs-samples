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
from typing import List


# [START dlp_create_trigger]
from typing import Optional

import google.cloud.dlp


def create_trigger(
    project: str,
    bucket: str,
    scan_period_days: int,
    info_types: List[str],
    trigger_id: Optional[str] = None,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
    min_likelihood: Optional[int] = None,
    max_findings: Optional[int] = None,
    auto_populate_timespan: Optional[bool] = False,
) -> None:
    """Creates a scheduled Data Loss Prevention API inspect_content trigger.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        bucket: The name of the GCS bucket to scan. This sample scans all
            files in the bucket using a wildcard.
        scan_period_days: How often to repeat the scan, in days.
            The minimum is 1 day.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        trigger_id: The id of the trigger. If omitted, an id will be randomly
            generated.
        display_name: The optional display name of the trigger.
        description: The optional description of the trigger.
        min_likelihood: A string representing the minimum likelihood threshold
            that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED',
            'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.
        max_findings: The maximum number of findings to report; 0 = no maximum.
        auto_populate_timespan: Automatically populates time span config start
            and end times in order to scan new content only.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries (protos are also accepted).
    info_types = [{"name": info_type} for info_type in info_types]

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    inspect_config = {
        "info_types": info_types,
        "min_likelihood": min_likelihood,
        "limits": {"max_findings_per_request": max_findings},
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

    # Construct the schedule definition:
    schedule = {
        "recurrence_period_duration": {"seconds": scan_period_days * 60 * 60 * 24}
    }

    # Construct the trigger definition.
    job_trigger = {
        "inspect_job": job,
        "display_name": display_name,
        "description": description,
        "triggers": [{"schedule": schedule}],
        "status": google.cloud.dlp_v2.JobTrigger.Status.HEALTHY,
    }

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.create_job_trigger(
        request={"parent": parent, "job_trigger": job_trigger, "trigger_id": trigger_id}
    )

    print(f"Successfully created trigger {response.name}")


# [END dlp_create_trigger]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "bucket", help="The name of the GCS bucket containing the file."
    )
    parser.add_argument(
        "scan_period_days",
        type=int,
        help="How often to repeat the scan, in days. The minimum is 1 day.",
    )
    parser.add_argument(
        "--trigger_id",
        help="The id of the trigger. If omitted, an id will be randomly " "generated",
    )
    parser.add_argument(
        "--display_name", help="The optional display name of the trigger."
    )
    parser.add_argument(
        "--description", help="The optional description of the trigger."
    )
    parser.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
    )
    parser.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    parser.add_argument(
        "--min_likelihood",
        choices=[
            "LIKELIHOOD_UNSPECIFIED",
            "VERY_UNLIKELY",
            "UNLIKELY",
            "POSSIBLE",
            "LIKELY",
            "VERY_LIKELY",
        ],
        help="A string representing the minimum likelihood threshold that "
        "constitutes a match.",
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

    create_trigger(
        args.project,
        args.bucket,
        args.scan_period_days,
        args.info_types,
        trigger_id=args.trigger_id,
        display_name=args.display_name,
        description=args.description,
        min_likelihood=args.min_likelihood,
        max_findings=args.max_findings,
        auto_populate_timespan=args.auto_populate_timespan,
    )
