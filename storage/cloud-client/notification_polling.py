#!/usr/bin/env python

# Copyright 2017 Google Inc. All rights reserved.
#
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

"""This application demonstrates how to poll for GCS notifications from a
Cloud Pub/Sub subscription, parse the incoming message, and acknowledge the
successful processing of the message.

This application will work with any subscription configured for pull rather
than push notifications. If you do not already have notifications configured,
you may consult the docs at
https://cloud.google.com/storage/docs/reporting-changes or follow the steps
below:

1. Activate the Google Cloud Pub/Sub API, if you have not already done so.
   https://console.cloud.google.com/flows/enableapi?apiid=pubsub

2. Create a Google Cloud Storage bucket:
   $ gsutil mb gs://testbucket

3. Create a Cloud Pub/Sub topic and publish bucket notifications there:
   $ gsutil notification create -f json -t testtopic gs://testbucket

4. Create a subscription for your new topic:
   $ gcloud beta pubsub subscriptions create testsubscription --topic=testtopic

5. Run this program:
   $ python notification_polling testsubscription

6. While the program is running, upload and delete some files in the testbucket
   bucket (you could use the console or gsutil) and watch as changes scroll by
   in the app.
"""

import argparse
import json
import sys

from google.cloud import pubsub


def summarize(message):
    # [START parse_message]
    data = message.data
    attributes = message.attributes

    event_type = attributes['eventType']
    bucket_id = attributes['bucketId']
    object_id = attributes['objectId']
    generation = attributes['objectGeneration']
    description = (
        '\tEvent type: {event_type}\n'
        '\tBucket ID: {bucket_id}\n'
        '\tObject ID: {object_id}\n'
        '\tGeneration: {generation}\n').format(
            event_type=event_type,
            bucket_id=bucket_id,
            object_id=object_id,
            generation=generation)

    payload_format = attributes['payloadFormat']
    if payload_format == 'JSON_API_V1':
        object_metadata = json.loads(data)
        size = object_metadata['size']
        content_type = object_metadata['contentType']
        metageneration = object_metadata['metageneration']
        description += (
            '\tContent type: {content_type}\n'
            '\tSize: {object_size}\n'
            '\tMetageneration: {metageneration}\n').format(
                content_type=content_type,
                object_size=size,
                metageneration=metageneration)
    return description
    # [END parse_message]


def poll_notifications(subscription_id):
    """Polls a Cloud Pub/Sub subscription for new GCS events for display."""
    # [BEGIN poll_notifications]
    client = pubsub.Client()
    subscription = pubsub.subscription.Subscription(
        subscription_id, client=client)

    if not subscription.exists():
        sys.stderr.write('Cannot find subscription {0}\n'.format(sys.argv[1]))
        return

    print('Polling for messages. Press ctrl+c to exit.')
    while True:
        pulled = subscription.pull(max_messages=100)
        for ack_id, message in pulled:
            print('Received message {0}:\n{1}'.format(
                message.message_id, summarize(message)))
            subscription.acknowledge([ack_id])
    # [END poll_notifications]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__)
    parser.add_argument('subscription',
                        help='The ID of the Pub/Sub subscription')
    args = parser.parse_args()
    poll_notifications(args.subscription)
