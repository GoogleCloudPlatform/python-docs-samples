# Copyright 2022 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import backoff
from google.api_core.exceptions import RetryError
from google.api_core.exceptions import ServiceUnavailable
from google.cloud.storage import Bucket

import azure_request


@backoff.on_exception(backoff.expo, (RetryError, ServiceUnavailable,),
                      max_time=60)
def test_azure_request(
        capsys, project_id: str, azure_storage_account: str,
        azure_sas_token: str, azure_source_container: str,
        destination_bucket: Bucket, job_description_unique: str):

    azure_request.create_one_time_azure_transfer(
        project_id=project_id,
        description=job_description_unique,
        azure_storage_account=azure_storage_account,
        azure_sas_token=azure_sas_token,
        source_container=azure_source_container,
        sink_bucket=destination_bucket.name)

    out, _ = capsys.readouterr()

    # Ensure the transferJob has been created
    assert "Created transferJob:" in out
