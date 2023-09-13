# Copyright 2023 Google LLC

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

import event_driven_aws_transfer


@backoff.on_exception(
    backoff.expo,
    (
        RetryError,
        ServiceUnavailable,
    ),
    max_time=60,
)
def test_event_driven_aws_transfer(
    capsys,
    project_id: str,
    job_description_unique: str,
    aws_source_bucket: str,
    destination_bucket: Bucket,
    sqs_queue_arn: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
):
    event_driven_aws_transfer.create_event_driven_aws_transfer(
        project_id=project_id,
        description=job_description_unique,
        source_s3_bucket=aws_source_bucket,
        sink_gcs_bucket=destination_bucket.name,
        sqs_queue_arn=sqs_queue_arn,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    out, _ = capsys.readouterr()

    # Ensure the transferJob has been created
    assert "Created transferJob:" in out
