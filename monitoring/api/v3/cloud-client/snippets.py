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

import argparse

from google.cloud.monitoring import (
    Aligner, Client, MetricKind, Reducer, ValueType)


def create_metric_descriptor(client):
    descriptor = client.metric_descriptor(
        'custom.googleapis.com/my_metric',
        metric_kind=MetricKind.GAUGE,
        value_type=ValueType.DOUBLE,
        description='This is a simple example of a custom metric.')
    descriptor.create()


def delete_metric_descriptor(client, descriptor):
    descriptor = client.metric_descriptor(
        'custom.googleapis.com/my_metric'
    )
    descriptor.delete()
    print 'Deleted metric.'


def write_time_series(client):
    resource = client.resource(
        'gce_instance',
        labels={
            'instance_id': '1234567890123456789',
            'zone': 'us-central1-f',
        }
    )

    metric = client.metric(
        type_='custom.googleapis.com/my_metric',
        labels={
            'status': 'successful',
        }
    )
    client.write_point(metric, resource, 3.14)


def list_time_series(client):
    metric = 'compute.googleapis.com/instance/cpu/utilization'
    print(list(client.query(metric, minutes=5)))


def list_time_series_header(client):
    metric = 'compute.googleapis.com/instance/cpu/utilization'
    print(list(client.query(metric, minutes=5).iter(headers_only=True)))


def list_time_series_aggregate(client):
    metric = 'compute.googleapis.com/instance/cpu/utilization'
    print(list(client.query(metric, hours=1).align(
        Aligner.ALIGN_MEAN, minutes=5)))


def list_time_series_reduce(client):
    metric = 'compute.googleapis.com/instance/cpu/utilization'
    print(list(client.query(metric, hours=1).align(
        Aligner.ALIGN_MEAN, minutes=5).reduce(
        Reducer.REDUCE_MEAN, 'resource.zone')))


def list_metric_descriptors(client):
    for descriptor in client.list_metric_descriptors():
        print(descriptor.type)


def list_monitored_resources(client):
    for descriptor in client.list_resource_descriptors():
        print (descriptor.type)


def get_monitored_resource_descriptor(client, type):
    print(client.fetch_resource_descriptor(type))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Demonstrates Monitoring API operations.')
    parser.add_argument('--project_id', help='Your cloud project ID.')

    subparsers = parser.add_subparsers(dest='command')

    create_metric_descriptor_parser = subparsers.add_parser(
        'create-metric-descriptor',
        help=create_metric_descriptor.__doc__
    )

    list_metric_descriptor_parser = subparsers.add_parser(
        'list-metric-descriptors',
        help=list_metric_descriptors.__doc__
    )

    delete_metric_descriptor_parser = subparsers.add_parser(
        'delete-metric-descriptor',
        help=list_metric_descriptors.__doc__
    )

    delete_metric_descriptor_parser.add_argument(
        '--metric',
        help='Metric descriptor to delete',
        required=True
    )

    list_resources_parser = subparsers.add_parser(
        'list-resources',
        help=list_monitored_resources.__doc__
    )

    get_resource_parser = subparsers.add_parser(
        'get-resource',
        help=get_monitored_resource_descriptor.__doc__
    )

    get_resource_parser.add_argument(
        '--resource',
        help='Monitored resource to view more information about.',
        required=True
    )

    write_time_series_parser = subparsers.add_parser(
        'write-time-series',
        help=write_time_series.__doc__
    )

    list_time_series_parser = subparsers.add_parser(
        'list-time-series',
        help=list_time_series.__doc__
    )

    list_time_series_header_parser = subparsers.add_parser(
        'list-time-series-header',
        help=list_time_series_header.__doc__
    )

    read_time_series_reduce = subparsers.add_parser(
        'list-time-series-reduce',
        help=list_time_series_reduce.__doc__
    )

    read_time_series_aggregate = subparsers.add_parser(
        'list-time-series-aggregate',
        help=list_time_series_aggregate.__doc__
    )

    args = parser.parse_args()
    client = Client(args.project_id)

    if args.command == 'create-metric-descriptor':
        create_metric_descriptor(client)
    if args.command == 'list-metric-descriptors':
        list_metric_descriptors(client)
    if args.command == 'delete-metric-descriptor':
        delete_metric_descriptor(client, args.metric)
    if args.command == 'list-resources':
        list_monitored_resources(client)
    if args.command == 'get-resource':
        get_monitored_resource_descriptor(client, args.resource)
    if args.command == 'write-time-series':
        write_time_series(client)
    if args.command == 'list-time-series':
        list_time_series(client)
    if args.command == 'list-time-series-header':
        list_time_series_header(client)
    if args.command == 'list-time-series-reduce':
        list_time_series_reduce(client)
    if args.command == 'list-time-series-aggregate':
        list_time_series_aggregate(client)
