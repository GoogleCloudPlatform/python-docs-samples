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

"""Sample that demonstrates how to use Stackdriver Monitoring metrics to
programmatically scale a Google Cloud Bigtable cluster."""

import argparse
import time

from google.cloud import bigtable
from google.cloud import monitoring


def get_cpu_load():
    """Returns the most recent Cloud Bigtable CPU load measurement.

    Returns:
          float: The most recent Cloud Bigtable CPU usage metric
    """
    # [START bigtable_cpu]
    client = monitoring.Client()
    query = client.query('bigtable.googleapis.com/cluster/cpu_load', minutes=5)
    time_series = list(query)
    recent_time_series = time_series[0]
    return recent_time_series.points[0].value
    # [END bigtable_cpu]


def scale_bigtable(bigtable_instance, bigtable_cluster, scale_up):
    """Scales the number of Cloud Bigtable nodes up or down.

    Edits the number of nodes in the Cloud Bigtable cluster to be increased
    or decreased, depending on the `scale_up` boolean argument. Currently
    the `incremental` strategy from `strategies.py` is used.


    Args:
           bigtable_instance (str): Cloud Bigtable instance ID to scale
           bigtable_cluster (str): Cloud Bigtable cluster ID to scale
           scale_up (bool): If true, scale up, otherwise scale down
    """

    # The minimum number of nodes to use. The default minimum is 3. If you have
    # a lot of data, the rule of thumb is to not go below 2.5 TB per node for
    # SSD lusters, and 8 TB for HDD. The
    # "bigtable.googleapis.com/disk/bytes_used" metric is useful in figuring
    # out the minimum number of nodes.
    min_node_count = 3

    # The maximum number of nodes to use. The default maximum is 30 nodes per
    # zone. If you need more quota, you can request more by following the
    # instructions at https://cloud.google.com/bigtable/quota.
    max_node_count = 30

    # The number of nodes to change the cluster by.
    size_change_step = 3

    # [START bigtable_scale]
    bigtable_client = bigtable.Client(admin=True)
    instance = bigtable_client.instance(bigtable_instance)
    instance.reload()

    cluster = instance.cluster(bigtable_cluster)
    cluster.reload()

    current_node_count = cluster.serve_nodes

    if scale_up:
        if current_node_count < max_node_count:
            new_node_count = min(
                current_node_count + size_change_step, max_node_count)
            cluster.serve_nodes = new_node_count
            cluster.update()
            print('Scaled up from {} to {} nodes.'.format(
                current_node_count, new_node_count))
    else:
        if current_node_count > min_node_count:
            new_node_count = max(
                current_node_count - size_change_step, min_node_count)
            cluster.serve_nodes = new_node_count
            cluster.update()
            print('Scaled down from {} to {} nodes.'.format(
                current_node_count, new_node_count))
    # [END bigtable_scale]


def main(
        bigtable_instance,
        bigtable_cluster,
        high_cpu_threshold,
        low_cpu_threshold,
        short_sleep,
        long_sleep):
    """Main loop runner that autoscales Cloud Bigtable.

    Args:
          bigtable_instance (str): Cloud Bigtable instance ID to autoscale
          high_cpu_threshold (float): If CPU is higher than this, scale up.
          low_cpu_threshold (float): If CPU is lower than this, scale down.
          short_sleep (int): How long to sleep after no operation
          long_sleep (int): How long to sleep after the number of nodes is
                            changed
    """
    cluster_cpu = get_cpu_load()
    print('Detected cpu of {}'.format(cluster_cpu))
    if cluster_cpu > high_cpu_threshold:
        scale_bigtable(bigtable_instance, bigtable_cluster, True)
        time.sleep(long_sleep)
    elif cluster_cpu < low_cpu_threshold:
        scale_bigtable(bigtable_instance, bigtable_cluster, False)
        time.sleep(long_sleep)
    else:
        print('CPU within threshold, sleeping.')
        time.sleep(short_sleep)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Scales Cloud Bigtable clusters based on CPU usage.')
    parser.add_argument(
        'bigtable_instance',
        help='ID of the Cloud Bigtable instance to connect to.')
    parser.add_argument(
        'bigtable_cluster',
        help='ID of the Cloud Bigtable cluster to connect to.')
    parser.add_argument(
        '--high_cpu_threshold',
        help='If Cloud Bigtable CPU usage is above this threshold, scale up',
        default=0.6)
    parser.add_argument(
        '--low_cpu_threshold',
        help='If Cloud Bigtable CPU usage is below this threshold, scale down',
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
            args.bigtable_cluster,
            float(args.high_cpu_threshold),
            float(args.low_cpu_threshold),
            int(args.short_sleep),
            int(args.long_sleep))
