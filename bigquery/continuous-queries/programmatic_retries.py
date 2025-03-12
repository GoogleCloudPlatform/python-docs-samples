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

# This code sample demonstrates one possible approach to automating query retry.
# Important things to consider when you retry a failed continuous query include the following:
#     - Whether reprocessing some amount of data processed by the previous query before it failed is tolerable.
#     - How to handle limiting retries or using exponential backoff.

# Make sure you provide your SERVICE_ACCOUNT and CUSTOM_JOB_ID_PREFIX.

# [START functions_bigquery_continuous_queries_programmatic_retry]
import base64
import json
import logging
import re
import uuid

import google.auth
import google.auth.transport.requests
import requests


def retry_continuous_query(event, context):
    logging.info("Cloud Function started.")

    if "data" not in event:
        logging.info("No data in Pub/Sub message.")
        return

    try:
        # [START functions_bigquery_retry_decode]
        # Decode and parse the Pub/Sub message data
        log_entry = json.loads(base64.b64decode(event["data"]).decode("utf-8"))
        # [END functions_bigquery_retry_decode]

        # [START functions_bigquery_retry_extract_query]
        # Extract the SQL query and other necessary data
        proto_payload = log_entry.get("protoPayload", {})
        metadata = proto_payload.get("metadata", {})
        job_change = metadata.get("jobChange", {})
        job = job_change.get("job", {})
        job_config = job.get("jobConfig", {})
        query_config = job_config.get("queryConfig", {})
        sql_query = query_config.get("query")
        job_stats = job.get("jobStats", {})
        end_timestamp = job_stats.get("endTime")
        failed_job_id = job.get("jobName")
        # [END functions_bigquery_retry_extract_query]

        # Check if required fields are missing
        if not all([sql_query, failed_job_id, end_timestamp]):
            logging.error("Required fields missing from log entry.")
            return

        logging.info(f"Retrying failed job: {failed_job_id}")

        # [START functions_bigquery_retry_adjust_timestamp]
        # Adjust the timestamp in the SQL query
        timestamp_match = re.search(
            r"\s*TIMESTAMP\(('.*?')\)(\s*\+ INTERVAL 1 MICROSECOND)?", sql_query
        )

        if timestamp_match:
            original_timestamp = timestamp_match.group(1)
            new_timestamp = f"'{end_timestamp}'"
            sql_query = sql_query.replace(original_timestamp, new_timestamp)
        elif "CURRENT_TIMESTAMP() - INTERVAL 10 MINUTE" in sql_query:
            new_timestamp = f"TIMESTAMP('{end_timestamp}') + INTERVAL 1 MICROSECOND"
            sql_query = sql_query.replace(
                "CURRENT_TIMESTAMP() - INTERVAL 10 MINUTE", new_timestamp
            )
        # [END functions_bigquery_retry_adjust_timestamp]

        # [START functions_bigquery_retry_api_call]
        # Get access token
        credentials, project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        access_token = credentials.token

        # API endpoint
        url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{project}/jobs"

        # Request headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        # Generate a random UUID
        random_suffix = str(uuid.uuid4())[:8]  # Take the first 8 characters of the UUID

        # Combine the prefix and random suffix
        job_id = f"CUSTOM_JOB_ID_PREFIX{random_suffix}"

        # Request payload
        data = {
            "configuration": {
                "query": {
                    "query": sql_query,
                    "useLegacySql": False,
                    "continuous": True,
                    "connectionProperties": [
                        {"key": "service_account", "value": "SERVICE_ACCOUNT"}
                    ],
                    # ... other query parameters ...
                },
                "labels": {"bqux_job_id_prefix": "CUSTOM_JOB_ID_PREFIX"},
            },
            "jobReference": {
                "projectId": project,
                "jobId": job_id,  # Use the generated job ID here
            },
        }

        # Make the API request
        response = requests.post(url, headers=headers, json=data)
        # [END functions_bigquery_retry_api_call]

        # [START functions_bigquery_retry_handle_response]
        # Handle the response
        if response.status_code == 200:
            logging.info("Query job successfully created.")
        else:
            logging.error(f"Error creating query job: {response.text}")
        # [END functions_bigquery_retry_handle_response]

    except Exception as e:
        logging.error(
            f"Error processing log entry or retrying query: {e}", exc_info=True
        )

    logging.info("Cloud Function finished.")


# [END functions_bigquery_continuous_queries_programmatic_retry]
