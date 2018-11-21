# Copyright 2016 Google LLC
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

import custom_roles


def test_custom_roles(capsys):
    project = os.environ['GCLOUD_PROJECT']
    name = 'pythonTestCustomRole' + str(random.randint(0, 100000))
    title = 'Python Test Custom Role'
    description = 'This is a Python test custom role.'
    permissions = ['iam.roles.get']
    stage = 'GA'

    custom_roles.query_testable_permissions(
        '//cloudresourcemanager.googleapis.com/projects/' + project
    )
    out, _ = capsys.readouterr()
    assert 'appengine' in out

    custom_roles.get_role('roles/appengine.appViewer')
    out, _ = capsys.readouterr()
    assert 'roles/' in out

    custom_roles.create_role(
        name, project, title, description, permissions, stage)
    out, _ = capsys.readouterr()
    assert 'Created role:' in out

    custom_roles.edit_role(name, project, title, 'Updated', permissions, stage)
    out, _ = capsys.readouterr()
    assert 'Updated role:' in out

    custom_roles.list_roles(project)
    out, _ = capsys.readouterr()
    assert 'roles/' in out

    custom_roles.disable_role(name, project)
    out, _ = capsys.readouterr()
    assert 'Disabled role:' in out

    custom_roles.delete_role(name, project)
    out, _ = capsys.readouterr()
    assert 'Deleted role:' in out


if __name__ == '__main__':
    test_custom_roles()
