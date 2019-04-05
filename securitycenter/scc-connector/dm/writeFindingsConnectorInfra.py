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
        'name': 'flushbuffer',
        'type': 'pubsub_topic.py'
    }, {
        'name': 'configuration',
        'type': 'pubsub_topic.py'
    }, {
        'name': 'translation',
        'type': 'pubsub_topic.py'
    }, {
        'name': 'forwardfilelink',
        'type': 'pubsub_topic.py'
    }, {
        'name': 'configuration_function',
        'type': 'cloud_function.py',
        'properties': {
            'region': region,
            'topic': 'configuration',
            'function_name': 'configuration',
            'entryPoint': 'saveConfiguration',
            'bucket': cf_bucket,
        }
    }, {
        'name': 'flushbuffer_function',
        'type': 'cloud_function.py',
        'properties': {
            'region': region,
            'topic': 'flushbuffer',
            'function_name': 'flushbuffer',
            'entryPoint': 'flushBuffer',
            'bucket': cf_bucket,
        }
    }, {
        'name': 'forwardfilelink_function',
        'type': 'cloud_function.py',
        'properties': {
            'region': region,
            'topic': 'forwardfilelink',
            'function_name': 'forwardfilelink',
            'entryPoint': 'subscribeFindings',
            'bucket': cf_bucket,
        }
    }, {
        'name': 'translation_function',
        'type': 'cloud_function.py',
        'properties': {
            'region': region,
            'topic': 'translation',
            'function_name': 'translation',
            'entryPoint': 'translate',
            'bucket': cf_bucket,
        }
    }, {
        'name': 'cleanup_function',
        'type': 'cloud_function.py',
        'properties': {
            'region': region,
            'topic': 'cleanup',
            'function_name': 'cleanup',
            'entryPoint': 'cleanUp',
            'bucket': cf_bucket,
        }

    }]
    return {'resources': resources}
