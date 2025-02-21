# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from google.auth.transport import Response

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"


def send_evaluation_request_gapic() -> Response:
    # [START generativeaionvertexai_evaluation_example_syntax]
    import json

    from google import auth
    from google.auth.transport import requests as google_auth_requests

    # TODO(developer): Update & uncomment the lines below
    # PROJECT_ID = "your-project-id"
    # LOCATION = "us-central1"

    creds, _ = auth.default(
        scopes=['https://www.googleapis.com/auth/cloud-platform'],
    )

    # Check the API reference for details:
    # https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/evaluation#bleuinput
    data = {
        "bleu_input": {
            "metric_spec": {
                "use_effective_order": False,
            },
            "instances": [
                {
                    "prediction": "The quick brown fox jumps over the lazy dog",
                    "reference": "A fast brown fox leaps across the sleeping dog",
                }
            ]
        }
    }

    uri = f"https://{LOCATION}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{LOCATION}:evaluateInstances"
    response = google_auth_requests.AuthorizedSession(creds).post(uri, json=data)

    # print(response.json())
    print(json.dumps(response.json(), indent=2))
    # Example response:
    #   {
    #       "bleuResults": {
    #           "bleuMetricValues": [
    #           {
    #               "score": 0.113395825
    #           }
    #           ]
    #       }
    #   }

    # [END generativeaionvertexai_evaluation_example_syntax]
    return response


if __name__ == "__main__":
    send_evaluation_request_gapic()
