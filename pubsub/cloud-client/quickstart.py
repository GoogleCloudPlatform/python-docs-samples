#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
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


def run_quickstart():
    # [START pubsub_quickstart]
    # Imports the Google Cloud client library
    from google.cloud import pubsub_v1

    # Instantiates a client
    publisher = pubsub_v1.PublisherClient()

    # The resource path for the new topic contains the project ID
    # and the topic name.
    topic_path = publisher.topic_path(
        'my-project', 'my-new-topic')

    # Create the topic.
    topic = publisher.create_topic(topic_path)

    print('Topic created: {}'.format(topic))
    # [END pubsub_quickstart]


if __name__ == '__main__':
    run_quickstart()
