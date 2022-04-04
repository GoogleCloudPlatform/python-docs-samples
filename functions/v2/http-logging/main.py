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
# [START functions_structured_logging]
import google.cloud.logging
from google.cloud.logging.handlers import StructuredLogHandler
from google.cloud.logging_v2.handlers import setup_logging

def structured_logging(request):
    logging_client = google.cloud.logging.Client()

    handler = StructuredLogHandler()
    setup_logging(handler)

    logger = logging_client.logger("New-Structured-Log")

    msg = (f"{request.headers}"
           f"{request.get_data().decode()}"
           )

    # Write structured log with HTTP request data
    logger.log_struct(
        {
            "message": "Hello, world!",
            "severity": "NOTICE",
            "component": "arbitrary-property",
            "httpRequest": msg
        }
    )

    print("Wrote logs to {}.".format(logger.name))
    return "Hello, world!"

# [END functions_structured_logging]
