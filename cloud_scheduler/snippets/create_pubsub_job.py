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

# [START cloudscheduler_create_pubsub_job]
import sys

from google.api_core import exceptions
from google.cloud import scheduler_v1


def create_pubsub_job(
    project_id: str, location_id: str, job_id: str, topic_id: str
) -> None:
    """Creates a job that publishes a Pub/Sub message on a schedule.

    Args:
        project_id: The Google Cloud project ID (for example, 'example-project-id').
        location_id: The region for the job (for example, 'us-central1').
        job_id: The ID for the new job (for example, 'example-job-id').
        topic_id: The ID of an existing Pub/Sub topic in the project (for
            example, 'example-topic').
    """
    client = scheduler_v1.CloudSchedulerClient()
    parent = f"projects/{project_id}/locations/{location_id}"

    # Cloud Scheduler publishes by using its service agent, which needs the
    # Cloud Scheduler Service Agent role in the project.
    pubsub_target = scheduler_v1.PubsubTarget(
        topic_name=f"projects/{project_id}/topics/{topic_id}",
        data=b"example-payload",
        attributes={"example-key": "example-value"},
    )
    job = scheduler_v1.Job(
        name=f"{parent}/jobs/{job_id}",
        pubsub_target=pubsub_target,
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
        print(f"Topic: {response.pubsub_target.topic_name}")


# [END cloudscheduler_create_pubsub_job]


if __name__ == "__main__":
    import argparse
    import os

    # Each flag defaults to its environment variable, then to an example value.
    parser = argparse.ArgumentParser(
        description=create_pubsub_job.__doc__.splitlines()[0]
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
        "--topic-id",
        default=os.environ.get("TOPIC_ID", "example-topic"),
        help="ID of an existing Pub/Sub topic (default: $TOPIC_ID)",
    )
    args = parser.parse_args()

    create_pubsub_job(
        project_id=args.project_id,
        location_id=args.location_id,
        job_id=args.job_id,
        topic_id=args.topic_id,
    )
