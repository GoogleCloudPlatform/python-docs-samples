# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import json
from unittest.mock import Mock, patch
import uuid

# Assuming your code is in a file named 'programmatic_retries.py'
import programmatic_retries


@patch("programmatic_retries.requests.post")
@patch("programmatic_retries.google.auth.default")
@patch("uuid.uuid4")
def test_retry_success(mock_uuid, mock_auth_default, mock_requests_post):
    # Mocking UUID to have a predictable result
    mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")

    # Mocking Google Auth
    mock_credentials = Mock()
    mock_credentials.token = "test_token"
    mock_auth_default.return_value = (mock_credentials, "test_project")

    # Mocking the BigQuery API response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_requests_post.return_value = mock_response

    # Sample Pub/Sub message data (mimicking a failed continuous query)
    end_time = "2025-03-06T10:00:00Z"
    sql_query = "SELECT * FROM APPENDS(TABLE `test.table`, CURRENT_TIMESTAMP() - INTERVAL 10 MINUTE) WHERE TRUE"

    failed_job_id = "projects/test_project/jobs/failed_job_123"

    log_entry = {
        "protoPayload": {
            "metadata": {
                "jobChange": {
                    "job": {
                        "jobConfig": {"queryConfig": {"query": sql_query}},
                        "jobStats": {"endTime": end_time},
                        "jobName": failed_job_id,
                    }
                }
            }
        }
    }

    # Encode the log entry as a Pub/Sub message
    event = {
        "data": base64.b64encode(json.dumps(log_entry).encode("utf-8")).decode("utf-8")
    }

    # Call the Cloud Function
    programmatic_retries.retry_continuous_query(event, None)

    # Print the new SQL query
    new_query = mock_requests_post.call_args[1]["json"]["configuration"]["query"][
        "query"
    ]
    print(f"\nNew SQL Query:\n{new_query}\n")

    # Assertions
    mock_requests_post.assert_called_once()
    assert end_time in new_query
    assert (
        "CUSTOM_JOB_ID_PREFIX12345678"
        in mock_requests_post.call_args[1]["json"]["jobReference"]["jobId"]
    )
