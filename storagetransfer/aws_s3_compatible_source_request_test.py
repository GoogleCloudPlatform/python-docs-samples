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
from google.cloud.storage.bucket import _API_ACCESS_ENDPOINT
from google.cloud.storage_transfer_v1.types import transfer_types

import aws_s3_compatible_source_request


@backoff.on_exception(backoff.expo, (RetryError, ServiceUnavailable,),
                      max_time=60)
def test_aws_s3_compatible_source_request(
    capsys,
    project_id: str,
    job_description_unique: str,
    agent_pool_name: str,
    source_bucket: Bucket,
    posix_root_directory: str,
    destination_bucket: Bucket
) -> None:

    AuthMethod = transfer_types.S3CompatibleMetadata.AuthMethod
    NetworkProtocol = transfer_types.S3CompatibleMetadata.NetworkProtocol
    RequestModel = transfer_types.S3CompatibleMetadata.RequestModel

    aws_s3_compatible_source_request.transfer_from_S3_compat_to_gcs(
        project_id=project_id,
        description=job_description_unique,
        source_agent_pool_name=agent_pool_name,
        source_bucket_name=source_bucket.name,
        source_path=posix_root_directory,
        gcs_sink_bucket=destination_bucket.name,
        gcs_path=posix_root_directory,
        region=source_bucket.location,
        endpoint=_API_ACCESS_ENDPOINT,
        protocol=NetworkProtocol.NETWORK_PROTOCOL_HTTPS,
        request_model=RequestModel.REQUEST_MODEL_VIRTUAL_HOSTED_STYLE,
        auth_method=AuthMethod.AUTH_METHOD_AWS_SIGNATURE_V4
    )

    out, _ = capsys.readouterr()

    assert "Created transferJob" in out
