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

    args = parser.parse_args()

    if args.content == "list":
        list_dlp_jobs(args.project, filter_string=args.filter, job_type=args.type)
    elif args.content == "delete":
        delete_dlp_job(args.project, args.job_name)
