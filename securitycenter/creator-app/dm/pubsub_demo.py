# Copyright 2017 Google Inc. All rights reserved.
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

"""Creates a Google PubSub Topic."""


def GenerateConfig(context):
    """Creates a Google PubSub Topic."""
    topic_name = context.env['name']
    project = context.properties['project-name']
    endpoint = context.properties['endpoint-url']
    resources = [
        {
            'name': topic_name,
            'type': 'pubsub.v1.topic',
            'properties': {
                'topic': topic_name
            }
        },
        {
            'name': 'demomodesubscriber',
            'type': 'pubsub.v1.subscription',
            'metadata': {
                'dependsOn': [topic_name]
            },
            'properties': {
                'subscription': 'demomode',
                'topic': 'projects/{}/topics/{}'.format(project, topic_name),
                'pushConfig': {
                    'pushEndpoint': endpoint
                },
                'ackDeadlineSeconds': 300
            }
        }
    ]
    return {'resources': resources}
