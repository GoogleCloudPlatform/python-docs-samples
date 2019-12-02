# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START_dataproc_submit_job]
from google.cloud import dataproc_v1 as dataproc


def submit_job(project_id, region, cluster_name, job_file_path):
    """Submit a job to a Cloud Dataproc cluster."""
    # Create a job client
    job_client = dataproc.JobControllerClient(client_options={
      'api_endpoint': '{}-dataproc.googleapis.com:443'.format(region)
    })

    job = {
      'placement': {
        'cluster_name': cluster_name
      },
      'pyspark_job': {
        'main_python_file_uri': job_file_path
      }
    }

    job_operation = job_client.submit_job(project_id, region, job)
    job_id = job_operation.reference.job_id
    print('Submitted job ID {}.'.format(job_id))

    # Wait for job to finish
    while True:
        job_info = job_client.get_job(project_id, region, job_id)
        # Handle exceptions
        if job_info.status.State.Name(job_info.status.state) == 'ERROR':
            print('Job {} failed: {}'.format(job_id, job_info.status.details))
            break
        elif job_info.status.State.Name(job_info.status.state) == 'DONE':
            print('Job {} finished.'.format(job_id))
            break
    # [END dataproc_submit_job]
