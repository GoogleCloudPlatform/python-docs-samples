 # Copyright 2018 Google LLC
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

# [START cloud_scheduler_create_job]
from google.cloud import scheduler

client = scheduler.CloudSchedulerClient()

# TODO(developer): Uncomment and set the following variables
# project_id = "PROJECT_ID"
# location_id = "LOCATION_ID"
# app_engine_version = "VERSION_ID"

parent = client.location_path(project_id, location_id)

job = {
    'app_engine_http_target': {
      'app_engine_routing': {
        'service':'default',
        'version': app_engine_version
        },
      'relative_uri': '/log_payload',
      'http_method': 'POST',
      'body': 'Hello World'.encode()
    },
    'schedule': "* * * * *",
    'time_zone': "America/Los_Angeles"
}

response = client.create_job(parent, job)
# [END cloud_scheduler_create_job]
