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
import json

from bigquery.samples.utils import get_service, paging
from six.moves import input


# [START sync_query]
def sync_query(service, project_id, query, timeout=10000, num_retries=5):
    query_data = {
        'query': query,
        'timeoutMs': timeout,
    }
    return service.jobs().query(
        projectId=project_id,
        body=query_data).execute(num_retries=num_retries)
# [END sync_query]


# [START run]
def run(project_id, query, timeout, num_retries):
    service = get_service()
    response = sync_query(service,
                          project_id,
                          query,
                          timeout,
                          num_retries)

    for page in paging(service,
                       service.jobs().getQueryResults,
                       num_retries=num_retries,
                       **response['jobReference']):
        yield json.dumps(page['rows'])
# [END run]


# [START main]
def main():
    project_id = input("Enter the project ID: ")
    query_string = input("Enter the Bigquery SQL Query: ")
    timeout = input(
        "Enter how long to wait for the query to complete in milliseconds"
        "\n (if longer than 10 seconds, use an asynchronous query): ")
    num_retries = int(input(
        "Enter how many times to retry in case of server error"))

    for result in run(project_id, query_string, timeout, num_retries):
        print(result)

# [END main]
