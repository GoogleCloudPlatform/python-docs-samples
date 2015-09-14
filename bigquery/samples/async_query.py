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
import argparse
import json
import uuid

from utils import get_service, paging, poll_job


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
def main(project_id, query_string, batch, num_retries, interval):
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

        print(json.dumps(page['rows']))
# [END run]


# [START main]
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Loads data into BigQuery.')
    parser.add_argument('project_id', help='Your Google Cloud project ID.')
    parser.add_argument('query', help='BigQuery SQL Query.')
    parser.add_argument(
        '-b', '--batch', help='Run query in batch mode.', action='store_true')
    parser.add_argument(
        '-r', '--num_retries',
        help='Number of times to retry in case of 500 error.',
        type=int,
        default=5)
    parser.add_argument(
        '-p', '--poll_interval',
        help='How often to poll the query for completion (seconds).',
        type=int,
        default=1)

    args = parser.parse_args()

    main(
        args.project_id,
        args.query,
        args.batch,
        args.num_retries,
        args.poll_interval)
# [END main]
