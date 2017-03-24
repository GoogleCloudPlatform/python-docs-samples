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

"""This application demonstrates how to poll a Google Cloud Pub/Sub
subscription for notification messages, parse those messages, and
acknowledge successful handling of them.

For more information, see the README.md file in this directory or the
docs at https://cloud.google.com/storage/docs/pubsub-notifications

Example usage:
  python notification_poller.py bucketsubscription
"""

from __future__ import print_function

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
DUPLICATION_KEY = '{event_type}|{resource}|{generation}|{metageneration}'


class GcsEvent(object):
    """Represents a single event message from GCS."""

    def __init__(self, message):
        """Initializes a GcsEvent with a Pub/Sub message."""
        # [START parse_message]
        data = message.data
        attributes = message.attributes

        # The kind of event that just happened. Example: OBJECT_FINALIZE
        self.event_type = attributes['eventType']

        # ID of the bucket. Example: "my_photos"
        self.bucket_id = attributes['bucketId']

        # The ID of the affected objet. Example: "image.jpeg"
        self.object_id = attributes['objectId']

        # Generation of the object. Example: 1234567
        self.generation = attributes['objectGeneration']

        # The full resource name of the object.
        # Example: projects/_/buckets/my_photos/objects/image.jpeg
        self.object_name = attributes['resource']

        # Format of the attached payload. Example: JSON_API_V1
        self.payload_format = attributes['payloadFormat']

        # ID of the notification configuration responsible for this event.
        # Example: projects/_/buckets/my_photos/notificationConfigs/1
        self.notification_config = attributes['notificationConfig']

        if self.payload_format == 'JSON_API_V1':
            # The payload is the JSON API object resource.
            self.object_metadata = json.loads(data)
            self.object_size = self.object_metadata['size']
            self.content_type = self.object_metadata['contentType']
            self.metageneration = self.object_metadata['metageneration']
        elif self.payload_format == 'NONE':
            # There is no payload.
            self.object_metadata = None
            self.metageneration = None
        else:
            print('Unknown payload format %s', self.payload_format)
            self.object_metadata = None
            self.metageneration = None
        # [END parse_message]

    def Summary(self):
        """Returns a one line summary of the event."""
        return '%s - %s/%s' % (
            ACTION_STRINGS.get(
                self.event_type, 'Unknown event %s' % self.event_type),
            self.bucket_id,
            self.object_id)

    def __unicode__(self):
        description = (
            '{summary}\n'
            '\tGeneration: {generation}\n').format(
                summary=self.Summary(),
                bucket_id=self.bucket_id,
                object_id=self.object_id,
                generation=self.generation)
        if self.object_metadata:
            description += (
                '\tContent type: {content_type}\n'
                '\tSize: {object_size}\n').format(
                    content_type=self.content_type,
                    object_size=self.object_size)
        return description

    def dup_string(self):
        """Returns a string unique to this specific event."""
        # GCS will publish each notification at least once to a Cloud Pub/Sub
        # topic, and Cloud Pub/Sub will deliver each message to each
        # subscription at least once. We must be able to safely handle
        # occasionally receiving duplicate messages.
        return DUPLICATION_KEY.format(
            event_type=self.event_type,
            resource=self.object_name,
            generation=self.generation,
            metageneration=self.metageneration)


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
            event = GcsEvent(message)
            if event.dup_string() in DUPLICATE_EVENT_CACHE:
                print('[DUPLICATE] %s' % event.Summary())
            else:
                DUPLICATE_EVENT_CACHE[event.dup_string()] = 1
                print(unicode(event))
            subscription.acknowledge([ack_id])
