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


"""Creates, writes, and reads a labeled custom metric.

This is an example of how to use the Stackdriver Monitoring API to create,
write, and read a labeled custom metric.
The metric has two labels: color and size, and the data points represent
the number of shirts of the given color and size in inventory.

Prerequisites: To run locally, download a Service Account JSON file from
your project and point GOOGLE_APPLICATION_CREDENTIALS to the file.

From App Engine or a GCE instance with the correct scope, the Service
Account step is not required.

Typical usage: Run the following shell commands on the instance:
    python labeled_custom_metric.py --project_id <project_id> /
    --color yellow  --size large  --count 10
"""

import argparse
import datetime
import time

import googleapiclient.discovery

CUSTOM_METRIC_DOMAIN = "custom.cloudmonitoring.googleapis.com"
CUSTOM_METRIC_NAME = "{}/shirt_inventory".format(CUSTOM_METRIC_DOMAIN)


def format_rfc3339(datetime_instance=None):
    """Formats a datetime per RFC 3339.
    :param datetime_instance: Datetime instance to format, defaults to utcnow
    """
    return datetime_instance.isoformat("T") + "Z"


def get_now_rfc3339():
    return format_rfc3339(datetime.datetime.utcnow())


def create_custom_metric(client, project_id):
    """Create metric descriptor for the custom metric and send it to the
    API."""
    # You need to execute this operation only once. The operation is
    # idempotent, so, for simplicity, this sample code calls it each time

    # Create a label descriptor for each of the metric labels. The
    # "description" field should be more meaningful for your metrics.
    label_descriptors = []
    for label in ["color", "size", ]:
        label_descriptors.append({"key": "/{}".format(label),
                                  "description": "The {}.".format(label)})

    # Create the metric descriptor for the custom metric.
    metric_descriptor = {
        "name": CUSTOM_METRIC_NAME,
        "project": project_id,
        "typeDescriptor": {
            "metricType": "gauge",
            "valueType": "int64",
        },
        "labels": label_descriptors,
        "description": "The size of my shirt inventory.",
    }
    # Submit the custom metric creation request.
    try:
        request = client.metricDescriptors().create(
            project=project_id, body=metric_descriptor)
        request.execute()  # ignore the response
    except Exception as e:
        print("Failed to create custom metric: exception={})".format(e))
        raise


def write_custom_metric(client, project_id, now_rfc3339, color, size, count):
    """Write a data point to a single time series of the custom metric."""
    # Identify the particular time series to which to write the data by
    # specifying the metric and values for each label.
    timeseries_descriptor = {
        "project": project_id,
        "metric": CUSTOM_METRIC_NAME,
        "labels": {
            "{}/color".format(CUSTOM_METRIC_DOMAIN): color,
            "{}/size".format(CUSTOM_METRIC_DOMAIN): size,
        }
    }

    # Specify a new data point for the time series.
    timeseries_data = {
        "timeseriesDesc": timeseries_descriptor,
        "point": {
            "start": now_rfc3339,
            "end": now_rfc3339,
            "int64Value": count,
        }
    }

    # Submit the write request.
    request = client.timeseries().write(
        project=project_id, body={"timeseries": [timeseries_data, ]})
    try:
        request.execute()  # ignore the response
    except Exception as e:
        print("Failed to write data to custom metric: exception={}".format(e))
        raise


def read_custom_metric(client, project_id, now_rfc3339, color, size):
    """Read all the timeseries data points for a given set of label values."""
    # To identify a time series, specify values for in label as a list.
    labels = ["{}/color=={}".format(CUSTOM_METRIC_DOMAIN, color),
              "{}/size=={}".format(CUSTOM_METRIC_DOMAIN, size), ]

    # Submit the read request.
    request = client.timeseries().list(
        project=project_id,
        metric=CUSTOM_METRIC_NAME,
        youngest=now_rfc3339,
        labels=labels)

    # When a custom metric is created, it may take a few seconds
    # to propagate throughout the system. Retry a few times.
    start = time.time()
    while True:
        try:
            response = request.execute()
            for point in response["timeseries"][0]["points"]:
                print("{}: {}".format(point["end"], point["int64Value"]))
            break
        except Exception as e:
            if time.time() < start + 20:
                print("Failed to read custom metric data, retrying...")
                time.sleep(3)
            else:
                print("Failed to read custom metric data, aborting: "
                      "exception={}".format(e))
                raise


def get_client():
    """Builds an http client authenticated with the application default
    credentials."""
    client = googleapiclient.discovery.build('cloudmonitoring', 'v2beta2')
    return client


def main(project_id, color, size, count):
    now_rfc3339 = get_now_rfc3339()

    client = get_client()

    print("Labels: color: {}, size: {}.".format(color, size))
    print("Creating custom metric...")
    create_custom_metric(client, project_id)
    time.sleep(2)
    print("Writing new data to custom metric timeseries...")
    write_custom_metric(client, project_id, now_rfc3339,
                        color, size, count)
    print("Reading data from custom metric timeseries...")
    read_custom_metric(client, project_id, now_rfc3339, color, size)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        '--project_id', help='Project ID you want to access.', required=True)
    parser.add_argument("--color", required=True)
    parser.add_argument("--size", required=True)
    parser.add_argument("--count", required=True)

    args = parser.parse_args()
    main(args.project_id, args.color, args.size, args.count)
