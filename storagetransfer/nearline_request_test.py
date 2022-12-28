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

from datetime import datetime

import backoff
from google.api_core.exceptions import RetryError
from google.cloud.storage import Bucket
from googleapiclient.errors import HttpError

import nearline_request
import nearline_request_apiary


@backoff.on_exception(backoff.expo, (RetryError,), max_time=60)
def test_nearline_request(
        capsys, project_id: str, source_bucket: Bucket,
        destination_bucket: Bucket, job_description_unique: str):

    nearline_request.create_daily_nearline_30_day_migration(
        project_id=project_id,
        description=job_description_unique,
        source_bucket=source_bucket.name,
        sink_bucket=destination_bucket.name,
        start_date=datetime.utcnow()
    )

    out, _ = capsys.readouterr()

    assert "Created transferJob" in out


@backoff.on_exception(backoff.expo, (HttpError,), max_time=60)
def test_nearline_request_apiary(
        capsys, project_id: str, source_bucket: Bucket,
        destination_bucket: Bucket, job_description_unique: str):
    nearline_request_apiary.main(
        description=job_description_unique,
        project_id=project_id,
        start_date=datetime.utcnow(),
        start_time=datetime.utcnow(),
        source_bucket=source_bucket.name,
        sink_bucket=destination_bucket.name
    )

    out, _ = capsys.readouterr()

    assert "Returned transferJob" in out
