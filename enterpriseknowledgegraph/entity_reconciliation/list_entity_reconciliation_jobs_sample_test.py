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

import list_entity_reconciliation_jobs_sample

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "global"


def test_list_entity_reconciliation_jobs(capsys):
    list_entity_reconciliation_jobs_sample.list_entity_reconciliation_jobs_sample(
        project_id=project_id, location=location
    )

    out, _ = capsys.readouterr()

    assert "Job: projects/" in out
    assert "Input Table: projects/" in out
    assert "Output Dataset: projects/" in out
    assert "State:" in out
