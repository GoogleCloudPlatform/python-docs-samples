# Copyright 2018 Google LLC
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

import access
import service_accounts


def test_access(capsys):
    # Setting up variables for testing
    project_id = os.environ['GCLOUD_PROJECT']

    # specifying a sample role to be assigned
    gcp_role = 'roles/owner'

    # section to create service account to test policy updates.
    rand = str(random.randint(0, 1000))
    name = 'python-test-' + rand
    email = name + '@' + project_id + '.iam.gserviceaccount.com'
    member = 'serviceAccount:' + email
    service_accounts.create_service_account(
        project_id, name, 'Py Test Account')

    policy = access.get_policy(project_id)
    out, _ = capsys.readouterr()
    assert u'etag' in out

    policy = access.modify_policy_add_role(policy, gcp_role, member)
    out, _ = capsys.readouterr()
    assert u'etag' in out

    policy = access.modify_policy_remove_member(policy, gcp_role, member)
    out, _ = capsys.readouterr()
    assert 'iam.gserviceaccount.com' in out

    policy = access.set_policy(project_id, policy)
    out, _ = capsys.readouterr()
    assert u'etag' in out

    access.test_permissions(project_id)
    out, _ = capsys.readouterr()
    assert u'permissions' in out

    # deleting the service account created above
    service_accounts.delete_service_account(
        email)
