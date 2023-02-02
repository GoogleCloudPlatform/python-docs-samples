# Copyright 2017 Google LLC
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
import os
import pprint
import time
import uuid

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


def create_metric_descriptor(project_id):
    # [START monitoring_create_metric]
    from google.api import label_pb2 as ga_label
    from google.api import metric_pb2 as ga_metric
    from google.cloud import monitoring_v3

    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    descriptor = ga_metric.MetricDescriptor()
    descriptor.type = "custom.googleapis.com/my_metric" + str(uuid.uuid4())
    descriptor.metric_kind = ga_metric.MetricDescriptor.MetricKind.GAUGE
    descriptor.value_type = ga_metric.MetricDescriptor.ValueType.DOUBLE
    descriptor.description = "This is a simple example of a custom metric."

    labels = ga_label.LabelDescriptor()
    labels.key = "TestLabel"
    labels.value_type = ga_label.LabelDescriptor.ValueType.STRING
    labels.description = "This is a test label"
    descriptor.labels.append(labels)

    descriptor = client.create_metric_descriptor(
        name=project_name, metric_descriptor=descriptor
    )
    print("Created {}.".format(descriptor.name))
    # [END monitoring_create_metric]


def delete_metric_descriptor(descriptor_name):
    # [START monitoring_delete_metric]
    from google.cloud import monitoring_v3

    client = monitoring_v3.MetricServiceClient()
    client.delete_metric_descriptor(name=descriptor_name)
    print("Deleted metric descriptor {}.".format(descriptor_name))
    # [END monitoring_delete_metric]


def write_time_series(project_id):
    # [START monitoring_write_timeseries]
    from google.cloud import monitoring_v3

    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/my_metric" + str(uuid.uuid4())
    series.resource.type = "gce_instance"
    series.resource.labels["instance_id"] = "1234567890123456789"
    series.resource.labels["zone"] = "us-central1-f"
    series.metric.labels["TestLabel"] = "My Label Data"
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)
    interval = monitoring_v3.TimeInterval(
        {"end_time": {"seconds": seconds, "nanos": nanos}}
    )
    point = monitoring_v3.Point({"interval": interval, "value": {"double_value": 3.14}})
    series.points = [point]
    client.create_time_series(name=project_name, time_series=[series])
    # [END monitoring_write_timeseries]


def list_time_series(project_id):
    # [START monitoring_read_timeseries_simple]
    from google.cloud import monitoring_v3

    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": (seconds - 1200), "nanos": nanos},
        }
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": 'metric.type = "compute.googleapis.com/instance/cpu/utilization"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    for result in results:
        print(result)
    # [END monitoring_read_timeseries_simple]


def list_time_series_header(project_id):
    # [START monitoring_read_timeseries_fields]
    from google.cloud import monitoring_v3

    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": (seconds - 1200), "nanos": nanos},
        }
    )
    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": 'metric.type = "compute.googleapis.com/instance/cpu/utilization"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.HEADERS,
        }
    )
    for result in results:
        print(result)
    # [END monitoring_read_timeseries_fields]


def list_time_series_aggregate(project_id):
    # [START monitoring_read_timeseries_align]
    from google.cloud import monitoring_v3

    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": (seconds - 3600), "nanos": nanos},
        }
    )
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 1200},  # 20 minutes
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        }
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": 'metric.type = "compute.googleapis.com/instance/cpu/utilization"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )
    for result in results:
        print(result)
    # [END monitoring_read_timeseries_align]


def list_time_series_reduce(project_id):
    # [START monitoring_read_timeseries_reduce]
    from google.cloud import monitoring_v3

    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": (seconds - 3600), "nanos": nanos},
        }
    )
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 1200},  # 20 minutes
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
            "group_by_fields": ["resource.zone"],
        }
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": 'metric.type = "compute.googleapis.com/instance/cpu/utilization"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )
    for result in results:
        print(result)
    # [END monitoring_read_timeseries_reduce]


def list_metric_descriptors(project_id):
    # [START monitoring_list_descriptors]
    from google.cloud import monitoring_v3

    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    for descriptor in client.list_metric_descriptors(name=project_name):
        print(descriptor.type)
    # [END monitoring_list_descriptors]


def list_monitored_resources(project_id):
    # [START monitoring_list_resources]
    from google.cloud import monitoring_v3

    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    resource_descriptors = client.list_monitored_resource_descriptors(name=project_name)
    for descriptor in resource_descriptors:
        print(descriptor.type)
    # [END monitoring_list_resources]


def get_monitored_resource_descriptor(project_id, resource_type_name):
    # [START monitoring_get_resource]
    from google.cloud import monitoring_v3

    client = monitoring_v3.MetricServiceClient()
    resource_path = (
        f"projects/{project_id}/monitoredResourceDescriptors/{resource_type_name}"
    )
    pprint.pprint(client.get_monitored_resource_descriptor(name=resource_path))
    # [END monitoring_get_resource]


def get_metric_descriptor(metric_name):
    # [START monitoring_get_descriptor]
    from google.cloud import monitoring_v3

    client = monitoring_v3.MetricServiceClient()
    descriptor = client.get_metric_descriptor(name=metric_name)
    pprint.pprint(descriptor)
    # [END monitoring_get_descriptor]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Demonstrates Monitoring API operations."
    )

    subparsers = parser.add_subparsers(dest="command")

    create_metric_descriptor_parser = subparsers.add_parser(
        "create-metric-descriptor", help=create_metric_descriptor.__doc__
    )

    list_metric_descriptor_parser = subparsers.add_parser(
        "list-metric-descriptors", help=list_metric_descriptors.__doc__
    )

    get_metric_descriptor_parser = subparsers.add_parser(
        "get-metric-descriptor", help=get_metric_descriptor.__doc__
    )

    get_metric_descriptor_parser.add_argument(
        "--metric-type-name",
        help="The metric type of the metric descriptor to see details about.",
        required=True,
    )

    delete_metric_descriptor_parser = subparsers.add_parser(
        "delete-metric-descriptor", help=list_metric_descriptors.__doc__
    )

    delete_metric_descriptor_parser.add_argument(
        "--metric-descriptor-name", help="Metric descriptor to delete", required=True
    )

    list_resources_parser = subparsers.add_parser(
        "list-resources", help=list_monitored_resources.__doc__
    )

    get_resource_parser = subparsers.add_parser(
        "get-resource", help=get_monitored_resource_descriptor.__doc__
    )

    get_resource_parser.add_argument(
        "--resource-type-name",
        help="Monitored resource to view more information about.",
        required=True,
    )

    write_time_series_parser = subparsers.add_parser(
        "write-time-series", help=write_time_series.__doc__
    )

    list_time_series_parser = subparsers.add_parser(
        "list-time-series", help=list_time_series.__doc__
    )

    list_time_series_header_parser = subparsers.add_parser(
        "list-time-series-header", help=list_time_series_header.__doc__
    )

    read_time_series_reduce = subparsers.add_parser(
        "list-time-series-reduce", help=list_time_series_reduce.__doc__
    )

    read_time_series_aggregate = subparsers.add_parser(
        "list-time-series-aggregate", help=list_time_series_aggregate.__doc__
    )

    args = parser.parse_args()

    if args.command == "create-metric-descriptor":
        create_metric_descriptor(PROJECT_ID)
    if args.command == "list-metric-descriptors":
        list_metric_descriptors(PROJECT_ID)
    if args.command == "get-metric-descriptor":
        get_metric_descriptor(args.metric_type_name)
    if args.command == "delete-metric-descriptor":
        delete_metric_descriptor(args.metric_descriptor_name)
    if args.command == "list-resources":
        list_monitored_resources(PROJECT_ID)
    if args.command == "get-resource":
        get_monitored_resource_descriptor(PROJECT_ID, args.resource_type_name)
    if args.command == "write-time-series":
        write_time_series(PROJECT_ID)
    if args.command == "list-time-series":
        list_time_series(PROJECT_ID)
    if args.command == "list-time-series-header":
        list_time_series_header(PROJECT_ID)
    if args.command == "list-time-series-reduce":
        list_time_series_reduce(PROJECT_ID)
    if args.command == "list-time-series-aggregate":
        list_time_series_aggregate(PROJECT_ID)
