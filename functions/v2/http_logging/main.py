# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_structured_logging]
import logging

import functions_framework
from google.cloud.logging import Client


@functions_framework.http
def structured_logging(request):
    # Initialize the Google Cloud logging client
    cloud_logging_client = Client()
    # Set up a Log Handler that exports logs in JSON format to stdout
    # when running in a serverless environment.
    # To manually set up a Structured Log Handler, see
    # https://googleapis.dev/python/logging/latest/handlers-structured-log.html
    cloud_logging_client.setup_logging()

    # Construct log message and additional metadata
    # https://cloud.google.com/run/docs/logging#using-json
    msg = "Hello, world!"
    metadata = {"component": "arbitrary-property"}

    # Write structured log with additional component fields
    # HTTP request data is attached automatically for request-log correlation
    logging.info(msg, extra={"json_fields": metadata})

    return "Success: A log message was written"

# [END functions_structured_logging]
