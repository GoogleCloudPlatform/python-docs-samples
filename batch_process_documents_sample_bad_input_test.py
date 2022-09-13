# Copyright 2020 Google LLC
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
from uuid import uuid4

from samples.snippets import batch_process_documents_sample

location = "us"
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
processor_id = "90484cfdedb024f6"
gcs_input_uri = "gs://cloud-samples-data/documentai/invoice.pdf"
input_mime_type = "application/pdf"
# following bucket contains .csv file which will cause the sample to fail.
gcs_output_full_uri_with_wrong_type = "gs://documentai-beta-samples"
gcs_output_uri_prefix = "test"
BUCKET_NAME = f"document-ai-python-{uuid4()}"


def test_batch_process_documents_with_bad_input(capsys):
    try:
        batch_process_documents_sample.batch_process_documents(
            project_id=project_id,
            location=location,
            processor_id=processor_id,
            gcs_input_uri=gcs_input_uri,
            input_mime_type=input_mime_type,
            gcs_output_bucket=gcs_output_full_uri_with_wrong_type,
            gcs_output_uri_prefix=gcs_output_uri_prefix,
            timeout=450,
        )
        out, _ = capsys.readouterr()
        assert "Failed" in out
    except Exception as e:
        assert "Internal error" in e.message
