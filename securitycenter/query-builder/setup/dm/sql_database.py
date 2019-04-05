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
"""Creates a sql database."""


def GenerateConfig(context):
    """Generate Deployment Manager configuration.

    Args:
      context: The context object provided by Deployment Manager.

    Returns:
      A config object for Deployment Manager (basically a dict with resources).
    """

    # Basic database
    resources = [{
        'name': context.properties['name'],
        'type': 'sqladmin.v1beta4.database',
        'properties': {
            'name': context.properties['name'],
            'instance': context.properties['instance'],
            'charset': context.properties['charset']
        }
    }]

    if context.properties['depends']:
        dependency = {
            'dependsOn': context.properties['depends']
        }
        resources[0]['metadata'] = dependency

    return {
        'resources': resources
    }
