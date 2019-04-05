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

"""Creates the backend Environment."""


def GenerateConfig(context):
    """Creates backend properties to configure environment."""

    region = context.properties['region']
    cf_bucket = context.properties['cfbucket']

    resources = [{
        'name': 'entrypoint',
        'type': 'pubsub_topic.py'
    }, {
        'name': 'redirect',
        'type': 'pubsub_topic.py'
    }, {
        'name': 'transformer',
        'type': 'cloud_function.py',
        'properties': {
            'region': region,
            'topic': 'entrypoint',
            'function_name': 'transformer',
            'entryPoint': 'transform',
            'bucket': cf_bucket
        }
    }, {
        'name': 'logger',
        'type': 'cloud_function.py',
        'properties': {
            'region': region,
            'topic': 'redirect',
            'function_name': 'logger',
            'entryPoint': 'log',
            'bucket': cf_bucket
        }
    }]

    return {'resources': resources}
