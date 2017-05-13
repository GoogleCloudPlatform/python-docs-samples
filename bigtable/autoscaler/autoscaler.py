# Copyright 2017 Google Inc.
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

"""Sample that demonstrates how to use Bigtable Stackdriver metrics to
autoscale Google Cloud Bigtable."""

import argparse
import os
import time

from google.cloud import bigtable
from google.cloud import monitoring

import strategies

CPU_METRIC = 'bigtable.googleapis.com/cluster/cpu_load'


def get_cpu_load():
    """Returns the most recent Bigtable CPU load measurement.

    Returns:
          float: The most recent Bigtable CPU usage metric
    """
    client = monitoring.Client()
    query = client.query(CPU_METRIC, minutes=5)
    return list(query)[0].points[0].value


def scale_bigtable(bigtable_instance, up):
    """Scales the number of Bigtable nodes up or down.

    Args:
           bigtable_instance (str): Cloud Bigtable instance id to scale
           up (bool): If true, scale up, otherwise scale down
    """
    bigtable_client = bigtable.Client(admin=True)
    instance = bigtable_client.instance(bigtable_instance)
    instance.reload()

    cluster = instance.cluster('{}-cluster'.format(bigtable_instance))
    cluster.reload()

    current_node_count = cluster.serve_nodes

    if current_node_count <= 3 and not up:
        # Can't downscale lower than 3 nodes
        return

    if up:
        strategies_dict = strategies.UPSCALE_STRATEGIES
    else:
        strategies_dict = strategies.DOWNSCALE_STRATEGIES

    strategy = strategies_dict['incremental']
    new_node_count = strategy(cluster.serve_nodes)
    cluster.serve_nodes = new_node_count
    cluster.update()
    print('Scaled from {} up to {} nodes.'.format(
        current_node_count, new_node_count))


def main(
        bigtable_instance,
        high_cpu_threshold,
        low_cpu_threshold,
        short_sleep,
        long_sleep):
    """Main loop runner that autoscales Bigtable.

    Args:
          bigtable_instance (str): Cloud Bigtable instance id to autoscale
          high_cpu_threshold (float): If CPU is higher than this, scale up.
          low_cpu_threshold (float): If CPU is higher than this, scale down.
          short_sleep (int): How long to sleep after no operation
          long_sleep (int): How long to sleep after the cluster nodes are
                            changed
    """
    cluster_cpu = get_cpu_load()
    print('Detected cpu of {}'.format(cluster_cpu))
    if cluster_cpu > high_cpu_threshold:
        scale_bigtable(bigtable_instance, True)
        time.sleep(long_sleep)
    elif cluster_cpu < low_cpu_threshold:
        scale_bigtable(bigtable_instance, False)
        time.sleep(short_sleep)
    else:
        print('CPU within threshold, sleeping.')
        time.sleep(short_sleep)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Scales Bigtable clusters based on CPU usage.')
    parser.add_argument(
        'bigtable_instance', help='ID of the Cloud Bigtable instance to '
                                  'connect to.')
    parser.add_argument(
        '--high_cpu_threshold',
        help='If Bigtable CPU usages is above this threshold, scale up',
        default=0.6)
    parser.add_argument(
        '--low_cpu_threshold',
        help='If Bigtable CPU usages is above this threshold, scale up',
        default=0.2)
    parser.add_argument(
        '--short_sleep',
        help='How long to sleep in seconds between checking metrics after no '
             'scale operation',
        default=60)
    parser.add_argument(
        '--long_sleep',
        help='How long to sleep in seconds between checking metrics after a '
             'scaling operation',
        default=60 * 10)
    args = parser.parse_args()

    while True:
        main(
            args.bigtable_instance,
            float(args.high_cpu_threshold),
            float(args.low_cpu_threshold),
            int(args.short_sleep),
            int(args.long_sleep))
