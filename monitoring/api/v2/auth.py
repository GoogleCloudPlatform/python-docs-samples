#!/usr/bin/env pyhton

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

"""Sample command-line program for retrieving Stackdriver Monitoring API data.

Prerequisites: To run locally, download a Service Account JSON file from
your project and point GOOGLE_APPLICATION_CREDENTIALS to the file.


This sample is used on this page:

    https://cloud.google.com/monitoring/api/authentication

For more information, see the README.md under /monitoring.
"""

# [START all]
import argparse
import json

import googleapiclient.discovery

METRIC = 'compute.googleapis.com/instance/disk/read_ops_count'
YOUNGEST = '2015-01-01T00:00:00Z'


def list_timeseries(project_name):
    """Query the Timeseries.list API method.

    Args:
      monitoring: the CloudMonitoring service object.
      project_name: the name of the project you'd like to monitor.
    """
    monitoring = googleapiclient.discovery.build('cloudmonitoring', 'v2beta2')

    timeseries = monitoring.timeseries()

    response = timeseries.list(
        project=project_name, metric=METRIC, youngest=YOUNGEST).execute()

    print('Timeseries.list raw response:')
    print(json.dumps(
      response,
      sort_keys=True,
      indent=2,
      separators=(',', ': ')))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud project ID.')

    args = parser.parse_args()

    list_timeseries(args.project_id)
# [END all]
