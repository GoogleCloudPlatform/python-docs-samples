# Copyright 2023 Google LLC
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

from discoveryengine import import_documents_sample
from discoveryengine import list_documents_sample

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "global"
search_engine_id = "test-structured-data-engine"
gcs_uri = "gs://cloud-samples-data/gen-app-builder/search/empty.json"

# Empty Dataset
bigquery_dataset = "genappbuilder_test"
bigquery_table = "import_documents_test"


def test_import_documents_gcs(capsys):
    import_documents_sample.import_documents_sample(
        project_id=project_id,
        location=location,
        search_engine_id=search_engine_id,
        gcs_uri=gcs_uri,
    )

    out, _ = capsys.readouterr()

    assert "operations/import-documents" in out


def test_import_documents_bigquery(capsys):
    import_documents_sample.import_documents_sample(
        project_id=project_id,
        location=location,
        search_engine_id=search_engine_id,
        bigquery_dataset=bigquery_dataset,
        bigquery_table=bigquery_table,
    )

    out, _ = capsys.readouterr()

    assert "operations/import-documents" in out


def test_list_documents(capsys):
    list_documents_sample.list_documents_sample(
        project_id=project_id,
        location=location,
        search_engine_id=search_engine_id,
    )

    out, _ = capsys.readouterr()

    assert f"Documents in {search_engine_id}" in out
