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
"""Creates the Auth config editor custom role."""


def GenerateConfig(context):
  """Generate Deployment Manager configuration.

  Args:
    context: The context object provided by Deployment Manager.

  Returns:
    A config object for Deployment Manager (basically a dict with resources).
  """
  
  # Custom IAM Role
  resources = [{
      'name': 'custom-gae-app-creator-role',
      'type': 'gcp-types/iam-v1:organizations.roles',
      'properties': {
          'parent': 'organizations/'+ context.properties['organizationId'],
          'roleId': 'custom.gaeAppCreator',
          'role' : {
              'title': 'CR - Google App Engine Application Creator',
              'description': 'Custom role to Create Google App Engine Applications.',
              'stage': 'BETA',
              'includedPermissions':[
                  'appengine.applications.create',
              ]

          }
      }
  }]

  return {
      'resources': resources
  }
