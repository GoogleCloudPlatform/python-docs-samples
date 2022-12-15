# Copyright 2022 Google LLC
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
#

import os

from google.api_core.exceptions import InvalidArgument, NotFound

import delete_entity_reconciliation_job_sample

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "global"
job_id = "5285051433452986164"


def test_delete_entity_reconciliation_job(capsys):
    try:
        delete_entity_reconciliation_job_sample.delete_entity_reconciliation_job_sample(
            project_id=project_id, location=location, job_id=job_id
        )
    except (InvalidArgument, NotFound) as e:
        print(e.message)

    out, _ = capsys.readouterr()

    assert "projects/" in out
