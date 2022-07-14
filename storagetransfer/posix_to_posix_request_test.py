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

import posix_to_posix_request


@backoff.on_exception(backoff.expo, (RetryError, ServiceUnavailable,), max_time=60)
def test_posix_to_posix_request(
        capsys, project_id: str, job_description_unique: str,
        agent_pool_name: str, posix_root_directory: str,
        intermediate_bucket: Bucket):

    # The agent pool associated with the POSIX data source.
    # Defaults to 'projects/{project_id}/agentPools/transfer_service_default'
    # source_agent_pool_name = 'projects/my-project/agentPools/my-agent'

    # The agent pool associated with the POSIX data sink.
    # Defaults to 'projects/{project_id}/agentPools/transfer_service_default'
    # sink_agent_pool_name = 'projects/my-project/agentPools/my-agent'

    # The root directory path on the source filesystem
    # root_directory = '/directory/to/transfer/source'

    # The root directory path on the destination filesystem
    # destination_directory = '/directory/to/transfer/sink'

    # The Google Cloud Storage bucket for intermediate storage
    # intermediate_bucket = 'my-intermediate-bucket'

    posix_to_posix_request.transfer_between_posix(
        project_id=project_id,
        description=job_description_unique,
        source_agent_pool_name=agent_pool_name,
        sink_agent_pool_name=agent_pool_name,
        root_directory=posix_root_directory,
        destination_directory=posix_root_directory,
        intermediate_bucket=intermediate_bucket.name
    )

    out, _ = capsys.readouterr()

    assert "Created transferJob" in out
