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

"""Creates a Google PubSub Subscriber."""


def GenerateConfig(context):
    """Creates a Google PubSub Subscriber."""

    name = context.env['name']
    topic_name = context.properties['topic_name']
    endpoint_url = context.properties['endpoint_url']

    resources = [{
        'name': name,
        'type': 'pubsub.v1.subscription',
        'metadata': {
            'dependsOn': [topic_name]
        },
        'properties': {
            'subscription': name,
            'topic': 'projects/' + context.env['project'] + '/topics/' + topic_name,
            'ackDeadlineSeconds': 10,
            'pushConfig': {
                'pushEndpoint': endpoint_url
            }
        }
    }]
    return {'resources': resources}
