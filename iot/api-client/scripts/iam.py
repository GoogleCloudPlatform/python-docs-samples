#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
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

"""This application demonstrates how programatically grant access to the
Cloud IoT Core service account on a given PubSub topic.

For more information, see https://cloud.google.com/iot.
"""

import argparse

from google.cloud import pubsub


def set_topic_policy(topic_name):
    """Sets the IAM policy for a topic for Cloud IoT Core."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)
    policy = topic.get_iam_policy()

    # Add a group as publishers.
    publishers = policy.get('roles/pubsub.publisher', [])
    publishers.append(policy.service_account(
            'cloud-iot@system.gserviceaccount.com'))
    policy['roles/pubsub.publisher'] = publishers

    # Set the policy
    topic.set_iam_policy(policy)

    print(f'IAM policy for topic {topic.name} set.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_argument(
            dest='topic_name',
            help='The PubSub topic to grant Cloud IoT Core access to')

    args = parser.parse_args()

    set_topic_policy(args.topic_name)
