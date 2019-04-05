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

"""Creates a Google Cloud Storage Bucket."""


def GenerateConfig(context):
    """Creates a Google Cloud Storage Bucket."""

    location = context.properties['location']
    bucket_name = context.properties['bucketname']
    storage_class = context.properties['storageClass']

    resources = [{
        'name': bucket_name,
        'type': 'storage.v1.bucket',
        'properties': {
            'storageClass': storage_class,
            'location': location,
            'name': bucket_name
        }
    }]
    return {'resources': resources}
