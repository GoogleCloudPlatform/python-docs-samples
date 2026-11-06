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

    # Use an OAuth token, not an OIDC token, when the target is a Google API
    # hosted on *.googleapis.com.
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
        # Runs every Monday at 09:00. UTC avoids skipped or repeated runs when
        # daylight saving time starts or ends.
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
    import os

    def arg(index: int, env_var: str, default: str) -> str:
        """Reads an environment variable, then a CLI argument, then a default."""
        cli_value = sys.argv[index] if len(sys.argv) > index else None
        return os.environ.get(env_var) or cli_value or default

    create_http_job_oauth(
        project_id=arg(1, "GOOGLE_CLOUD_PROJECT", "example-project-id"),
        location_id=arg(2, "GOOGLE_CLOUD_LOCATION", "us-central1"),
        job_id=arg(3, "SCHEDULER_JOB_ID", "example-job-id"),
        workflow_template_id=arg(
            4, "WORKFLOW_TEMPLATE_ID", "example-workflow-template"
        ),
        service_account_email=arg(
            5,
            "SERVICE_ACCOUNT_EMAIL",
            "example-invoker@example-project-id.iam.gserviceaccount.com",
        ),
    )
