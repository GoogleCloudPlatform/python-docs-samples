# Copyright 2021 Google LLC

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

import datetime

import backoff
from google.api_core.exceptions import RetryError
from google.api_core.exceptions import ServiceUnavailable
from google.cloud.storage import Bucket
from googleapiclient.errors import HttpError

import aws_request
import aws_request_apiary


@backoff.on_exception(backoff.expo, (RetryError, ServiceUnavailable,),
                      max_time=60)
def test_aws_request(
        capsys, project_id: str, aws_source_bucket: str,
        aws_access_key_id: str, aws_secret_access_key: str,
        destination_bucket: Bucket, job_description_unique: str):

    aws_request.create_one_time_aws_transfer(
        project_id=project_id,
        description=job_description_unique,
        source_bucket=aws_source_bucket,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        sink_bucket=destination_bucket.name)

    out, _ = capsys.readouterr()

    # Ensure the transferJob has been created
    assert "Created transferJob:" in out


@backoff.on_exception(backoff.expo, (HttpError,), max_time=60)
def test_aws_request_apiary(
        capsys, project_id: str, aws_source_bucket: str,
        aws_access_key_id: str, aws_secret_access_key: str,
        destination_bucket: Bucket, job_description_unique: str):
    aws_request_apiary.main(
        description=job_description_unique,
        project_id=project_id,
        start_date=datetime.datetime.utcnow(),
        start_time=datetime.datetime.utcnow(),
        source_bucket=aws_source_bucket,
        access_key_id=aws_access_key_id,
        secret_access_key=aws_secret_access_key,
        sink_bucket=destination_bucket.name
    )

    out, _ = capsys.readouterr()

    # Ensure the transferJob has been created
    assert "Returned transferJob:" in out
