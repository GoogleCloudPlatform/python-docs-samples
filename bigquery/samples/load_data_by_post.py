#	Copyright 2015, Google, Inc. 
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
import httplib2
from samples.utils import get_service, poll_job
from oauth2client.client import GoogleCredentials


# [START make_post]
def make_post(http, schema, data, projectId, datasetId, tableId):
    url = ('https://www.googleapis.com/upload/bigquery/v2/projects/' +
           projectId + '/jobs')
    # Create the body of the request, separated by a boundary of xxx
    resource = ('--xxx\n' +
                'Content-Type: application/json; charset=UTF-8\n' + '\n' +
                '{\n' +
                '   "configuration": {\n' +
                '     "load": {\n' +
                '       "schema": {\n'
                '         "fields": ' + str(schema) + '\n' +
                '      },\n' +
                '      "destinationTable": {\n' +
                '        "projectId": "' + projectId + '",\n' +
                '        "datasetId": "' + datasetId + '",\n' +
                '        "tableId": "' + tableId + '"\n' +
                '      }\n' +
                '    }\n' +
                '  }\n' +
                '}\n' +
                '--xxx\n' +
                'Content-Type: application/octet-stream\n' +
                '\n')
    # Append data to the request body
    resource += data

    # Signify the end of the body
    resource += ('--xxx--\n')

    headers = {'Content-Type': 'multipart/related; boundary=xxx'}

    return http.request(url,
                        method='POST',
                        body=resource,
                        headers=headers)
    # [END make_post]


# [START main]
def main():
    credentials = GoogleCredentials.get_application_default()
    http = credentials.authorize(httplib2.Http())
    projectId = raw_input('Enter the project ID: ')
    datasetId = raw_input('Enter a dataset ID: ')
    tableId = raw_input('Enter a table name to load the data to: ')
    schema_path = raw_input(
            'Enter the path to the schema file for the table: ')

    with open(schema_path, 'r') as schema_file:
        schema = schema_file.read()

    data_path = raw_input('Enter the path to the data file: ')

    with open(data_path, 'r') as data_file:
        data = data_file.read()

    resp, content = make_post(http,
                              schema,
                              data,
                              projectId,
                              datasetId,
                              tableId)

    if resp.status == 200:
        job_resource = json.loads(content)
        service = get_service(credentials)
        poll_job(service, **job_resource['jobReference'])
        print("Success!")
    else:
        print("Http error code: {}".format(resp.status))
# [END main]

if __name__ == '__main__':
    main()
