#!/usr/bin/env python

# Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START all]
"""Command-line sample that creates a one-time transfer from Amazon S3 to
Google Cloud Storage.

This sample is used on this page:

    https://cloud.google.com/storage/transfer/create-transfer

For more information, see README.md.
"""

import argparse
import datetime
import json

import googleapiclient.discovery


# [START main]
def main(description, project_id, year, month, day, hours, minutes,
         source_bucket, access_key, secret_access_key, sink_bucket):
    """Create a one-off transfer from Amazon S3 to Google Cloud Storage."""
    storagetransfer = googleapiclient.discovery.build('storagetransfer', 'v1')

    # Edit this template with desired parameters.
    # Specify times below using US Pacific Time Zone.
    transfer_job = {
        'description': description,
        'status': 'ENABLED',
        'projectId': project_id,
        'schedule': {
            'scheduleStartDate': {
                'day': day,
                'month': month,
                'year': year
            },
            'scheduleEndDate': {
                'day': day,
                'month': month,
                'year': year
            },
            'startTimeOfDay': {
                'hours': hours,
                'minutes': minutes
            }
        },
        'transferSpec': {
            'awsS3DataSource': {
                'bucketName': source_bucket,
                'awsAccessKey': {
                    'accessKeyId': access_key,
                    'secretAccessKey': secret_access_key
                }
            },
            'gcsDataSink': {
                'bucketName': sink_bucket
            }
        }
    }

    result = storagetransfer.transferJobs().create(body=transfer_job).execute()
    print('Returned transferJob: {}'.format(
        json.dumps(result, indent=4)))
# [END main]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('description', help='Transfer description.')
    parser.add_argument('project_id', help='Your Google Cloud project ID.')
    parser.add_argument('date', help='Date YYYY/MM/DD.')
    parser.add_argument('time', help='Time (24hr) HH:MM.')
    parser.add_argument('source_bucket', help='Source bucket name.')
    parser.add_argument('access_key', help='Your AWS access key id.')
    parser.add_argument('secret_access_key', help='Your AWS secret access '
                        'key.')
    parser.add_argument('sink_bucket', help='Sink bucket name.')

    args = parser.parse_args()
    date = datetime.datetime.strptime(args.date, '%Y/%m/%d')
    time = datetime.datetime.strptime(args.time, '%H:%M')

    main(
        args.description,
        args.project_id,
        date.year,
        date.month,
        date.day,
        time.hour,
        time.minute,
        args.source_bucket,
        args.access_key,
        args.secret_access_key,
        args.sink_bucket)
# [END all]
