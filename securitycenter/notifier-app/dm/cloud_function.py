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

"""Cloud Function (nicely deployed in deployment) DM template."""

def GenerateConfig(ctx):
  """Generate YAML resource configuration."""
  function_name = ctx.properties['function_name']
  bucket_name = ctx.properties['bucket']
  source_url = 'gs://{}/{}.zip'.format(bucket_name, function_name)

  cloud_function = {
    'type': 'gcp-types/cloudfunctions-v1beta2:projects.locations.functions',
    'name': function_name + '_cf',
    'properties': {
      'location': ctx.properties['region'],
      'function': function_name,
      'sourceArchiveUrl': source_url,
      'httpsTrigger': {},
      'timeout': '180s',
      'availableMemoryMb': 256
    }
  }
  resources = [cloud_function]

  return {'resources': resources}
