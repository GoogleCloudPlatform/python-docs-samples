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

1. [Activate the Google Cloud Pub/Sub API], if you have not already done so.
2. Create a Google Cloud Storage bucket:

    ```
    $ gsutil mb gs://testbucket
    ```

3. Create a Cloud Pub/Sub topic and publish bucket notifications there:

   ```
   $ gsutil notification create -f json -t testtopic gs://testbucket
   ```

4. Create a subscription for your new topic:

   ```
   $ gcloud beta pubsub subscriptions create testsubscription --topic=testtopic
   ```

5. Run this program:

   ```
   $ python notification_polling testsubscription`
   ```

6. While the program is running, upload and delete some files in the testbucket
   bucket (you could use the console or gsutil) and watch as changes scroll by
   in the app.
"""

import argparse
import json
import sys

from cachetools import LRUCache
from google.cloud import pubsub


ACTION_STRINGS = {
    'OBJECT_ARCHIVE': 'Object archived',
    'OBJECT_DELETE': 'Object deleted',
    'OBJECT_FINALIZE': 'Object created',
    'OBJECT_METADATA_UPDATE': 'Object metadata updated'
}


DUPLICATE_EVENT_CACHE = LRUCache(10000)
DUPLICATION_KEY = '{event_type}|{resource}|{metageneration}'


def Summarize(message):
    # [START parse_message]
    data = message.data
    attributes = message.attributes

    # The kind of event that just happened. Example: OBJECT_FINALIZE
    event_type = attributes['eventType']
    event_description = ACTION_STRINGS.get(
        event_type, 'Unknown Event %s' % event_type)

    # ID of the bucket. Example: "my_photos"
    bucket_id = attributes['bucketId']
    # The ID of the affected objet. Example: "image.jpeg"
    object_id = attributes['objectId']
    # Generation of the object. Example: 1234567
    generation = attributes['objectGeneration']
    # Format of the attached payload. Example: JSON_API_V1
    payload_format = attributes['payloadFormat']
    description = (
        '{summary} - {bucket_id}/{object_id}\n'
        '\tGeneration: {generation}\n').format(
            summary=event_description,
            bucket_id=bucket_id,
            object_id=object_id,
            generation=generation)

    if payload_format == 'JSON_API_V1':
        # The payload is the JSON API object resource.
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
    elif payload_format == 'NONE':
        # There is no payload.
        pass
    else:
        print('Unknown payload format %s', payload_format)
    return description
    # [END parse_message]


def GetDedupString(message):
    """Returns a string unique to this specific event."""
    # GCS will publish each notification at least once to a Cloud Pub/Sub
    # topic, and Cloud Pub/Sub will deliver each message to each
    # subscription at least once. We must be able to safely handle
    # occasionally receiving duplicate messages.
    metageneration = 'unknown'
    if message.attributes['payloadFormat'] == 'JSON_API_V1':
        metageneration = json.loads(message.data)['metageneration']
    return DUPLICATION_KEY.format(
        event_type=message.attributes['eventType'],
        resource=message.attributes['resource'],
        metageneration=metageneration)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__)
    parser.add_argument(
        '--project',
        help='The project of the subscription, if not in your default project')
    parser.add_argument('subscription',
                        help='The ID of the Pub/Sub subscription')
    args = parser.parse_args()

    subscription_id = args.subscription
    client = pubsub.Client(project=args.project)
    subscription = pubsub.subscription.Subscription(
        subscription_id, client=client)
    if not subscription.exists():
        sys.stderr.write('Cannot find subscription %s\n' % sys.argv[1])
        sys.exit(1)

    print('Polling for messages.')
    while True:
        pulled = subscription.pull(max_messages=100)
        for ack_id, message in pulled:
            dup_string = GetDedupString(message)
            summary = Summarize(message)
            if dup_string in DUPLICATE_EVENT_CACHE:
                print('[DUPLICATE] %s' % summary)
            else:
                DUPLICATE_EVENT_CACHE[dup_string] = 1
                print(summary)
            subscription.acknowledge([ack_id])
