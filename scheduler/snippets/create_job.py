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


def create_scheduler_job(project_id, location_id, service_id):
    """Create a job with an App Engine target via the Cloud Scheduler API"""
    # [START cloud_scheduler_create_job]
    from google.cloud import scheduler

    # Create a client.
    client = scheduler.CloudSchedulerClient()

    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID'
    # location_id = 'LOCATION_ID'
    # service_id = 'my-service'

    # Construct the fully qualified location path.
    parent = f"projects/{project_id}/locations/{location_id}"

    # Construct the request body.
    job = {
        'app_engine_http_target': {
            'app_engine_routing': {
                'service': service_id
            },
            'relative_uri': '/log_payload',
            'http_method': 1,
            'body': 'Hello World'.encode()
        },
        'schedule': '* * * * *',
        'time_zone': 'America/Los_Angeles'
    }

    # Use the client to send the job creation request.
    response = client.create_job(
        request={
            "parent": parent,
            "job": job
        }
    )

    print('Created job: {}'.format(response.name))
    # [END cloud_scheduler_create_job]
    return response


def delete_scheduler_job(project_id, location_id, job_id):
    """Delete a job via the Cloud Scheduler API"""
    # [START cloud_scheduler_delete_job]
    from google.cloud import scheduler
    from google.api_core.exceptions import GoogleAPICallError

    # Create a client.
    client = scheduler.CloudSchedulerClient()

    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID'
    # location_id = 'LOCATION_ID'
    # job_id = 'JOB_ID'

    # Construct the fully qualified job path.
    job = f"projects/{project_id}/locations/{location_id}/jobs/{job_id}"

    # Use the client to send the job deletion request.
    try:
        client.delete_job(name=job)
        print("Job deleted.")
    except GoogleAPICallError as e:
        print("Error: %s" % e)
    # [END cloud_scheduler_delete_job]
