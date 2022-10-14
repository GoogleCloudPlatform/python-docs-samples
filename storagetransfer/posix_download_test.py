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

import posix_download


@backoff.on_exception(backoff.expo, (RetryError, ServiceUnavailable,), max_time=60)
def test_posix_download(
        capsys, project_id: str, job_description_unique: str,
        agent_pool_name: str, posix_root_directory: str,
        source_bucket: Bucket):

    posix_download.download_from_gcs(
        project_id=project_id,
        description=job_description_unique,
        sink_agent_pool_name=agent_pool_name,
        root_directory=posix_root_directory,
        source_bucket=source_bucket.name,
        gcs_source_path=posix_root_directory
    )

    out, _ = capsys.readouterr()

    assert "Created transferJob" in out
