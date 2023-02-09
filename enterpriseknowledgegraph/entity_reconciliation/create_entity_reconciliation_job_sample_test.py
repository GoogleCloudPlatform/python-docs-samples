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

from google.api_core.exceptions import ResourceExhausted
from google.cloud import enterpriseknowledgegraph as ekg

import create_entity_reconciliation_job_sample

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "global"
input_dataset = "ekg_entity_reconciliation"
input_table = "patients"
mapping_file_uri = "gs://cloud-samples-data/ekg/quickstart/test_mapping1.yml"
entity_type = ekg.InputConfig.EntityType.PERSON
output_dataset = "ekg_entity_reconciliation"


def test_create_entity_reconciliation_job(capsys):

    try:
        create_entity_reconciliation_job_sample.create_entity_reconciliation_job_sample(
            project_id=project_id,
            location=location,
            input_dataset=input_dataset,
            input_table=input_table,
            mapping_file_uri=mapping_file_uri,
            entity_type=entity_type,
            output_dataset=output_dataset,
        )
    except (ResourceExhausted) as e:
        # Quota for simultaneous jobs is 2
        print(e.message)

    out, _ = capsys.readouterr()

    assert "Job: projects/" in out or "Resource Exhausted" in out
