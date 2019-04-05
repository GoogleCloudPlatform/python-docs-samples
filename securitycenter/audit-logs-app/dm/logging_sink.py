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

"""Creates a Google Stackdriver Export Sink."""


def GenerateConfig(context):
    """Creates a Google Stackdriver Export Sink."""

    organization_id = context.properties['organization_id']
    sink_name = context.properties['sink_name']
    _filter = context.properties['filter']
    destination = context.properties['destination']

    resources = [{
        'name': sink_name,
        'type': 'gcp-types/logging-v2:organizations.sinks',
        'properties': {
            'organization': organization_id,
            'sink': sink_name,
            'includeChildren': True,
            'filter': _filter,
            'destination' : destination
        }
    }]
    outputs = [{
        'name': 'writer_identity',
        'value': '$(ref.{}.writerIdentity)'.format(sink_name)
    }]

    return {
        'resources': resources,
        'outputs': outputs
    }
