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

"""Demonstrates how to perform basic access policy queries with Google Cloud IAM.
For more information, see the documentation at
https://cloud.google.com/iam/docs/
"""


from google.oauth2 import service_account
import googleapiclient.discovery


class my_dictionary(dict):

    # __init__ function
    def __init__(self):
        self = dict()

    # Function to add key:value
    def add(self, key, value):
        self[key] = value


credentials = service_account.Credentials.from_service_account_file(
    filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
    scopes=['https://www.googleapis.com/auth/cloud-platform'])
print('Starting to query projects')
service = discovery.build(
    'cloudresourcemanager', 'v1', credentials=credentials)

# [START generatePolicyReport]
def generatePolicyReport()
    try:
        request = service.projects().list()
        response = request.execute()
        project_list = my_dictionary()
        for project in response.get('projects', []):
            project_list.add(
                project['projectNumber'], project['projectId'])
        print('Starting to query IAM bindings')
        for key, value in project_list.items():
            policy = service.projects().getIamPolicy(
                resource=value, body={}).execute()
            for bindings in policy.get('bindings', []):
                with open('GCPIAMBindings.csv', 'a') as f:
                    print(value, bindings['role'], bindings['members'], file=f)

        print('Finished export')
    except Exception as e:
        print(e)
# [END generatePolicyReport]
