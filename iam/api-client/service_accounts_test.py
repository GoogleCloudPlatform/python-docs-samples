# Copyright 2016 Google Inc. All Rights Reserved.
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

import os
import random

import service_accounts


def test_service_accounts(capsys):
    project_id = os.environ['GCLOUD_PROJECT']
    rand = str(random.randint(0, 1000))
    name = 'python-test-' + rand
    email = name + '@' + project_id + '.iam.gserviceaccount.com'

    service_accounts.create_service_account(
        project_id, name, 'Py Test Account')
    service_accounts.list_service_accounts(
        project_id)
    service_accounts.rename_service_account(
        email, 'Updated Py Test Account')
    service_accounts.disable_service_account(
        email)
    service_accounts.enable_service_account(
        email)
    service_accounts.delete_service_account(
        email)
