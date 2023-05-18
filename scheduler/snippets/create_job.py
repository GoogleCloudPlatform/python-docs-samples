# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START cloudscheduler_create_job]

from google.cloud import scheduler
from google.cloud.scheduler_v1 import Job


def create_scheduler_job(project_id: str, location_id: str, service_id: str) -> Job:
    """Create a job with an App Engine target via the Cloud Scheduler API.

    Args:
        project_id: The Google Cloud project id.
        location_id: The location for the job.
        service_id: An unique service id for the job.

    Returns:
        The created job.
    """

    # Create a client.
    client = scheduler.CloudSchedulerClient()

    # Construct the fully qualified location path.
    parent = f"projects/{project_id}/locations/{location_id}"

    # Construct the request body.
    job = {
        "app_engine_http_target": {
            "app_engine_routing": {"service": service_id},
            "relative_uri": "/log_payload",
            "http_method": 1,
            "body": b"Hello World",
        },
        "schedule": "* * * * *",
        "time_zone": "America/Los_Angeles",
    }

    # Use the client to send the job creation request.
    response = client.create_job(request={"parent": parent, "job": job})

    print(f"Created job: {response.name}")
    return response

# [END cloudscheduler_create_job]
