#!/usr/bin/env python

# Copyright 2018 Google LLC All Rights Reserved.
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

# [START quickstart]
import os

from googleapiclient.discovery import build
from googleapiclient.errors import Error

client_service = build('jobs', 'v3')


def run_sample():
    try:
        project_id = 'projects/' + os.environ['GOOGLE_CLOUD_PROJECT']
        response = client_service.projects().companies().list(
            parent=project_id).execute()
        print('Request Id: %s' %
              response.get('metadata').get('requestId'))
        print('Companies:')
        if response.get('companies') is not None:
            for company in response.get('companies'):
                print('%s' % company.get('name'))
        print('')

    except Error as e:
        print('Got exception while listing companies')
        raise e


if __name__ == '__main__':
    run_sample()
# [END quickstart]
