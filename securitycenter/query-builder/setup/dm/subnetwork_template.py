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
"""Creates a subnetwork."""


def GenerateConfig(context):
    """Generate Deployment Manager configuration.

    Args:
      context: The context object provided by Deployment Manager.

    Returns:
      A config object for Deployment Manager (basically a dict with resources).
    """
    network_ref = '$(ref.{}.selfLink)'.format(context.properties['network'])

    # Subnetwork creation
    resources = [{
        'name': context.env['name'],
        'type': 'compute.v1.subnetwork',
        'properties': {
            'region': context.properties['region'],
            'privateIpGoogleAccess': True,
            'ipCidrRange': context.properties['ipRange'],
            'network': network_ref
        }
    }]

    if context.properties.get('secondaryIpRanges'):
        secondary_ranges = []
        for secondary_range in context.properties['secondaryIpRanges']:
            secondary_ranges.append({
                'rangeName': secondary_range['rangeName'],
                'ipCidrRange': secondary_range['ipCidrRange'],
            })
        resources[0]['properties']['secondaryIpRanges'] = secondary_ranges

    return {
        'resources': resources
    }
