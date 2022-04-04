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
#
# [START functions_structured_logging_event]
import functions_framework
import google.cloud.logging
from google.cloud.logging.handlers import StructuredLogHandler
from google.cloud.logging_v2.handlers import setup_logging


@functions_framework.cloud_event
def structured_logging_event(cloud_event):
    logging_client = google.cloud.logging.Client()

    handler = StructuredLogHandler()
    setup_logging(handler)

    logger = logging_client.logger("New-Structured-Log")

    # Write structured log with CloudEvent data
    logger.log_struct(
        {
            "message": "Hello, world!",
            "severity": "NOTICE",
            "component": "arbitrary-property",
            "cloudEvent": cloud_event.__dict__
        }
    )

    print("Wrote logs to {}.".format(logger.name))

# [END functions_structured_logging_event]
