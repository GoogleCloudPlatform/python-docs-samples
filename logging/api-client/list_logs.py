#!/usr/bin/env python

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

This sample is used in this section of the documentation:

    https://cloud.google.com/logging/docs

For more information, see the README.md under /cloud_logging.
"""

# [START all]
import argparse

import googleapiclient.discovery


# [START list_logs]
def list_logs(project_id, logging_service):
    request = logging_service.projects().logs().list(projectsId=project_id)

    while request:
        response = request.execute()
        if not response:
            print("No logs found in {0} project").format(project_id)
            return False

        for log in response['logs']:
            print(log['name'])

        request = logging_service.projects().logs().list_next(
            request, response)
# [END list_logs]


def main(project_id):
    # [START build_service]
    logging_service = googleapiclient.discovery.build('logging', 'v1beta3')
    # [END build_service]

    list_logs(project_id, logging_service)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud project ID.')

    args = parser.parse_args()

    main(args.project_id)
# [END all]
