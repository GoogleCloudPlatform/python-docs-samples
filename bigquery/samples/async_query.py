# Copyright 2015, Google, Inc.
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
#
from __future__ import print_function  # For python 2/3 interoperability

import json
import uuid

from bigquery.samples.utils import get_service
from bigquery.samples.utils import paging
from bigquery.samples.utils import poll_job
from bigquery.samples.utils import get_input


# [START async_query]
def async_query(service, project_id, query, batch=False, num_retries=5):
    # Generate a unique job_id so retries
    # don't accidentally duplicate query
    job_data = {
        'jobReference': {
            'projectId': project_id,
            'job_id': str(uuid.uuid4())
        },
        'configuration': {
            'query': {
                'query': query,
                'priority': 'BATCH' if batch else 'INTERACTIVE'
            }
        }
    }
    return service.jobs().insert(
        projectId=project_id,
        body=job_data).execute(num_retries=num_retries)
# [END async_query]


# [START run]
def run(project_id, query_string, batch, num_retries, interval):
    service = get_service()

    query_job = async_query(service,
                            project_id,
                            query_string,
                            batch,
                            num_retries)

    poll_job(service,
             query_job['jobReference']['projectId'],
             query_job['jobReference']['jobId'],
             interval,
             num_retries)

    for page in paging(service,
                       service.jobs().getQueryResults,
                       num_retries=num_retries,
                       **query_job['jobReference']):

        yield json.dumps(page['rows'])
# [END run]


# [START main]
def main():
    project_id = get_input("Enter the project ID: ")
    query_string = get_input("Enter the Bigquery SQL Query: ")
    batch = get_input("Run query as batch (y/n)?: ") in (
        'True', 'true', 'y', 'Y', 'yes', 'Yes')

    num_retries = get_input(
        "Enter number of times to retry in case of 500 error: ")
    interval = get_input(
        "Enter how often to poll the query for completion (seconds): ")
    for result in run(project_id, query_string, batch, num_retries, interval):
        print(result)
# [END main]
