#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Sample command-line program for listing Google Dataproc Clusters
"""

import argparse

import googleapiclient.discovery

# Currently only the "global" region is supported
REGION = 'global'


# [START list_clusters]
def list_clusters(dataproc, project):
    result = dataproc.projects().regions().clusters().list(
        projectId=project,
        region=REGION).execute()
    return result
# [END list_clusters]


# [START get_client]
def get_client():
    """Builds a client to the dataproc API."""
    dataproc = googleapiclient.discovery.build('dataproc', 'v1')
    return dataproc
# [END get_client]


def main(project_id, zone):
    dataproc = get_client()
    result = list_clusters(dataproc, project_id)
    print(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'project_id', help='Project ID you want to access.'),
    parser.add_argument(
        'zone', help='Region to create clusters in')

    args = parser.parse_args()
    main(args.project_id, args.zone)
