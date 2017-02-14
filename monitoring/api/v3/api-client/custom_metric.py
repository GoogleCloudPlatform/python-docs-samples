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

""" Sample command-line program for writing and reading Stackdriver Monitoring
API V3 custom metrics.

Simple command-line program to demonstrate connecting to the Google
Monitoring API to write custom metrics and read them back.

See README.md for instructions on setting up your development environment.

This example creates a custom metric based on a hypothetical GAUGE measurement.

To run locally:

    python custom_metric.py --project_id=<YOUR-PROJECT-ID>

"""

# [START all]
import argparse
import datetime
import pprint
import random
import time

import list_resources


def format_rfc3339(datetime_instance=None):
    """Formats a datetime per RFC 3339.
    :param datetime_instance: Datetime instanec to format, defaults to utcnow
    """
    return datetime_instance.isoformat("T") + "Z"


def get_start_time():
    # Return now- 5 minutes
    start_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
    return format_rfc3339(start_time)


def get_now_rfc3339():
    # Return now
    return format_rfc3339(datetime.datetime.utcnow())


def create_custom_metric(client, project_id,
                         custom_metric_type, metric_kind):
    """Create custom metric descriptor"""
    metrics_descriptor = {
        "type": custom_metric_type,
        "labels": [
            {
                "key": "environment",
                "valueType": "STRING",
                "description": "An arbitrary measurement"
            }
        ],
        "metricKind": metric_kind,
        "valueType": "INT64",
        "unit": "items",
        "description": "An arbitrary measurement.",
        "displayName": "Custom Metric"
    }

    return client.projects().metricDescriptors().create(
        name=project_id, body=metrics_descriptor).execute()


def delete_metric_descriptor(
        client, custom_metric_name):
    """Delete a custom metric descriptor."""
    client.projects().metricDescriptors().delete(
        name=custom_metric_name).execute()


def get_custom_metric(client, project_id, custom_metric_type):
    """Retrieve the custom metric we created"""
    request = client.projects().metricDescriptors().list(
        name=project_id,
        filter='metric.type=starts_with("{}")'.format(custom_metric_type))
    response = request.execute()
    print('ListCustomMetrics response:')
    pprint.pprint(response)
    try:
        return response['metricDescriptors']
    except KeyError:
        return None


def get_custom_data_point():
    """Dummy method to return a mock measurement for demonstration purposes.
    Returns a random number between 0 and 10"""
    length = random.randint(0, 10)
    print("reporting timeseries value {}".format(str(length)))
    return length


# [START write_timeseries]
def write_timeseries_value(client, project_resource,
                           custom_metric_type, instance_id, metric_kind):
    """Write the custom metric obtained by get_custom_data_point at a point in
    time."""
    # Specify a new data point for the time series.
    now = get_now_rfc3339()
    timeseries_data = {
        "metric": {
            "type": custom_metric_type,
            "labels": {
                "environment": "STAGING"
            }
        },
        "resource": {
            "type": 'gce_instance',
            "labels": {
                'instance_id': instance_id,
                'zone': 'us-central1-f'
            }
        },
        "points": [
            {
                "interval": {
                    "startTime": now,
                    "endTime": now
                },
                "value": {
                    "int64Value": get_custom_data_point()
                }
            }
        ]
    }

    request = client.projects().timeSeries().create(
        name=project_resource, body={"timeSeries": [timeseries_data]})
    request.execute()
# [END write_timeseries]


def read_timeseries(client, project_resource, custom_metric_type):
    """Reads all of the CUSTOM_METRICS that we have written between START_TIME
    and END_TIME
    :param project_resource: Resource of the project to read the timeseries
                             from.
    :param custom_metric_name: The name of the timeseries we want to read.
    """
    request = client.projects().timeSeries().list(
        name=project_resource,
        filter='metric.type="{0}"'.format(custom_metric_type),
        pageSize=3,
        interval_startTime=get_start_time(),
        interval_endTime=get_now_rfc3339())
    response = request.execute()
    return response


def main(project_id):
    # This is the namespace for all custom metrics
    CUSTOM_METRIC_DOMAIN = "custom.googleapis.com"
    # This is our specific metric name
    CUSTOM_METRIC_TYPE = "{}/custom_measurement".format(CUSTOM_METRIC_DOMAIN)
    INSTANCE_ID = "test_instance"
    METRIC_KIND = "GAUGE"

    project_resource = "projects/{0}".format(project_id)
    client = list_resources.get_client()
    create_custom_metric(client, project_resource,
                         CUSTOM_METRIC_TYPE, METRIC_KIND)
    custom_metric = None
    while not custom_metric:
        # wait until it's created
        time.sleep(1)
        custom_metric = get_custom_metric(
            client, project_resource, CUSTOM_METRIC_TYPE)

    write_timeseries_value(client, project_resource,
                           CUSTOM_METRIC_TYPE, INSTANCE_ID, METRIC_KIND)
    # Sometimes on new metric descriptors, writes have a delay in being read
    # back. 3 seconds should be enough to make sure our read call picks up the
    # write
    time.sleep(3)
    timeseries = read_timeseries(client, project_resource, CUSTOM_METRIC_TYPE)
    print('read_timeseries response:\n{}'.format(pprint.pformat(timeseries)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--project_id', help='Project ID you want to access.', required=True)

    args = parser.parse_args()
    main(args.project_id)

# [END all]
