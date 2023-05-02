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

from __future__ import print_function

import argparse
from typing import List


# [START dlp_list_jobs]
def list_dlp_jobs(project, filter_string=None, job_type=None):
    """Uses the Data Loss Prevention API to lists DLP jobs that match the
        specified filter in the request.
    Args:
        project: The project id to use as a parent resource.
        filter: (Optional) Allows filtering.
            Supported syntax:
            * Filter expressions are made up of one or more restrictions.
            * Restrictions can be combined by 'AND' or 'OR' logical operators.
            A sequence of restrictions implicitly uses 'AND'.
            * A restriction has the form of '<field> <operator> <value>'.
            * Supported fields/values for inspect jobs:
                - `state` - PENDING|RUNNING|CANCELED|FINISHED|FAILED
                - `inspected_storage` - DATASTORE|CLOUD_STORAGE|BIGQUERY
                - `trigger_name` - The resource name of the trigger that
                                   created job.
            * Supported fields for risk analysis jobs:
                - `state` - RUNNING|CANCELED|FINISHED|FAILED
            * The operator must be '=' or '!='.
            Examples:
            * inspected_storage = cloud_storage AND state = done
            * inspected_storage = cloud_storage OR inspected_storage = bigquery
            * inspected_storage = cloud_storage AND
                                  (state = done OR state = canceled)
        type: (Optional) The type of job. Defaults to 'INSPECT'.
            Choices:
            DLP_JOB_TYPE_UNSPECIFIED
            INSPECT_JOB: The job inspected content for sensitive data.
            RISK_ANALYSIS_JOB: The job executed a Risk Analysis computation.

    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library.
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Job type dictionary
    job_type_to_int = {
        "DLP_JOB_TYPE_UNSPECIFIED": google.cloud.dlp.DlpJobType.DLP_JOB_TYPE_UNSPECIFIED,
        "INSPECT_JOB": google.cloud.dlp.DlpJobType.INSPECT_JOB,
        "RISK_ANALYSIS_JOB": google.cloud.dlp.DlpJobType.RISK_ANALYSIS_JOB,
    }
    # If job type is specified, convert job type to number through enums.
    if job_type:
        job_type = job_type_to_int[job_type]

    # Call the API to get a list of jobs.
    response = dlp.list_dlp_jobs(
        request={"parent": parent, "filter": filter_string, "type_": job_type}
    )

    # Iterate over results.
    for job in response:
        print("Job: %s; status: %s" % (job.name, job.state.name))


# [END dlp_list_jobs]


# [START dlp_delete_job]
def delete_dlp_job(project, job_name):
    """Uses the Data Loss Prevention API to delete a long-running DLP job.
    Args:
        project: The project id to use as a parent resource.
        job_name: The name of the DlpJob resource to be deleted.

    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library.
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id and job name into a full resource id.
    name = f"projects/{project}/dlpJobs/{job_name}"

    # Call the API to delete job.
    dlp.delete_dlp_job(request={"name": name})

    print("Successfully deleted %s" % job_name)


# [END dlp_delete_job]


# [START dlp_create_job]
def create_dlp_job(
    project: str,
    bucket: str,
    info_types: List[str],
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
    # Import the client library
    import google.cloud.dlp

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
    url = "gs://{}/*".format(bucket)
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
        request={
            "parent": parent,
            "inspect_job": job,
            "job_id": job_id
        }
    )

    # Print out the result.
    print("Job : {} status: {}".format(response.name, response.state))

# [END dlp_create_job]


# [START dlp_get_job]
def get_dlp_job(
    project: str,
    job_name: str
) -> None:
    """Uses the Data Loss Prevention API to retrieve a DLP job.
    Args:
        project: The project id to use as a parent resource.
        job_name: The name of the DlpJob resource to be retrieved.
    """
    # Import the client library
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Convert the project id and job name into a full resource id.
    job_name = f"projects/{project}/dlpJobs/{job_name}"

    # Call the API
    response = dlp.get_dlp_job(request={
        "name": job_name
    })

    print(f"Job: {response.name} Status: {response.state}")

# [END dlp_get_job]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(
        dest="content", help="Select how to submit content to the API."
    )
    subparsers.required = True

    list_parser = subparsers.add_parser(
        "list",
        help="List Data Loss Prevention API jobs corresponding to a given " "filter.",
    )
    list_parser.add_argument(
        "project", help="The project id to use as a parent resource."
    )
    list_parser.add_argument(
        "-f",
        "--filter",
        help="Filter expressions are made up of one or more restrictions.",
    )
    list_parser.add_argument(
        "-t",
        "--type",
        choices=["DLP_JOB_TYPE_UNSPECIFIED", "INSPECT_JOB", "RISK_ANALYSIS_JOB"],
        help='The type of job. API defaults to "INSPECT"',
    )

    delete_parser = subparsers.add_parser(
        "delete", help="Delete results of a Data Loss Prevention API job."
    )
    delete_parser.add_argument(
        "project", help="The project id to use as a parent resource."
    )
    delete_parser.add_argument(
        "job_name",
        help="The name of the DlpJob resource to be deleted. " "Example: X-#####",
    )

    create_parser = subparsers.add_parser(
        "create", help="Create a Data Loss Prevention API job."
    )
    create_parser.add_argument(
        "project", help="The project id to use as a parent resource."
    )
    create_parser.add_argument(
        "bucket",
        help="The name of the GCS bucket to scan. This sample scans all files "
        "in the bucket."
    )
    create_parser.add_argument(
        "--info_types",
        nargs="+",
        help="Strings representing info types to look for. A full list of "
             "info categories and types is available from the API. Examples "
             'include "FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS". '
    )
    create_parser.add_argument(
        "--job_id",
        help="The id of the job. If omitted, an id will be randomly generated."
    )
    create_parser.add_argument(
        "--max_findings",
        type=int,
        help="The maximum number of findings to report; 0 = no maximum.",
    )
    create_parser.add_argument(
        "--auto_populate_timespan",
        type=bool,
        help="Limit scan to new content only.",
    )

    get_parser = subparsers.add_parser(
        "get", help="Get a Data Loss Prevention API job."
    )
    get_parser.add_argument(
        "project", help="The project id to use as a parent resource."
    )
    get_parser.add_argument(
        "job_name",
        help="The name of the DlpJob resource to be retrieved. " "Example: X-#####",
    )

    args = parser.parse_args()

    if args.content == "list":
        list_dlp_jobs(args.project, filter_string=args.filter, job_type=args.type)
    elif args.content == "delete":
        delete_dlp_job(args.project, args.job_name)
    elif args.content == "create":
        create_dlp_job(
            args.project,
            args.bucket,
            args.info_types,
            job_id=args.job_id,
            max_findings=args.max_findings,
            auto_populate_timespan=args.auto_populate_timespan,
        )
    elif args.content == "get":
        get_dlp_job(args.project, args.job_name)
