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


"""Writes and reads a lightweight custom metric.

This is an example of how to use the Stackdriver Monitoring API to write
and read a lightweight custom metric. Lightweight custom metrics have no
labels and you do not need to create a metric descriptor for them.

Prerequisites: To run locally, download a Service Account JSON file from
your project and point GOOGLE_APPLICATION_CREDENTIALS to the file.

From App Engine or a GCE instance with the correct scope, the Service
Account step is not required.

Typical usage: Run the following shell commands on the instance:

    python lightweight_custom_metric.py --project_id=<YOUR-PROJECT-ID>
"""

import argparse
import datetime
import os
import time

import googleapiclient.discovery

CUSTOM_METRIC_NAME = "custom.cloudmonitoring.googleapis.com/pid"


def format_rfc3339(datetime_instance=None):
    """Formats a datetime per RFC 3339.
    :param datetime_instance: Datetime instanec to format, defaults to utcnow
    """
    return datetime_instance.isoformat("T") + "Z"


def get_now_rfc3339():
    return format_rfc3339(datetime.datetime.utcnow())


def main(project_id):
    client = googleapiclient.discovery.build('cloudmonitoring', 'v2beta2')

    # Set up the write request.
    now = get_now_rfc3339()
    desc = {"project": project_id,
            "metric": CUSTOM_METRIC_NAME}
    point = {"start": now,
             "end": now,
             "doubleValue": os.getpid()}
    print("Writing {} at {}".format(point["doubleValue"], now))

    # Write a new data point.
    try:
        write_request = client.timeseries().write(
            project=project_id,
            body={"timeseries": [{"timeseriesDesc": desc, "point": point}]})
        write_request.execute()  # Ignore the response.
    except Exception as e:
        print("Failed to write custom metric data: exception={}".format(e))
        raise

    # Read all data points from the time series.
    # When a custom metric is created, it may take a few seconds
    # to propagate throughout the system. Retry a few times.
    print("Reading data from custom metric timeseries...")
    read_request = client.timeseries().list(
        project=project_id,
        metric=CUSTOM_METRIC_NAME,
        youngest=now)
    start = time.time()
    while True:
        try:
            read_response = read_request.execute()
            for point in read_response["timeseries"][0]["points"]:
                print("Point:  {}: {}".format(
                    point["end"], point["doubleValue"]))
            break
        except Exception as e:
            if time.time() < start + 20:
                print("Failed to read custom metric data, retrying...")
                time.sleep(3)
            else:
                print("Failed to read custom metric data, aborting: "
                      "exception={}".format(e))
                raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--project_id', help='Project ID you want to access.', required=True)

    args = parser.parse_args()
    main(args.project_id)
