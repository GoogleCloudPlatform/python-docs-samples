# Copyright 2015 Google Inc. All rights reserved.
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

"""Command-line program to list the logs in a Google Cloud Platform project.

Simple command-line program to demonstrate connecting to the Google Cloud
Logging API to retrieve logs data, using application default credentials[1] to
authenticate.

This application will run--without modification--on 1) Google App Engine,
2) Google Compute Engine, 3) a local Linux workstation with the Google Cloud
SDK, or 4) a Linux computer without the SDK.

In cases 1) and 2), authorization comes from a built-in service account on the
instance running this application.  In case 3) you must run "gcloud auth login"
your workstation to authorize the application.  In case 4) you must create a
service account[2] in the Google Cloud project whose log data you will fetch,
copy the account's JSON private key file to the computer running this
application, and on that computer set the environment variable
GOOGLE_APPLICATION_CREDENTIALS to point to the JSON private key file. For
example:

    $ export GOOGLE_APPLICATION_CREDENTIALS=/path/to/json-key.json

[1] https://developers.google.com/identity/protocols/application-default-credentials
[2] https://console.developers.google.com/project/_/apiui/credential
"""  # NOQA

# [START all]
import json
import sys

from googleapiclient.discovery import build

from oauth2client.client import GoogleCredentials

# [START auth]
def GetLoggingService():
    credentials = GoogleCredentials.get_application_default()
    service = build('logging', 'v1beta3', credentials=credentials)
    return service
# [END auth]


# [START listlogs]
def ListLogs(project_id, service):
    next_page_token = None
    while True:
        response = service.projects().logs().list(
            projectsID=project_id, pageToken=next_page_token).execute()
        for log in response["logs"]:
            print log["name"]
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
# [END listlogs]


def main(project_id):
    service = GetLoggingService()
    ListLogs(project_id, service)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: %s <project-name>" % sys.argv[0]
        sys.exit(1)
    main(sys.argv[1])
# [END all]
