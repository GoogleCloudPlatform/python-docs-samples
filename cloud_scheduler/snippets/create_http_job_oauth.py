# Copyright 2026 Google LLC
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

# [START cloudscheduler_create_http_job_oauth]
import sys

from google.api_core import exceptions
from google.cloud import scheduler_v1


def create_http_job_oauth(
    project_id: str,
    location_id: str,
    job_id: str,
    workflow_template_id: str,
    service_account_email: str,
) -> None:
    """Creates a job that starts a Managed Spark workflow template on a schedule.

    The job calls the Dataproc API directly, authenticating with an OAuth
    access token for a service account.

    Args:
        project_id: The Google Cloud project ID (for example, 'example-project-id').
        location_id: The region of the job and the workflow template (for
            example, 'us-central1').
        job_id: The ID for the new job (for example, 'example-job-id').
        workflow_template_id: The ID of the workflow template to start (for
            example, 'example-workflow-template').
        service_account_email: The service account that the job uses to get an
            OAuth token. It needs permission to start the workflow template.
    """
    client = scheduler_v1.CloudSchedulerClient()
    parent = f"projects/{project_id}/locations/{location_id}"
    template_name = (
        f"projects/{project_id}/regions/{location_id}"
        f"/workflowTemplates/{workflow_template_id}"
    )

    # Google APIs (*.googleapis.com) need an OAuth token, not OIDC.
    oauth_token = scheduler_v1.OAuthToken(
        service_account_email=service_account_email,
        scope="https://www.googleapis.com/auth/cloud-platform",
    )
    http_target = scheduler_v1.HttpTarget(
        uri=f"https://dataproc.googleapis.com/v1/{template_name}:instantiate",
        http_method=scheduler_v1.HttpMethod.POST,
        headers={"Content-Type": "application/json"},
        body=b"{}",
        oauth_token=oauth_token,
    )
    job = scheduler_v1.Job(
        name=f"{parent}/jobs/{job_id}",
        http_target=http_target,
        # Every Monday at 09:00 UTC, which has no daylight saving shifts.
        schedule="0 9 * * 1",
        time_zone="UTC",
    )
    request = scheduler_v1.CreateJobRequest(parent=parent, job=job)

    try:
        response = client.create_job(request=request)
    except exceptions.AlreadyExists as err:
        print(
            f"error: job '{job_id}' already exists in location '{location_id}' "
            f"for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to create job '{job_id}' in location '{location_id}' "
            f"for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {response.name}")
        print(f"Schedule: {response.schedule}")
        print(f"State: {response.state.name}")
        print(f"Target URI: {response.http_target.uri}")


# [END cloudscheduler_create_http_job_oauth]


if __name__ == "__main__":
    import argparse
    import os

    # Each flag defaults to its environment variable, then to an example value.
    parser = argparse.ArgumentParser(
        description=create_http_job_oauth.__doc__.splitlines()[0]
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
        help="Google Cloud project ID (default: $GOOGLE_CLOUD_PROJECT)",
    )
    parser.add_argument(
        "--location-id",
        default=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
        help="Region of the job (default: $GOOGLE_CLOUD_LOCATION)",
    )
    parser.add_argument(
        "--job-id",
        default=os.environ.get("SCHEDULER_JOB_ID", "example-job-id"),
        help="ID of the job (default: $SCHEDULER_JOB_ID)",
    )
    parser.add_argument(
        "--workflow-template-id",
        default=os.environ.get("WORKFLOW_TEMPLATE_ID", "example-workflow-template"),
        help="ID of the workflow template to start (default: $WORKFLOW_TEMPLATE_ID)",
    )
    parser.add_argument(
        "--service-account-email",
        default=os.environ.get(
            "SERVICE_ACCOUNT_EMAIL",
            "example-invoker@example-project-id.iam.gserviceaccount.com",
        ),
        help="Service account that the job uses to get tokens (default: $SERVICE_ACCOUNT_EMAIL)",
    )
    args = parser.parse_args()

    create_http_job_oauth(
        project_id=args.project_id,
        location_id=args.location_id,
        job_id=args.job_id,
        workflow_template_id=args.workflow_template_id,
        service_account_email=args.service_account_email,
    )
