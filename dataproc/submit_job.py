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

def submit_job(project_id, region, cluster_name, job_file_path):
    # [START_dataproc_submit_job]
    from google.cloud import dataproc_v1 as dataproc

    # TODO(developer): Uncomment and set the following variables
    # project_id = 'YOUR_PROJECT_ID'
    # region = 'YOUR_CLUSTER_REGION'
    # cluster_name = 'YOUR_CLUSTER_NAME'
    # job_file_path = 'YOUR_JOB_FILE_PATH'

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
        job = dataproc.get_job(project_id, region, job_id)
        # Handle exceptions
        if job.status.State.Name(job.status.state) == 'ERROR':
            print('Jod {} failed: {}'.format(job_id, job.status.details))
        elif job.status.State.Name(job.status.state) == 'DONE':
            print('Job {} finished.'.format(job_id))
            break
    # [END dataproc_submit_job]