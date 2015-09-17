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

"""Sample command-line program for retrieving Google Cloud Monitoring API data.

Simple command-line program to demonstrate connecting to the Google Cloud
Monitoring API to retrieve API data, using application default credentials to
authenticate.

This sample obtains authentication information from its environment via
application default credentials [1].

If you're not running the sample on Google App Engine or Compute Engine (where
the environment comes pre-authenticated as a service account), you'll have to
initialize your environment with credentials the sample can use.

One way to do this is through the cloud console's credentials page [2]. Create
a new client ID of type 'Service account', and download its JSON key. This will
be the account the sample authenticates as.

Once you've downloaded the service account's JSON key, you provide it to the
sample by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable to
point to the key file:

$ export GOOGLE_APPLICATION_CREDENTIALS=/path/to/json-key.json

[1] https://developers.google.com/identity/protocols/\
    application-default-credentials
[2] https://console.developers.google.com/project/_/apiui/credential
"""  # NOQA

# [START all]
import json
import sys

from googleapiclient.discovery import build

from oauth2client.client import GoogleCredentials


METRIC = 'compute.googleapis.com/instance/disk/read_ops_count'
YOUNGEST = '2015-01-01T00:00:00Z'


def ListTimeseries(project_name, service):
    """Query the Timeseries.list API method.

    Args:
      project_name: the name of the project you'd like to monitor.
      service: the CloudMonitoring service object.
    """

    timeseries = service.timeseries()

    print('Timeseries.list raw response:')
    try:
        response = timeseries.list(
            project=project_name, metric=METRIC, youngest=YOUNGEST).execute()

        print(json.dumps(response,
                         sort_keys=True,
                         indent=4,
                         separators=(',', ': ')))
    except:
        print('Error:')
        for error in sys.exc_info():
            print(error)


def main(project_name):
    # Create and return the CloudMonitoring service object.
    service = build('cloudmonitoring', 'v2beta2',
                    credentials=GoogleCredentials.get_application_default())

    ListTimeseries(project_name, service)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} <project-name>".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1])
# [END all]
