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
    bucket_name = context.properties['bucket_name']
    log_bucket_name = bucket_name + '_log'

    resources = [{
        'name': log_bucket_name,
        'type': 'storage.v1.bucket',
        'properties': {
            'storageClass': 'REGIONAL',
            'location': region,
            'name': log_bucket_name
        }
    }, {
        'name': bucket_name,
        'type': 'storage.v1.bucket',
        'properties': {
            'storageClass': 'REGIONAL',
            'location': region,
            'name': bucket_name,
            'logging': {
                'logBucket': '$(ref.{}.name)'.format(log_bucket_name),
                'logObjectPrefix': 'log-prefix',
            },
            'versioning': {
                'enabled': True,
            }
        }
    }]
    return {'resources': resources}