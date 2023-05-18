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
import os


# [START dlp_create_trigger]
def create_trigger(
    project,
    bucket,
    scan_period_days,
    info_types,
    trigger_id=None,
    display_name=None,
    description=None,
    min_likelihood=None,
    max_findings=None,
    auto_populate_timespan=False,
):
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

    # Import the client library
    import google.cloud.dlp

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


# [START dlp_list_triggers]
def list_triggers(project):
    """Lists all Data Loss Prevention API triggers.
    Args:
        project: The Google Cloud project id to use as a parent resource.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.list_job_triggers(request={"parent": parent})

    for trigger in response:
        print(f"Trigger {trigger.name}:")
        print(f"  Created: {trigger.create_time}")
        print(f"  Updated: {trigger.update_time}")
        if trigger.display_name:
            print(f"  Display Name: {trigger.display_name}")
        if trigger.description:
            print(f"  Description: {trigger.discription}")
        print(f"  Status: {trigger.status}")
        print(f"  Error count: {len(trigger.errors)}")


# [END dlp_list_triggers]


# [START dlp_delete_trigger]
def delete_trigger(project, trigger_id):
    """Deletes a Data Loss Prevention API trigger.
    Args:
        project: The id of the Google Cloud project which owns the trigger.
        trigger_id: The id of the trigger to delete.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Combine the trigger id with the parent id.
    trigger_resource = f"{parent}/jobTriggers/{trigger_id}"

    # Call the API.
    dlp.delete_job_trigger(request={"name": trigger_resource})

    print(f"Trigger {trigger_resource} successfully deleted.")


# [END dlp_delete_trigger]


if __name__ == "__main__":
    default_project = os.environ.get("GOOGLE_CLOUD_PROJECT")

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(
        dest="action", help="Select which action to perform."
    )
    subparsers.required = True

    parser_create = subparsers.add_parser("create", help="Create a trigger.")
    parser_create.add_argument(
        "bucket", help="The name of the GCS bucket containing the file."
    )
    parser_create.add_argument(
        "scan_period_days",
        type=int,
        help="How often to repeat the scan, in days. The minimum is 1 day.",
    )
    parser_create.add_argument(
        "--trigger_id",
        help="The id of the trigger. If omitted, an id will be randomly " "generated",
    )
    parser_create.add_argument(
        "--display_name", help="The optional display name of the trigger."
    )
    parser_create.add_argument(
        "--description", help="The optional description of the trigger."
    )
    parser_create.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
        default=default_project,
    )
    parser_create.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
        "info categories and types is available from the API. Examples "
        'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
        "If unspecified, the three above examples will be used.",
        default=["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"],
    )
    parser_create.add_argument(
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
    parser_create.add_argument(
        "--max_findings",
        type=int,
        help="The maximum number of findings to report; 0 = no maximum.",
    )
    parser_create.add_argument(
        "--auto_populate_timespan",
        type=bool,
        help="Limit scan to new content only.",
    )

    parser_list = subparsers.add_parser("list", help="List all triggers.")
    parser_list.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
        default=default_project,
    )

    parser_delete = subparsers.add_parser("delete", help="Delete a trigger.")
    parser_delete.add_argument("trigger_id", help="The id of the trigger to delete.")
    parser_delete.add_argument(
        "--project",
        help="The Google Cloud project id to use as a parent resource.",
        default=default_project,
    )

    args = parser.parse_args()

    if args.action == "create":
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
    elif args.action == "list":
        list_triggers(args.project)
    elif args.action == "delete":
        delete_trigger(args.project, args.trigger_id)
