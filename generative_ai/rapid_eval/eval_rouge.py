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

def generate_content(PROJECT_ID: str, REGION: str):
    # [START generativeaionvertexai_eval_rouge]
    import json

    from google import auth
    from google.api_core import exceptions
    from google.auth.transport import requests as google_auth_requests

    creds, _ = auth.default(
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    data = {
    "rouge_input": {
        "metric_spec": {
            "rouge_type": "rougeLsum",
            "use_stemmer": True,
            "split_summaries": True
        },
        "instances": [
            {
            "prediction": "A fast brown fox leaps over a lazy dog.",
            "reference": "The quick brown fox jumps over the lazy dog.",
            }, {
            "prediction": "A quick brown fox jumps over the lazy canine.",
            "reference": "The quick brown fox jumps over the lazy dog.",
            }, {
            "prediction": "The speedy brown fox jumps over the lazy dog.",
            "reference": "The quick brown fox jumps over the lazy dog.",
            }
        ]
    }
    }

    uri = f'https://${REGION}-aiplatform.googleapis.com/v1beta1/projects/${PROJECT_ID}/locations/${REGION}:evaluateInstances'
    result = google_auth_requests.AuthorizedSession(creds).post(uri, json=data)

    print(json.dumps(result.json(), indent=2))
    # [END generativeaionvertexai_eval_rouge]

    return result