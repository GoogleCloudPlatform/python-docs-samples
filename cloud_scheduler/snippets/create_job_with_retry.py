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

# [START cloudscheduler_create_job_with_retry]
import datetime
import sys

from google.api_core import exceptions
from google.cloud import scheduler_v1


def create_job_with_retry(
    project_id: str,
    location_id: str,
    job_id: str,
    service_url: str,
    service_account_email: str,
) -> None:
    """Creates a job that retries failed calls to a Cloud Run service.

    Args:
        project_id: The Google Cloud project ID (for example, 'example-project-id').
        location_id: The region for the job (for example, 'us-central1').
        job_id: The ID for the new job (for example, 'example-job-id').
        service_url: The HTTPS URL of the Cloud Run service to call.
        service_account_email: The service account that the job uses to get an
            OIDC token. It needs the Cloud Run Invoker role on the service.
    """
    client = scheduler_v1.CloudSchedulerClient()
    parent = f"projects/{project_id}/locations/{location_id}"

    oidc_token = scheduler_v1.OidcToken(
        service_account_email=service_account_email,
        audience=service_url,
    )
    http_target = scheduler_v1.HttpTarget(
        uri=service_url,
        http_method=scheduler_v1.HttpMethod.POST,
        body=b"example-payload",
        oidc_token=oidc_token,
    )
    # Cloud Scheduler stops retrying a run when it reaches either limit:
    # retry_count retries or max_retry_duration since the first attempt.
    # The wait between retries starts at min_backoff_duration, doubles
    # max_doublings times, and then grows linearly up to max_backoff_duration.
    retry_config = scheduler_v1.RetryConfig(
        retry_count=3,
        max_retry_duration=datetime.timedelta(hours=1),
        min_backoff_duration=datetime.timedelta(seconds=10),
        max_backoff_duration=datetime.timedelta(minutes=5),
        max_doublings=3,
    )
    job = scheduler_v1.Job(
        name=f"{parent}/jobs/{job_id}",
        http_target=http_target,
        retry_config=retry_config,
        # Runs every Monday at 09:00. UTC avoids skipped or repeated runs when
        # daylight saving time starts or ends.
        schedule="0 9 * * 1",
        time_zone="UTC",
        # A response that misses this deadline counts as a failed attempt and
        # is retried, so match it to the service's request timeout.
        attempt_deadline=datetime.timedelta(minutes=5),
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
        print(f"Max Retry Duration: {response.retry_config.max_retry_duration}")
        print(f"Retry Count: {response.retry_config.retry_count}")
        print(f"State: {response.state.name}")


# [END cloudscheduler_create_job_with_retry]


if __name__ == "__main__":
    import argparse
    import os

    # Each flag defaults to its environment variable, then to an example value.
    parser = argparse.ArgumentParser(
        description=create_job_with_retry.__doc__.splitlines()[0]
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
        "--service-url",
        default=os.environ.get("SERVICE_URL", "https://example-service.a.run.app/"),
        help="HTTPS URL of the Cloud Run service to call (default: $SERVICE_URL)",
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

    create_job_with_retry(
        project_id=args.project_id,
        location_id=args.location_id,
        job_id=args.job_id,
        service_url=args.service_url,
        service_account_email=args.service_account_email,
    )
