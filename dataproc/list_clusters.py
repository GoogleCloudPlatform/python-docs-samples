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

"""Sample command-line program to list Cloud Dataproc Clusters.
"""

# Example Usage:
# python list_clusters.py $PROJECT-ID --region=$REGION

# -------------------------------
# Import required modules:
# -----------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse
from google.cloud import dataproc_v1
from google.cloud.dataproc_v1.gapic.transports import cluster_controller_grpc_transport


def list_clusters(dataproc, project, region):
  for cluster in dataproc.list_clusters(project, region):
    print(('{} - {}'.format(cluster.cluster_name,
                            cluster.status.State.Name(cluster.status.state))))


def main(project_id, region):
  if region == 'global':
    client_transport = ''
  else:
    client_transport = cluster_controller_grpc_transport.ClusterControllerGrpcTransport(
        address='{}-dataproc.googleapis.com:443'.format(region))
  dataproc_cluster_client = dataproc_v1.ClusterControllerClient(
      client_transport)

  list_clusters(dataproc_cluster_client, project_id, region)


if __name__ == '__main__':
  _ = parser = argparse.ArgumentParser(
      description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter
  )
  _ = parser.add_argument(
      'project_id', help='Project ID you want to access.'),
  _ = parser.add_argument(
      '--region', default='global', help='Region to list clusters')

args = parser.parse_args()
main(args.project_id, args.region)
