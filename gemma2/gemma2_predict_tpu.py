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
import sys

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def gemma2_predict_tpu(ENDPOINT_REGION: str, ENDPOINT_ID: str) -> str:
    # [START generativeaionvertexai_gemma2_predict_tpu]
    """
    Sample to run inference on a Gemma2 model deployed to a Vertex AI endpoint with TPU accellerators.
    """

    from google.cloud import aiplatform
    from google.protobuf import json_format
    from google.protobuf.struct_pb2 import Value

    # TODO(developer): Update & uncomment lines below
    # PROJECT_ID = "your-project-id"
    # ENDPOINT_REGION = "your-vertex-endpoint-region"
    # ENDPOINT_ID = "your-vertex-endpoint-id"

    # Default configuration
    config = {"max_tokens": 1024, "temperature": 0.9, "top_p": 1.0, "top_k": 1}

    # Prompt used in the prediction
    prompt = "Why is the sky blue?"

    # Encapsulate the prompt in a correct format for TPUs
    # Example format: [{'prompt': 'Why is the sky blue?', 'temperature': 0.9}]
    input = {"prompt": prompt}
    input.update(config)

    # Convert input message to a list of GAPIC instances for model input
    instances = [json_format.ParseDict(input, Value())]

    # Create a client
    api_endpoint = f"{ENDPOINT_REGION}-aiplatform.googleapis.com"
    client = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": api_endpoint}
    )

    # Call the Gemma2 endpoint
    gemma2_end_point = (
        f"projects/{PROJECT_ID}/locations/{ENDPOINT_REGION}/endpoints/{ENDPOINT_ID}"
    )
    response = client.predict(
        endpoint=gemma2_end_point,
        instances=instances,
    )
    text_responses = response.predictions
    print(text_responses[0])

    # [END generativeaionvertexai_gemma2_predict_tpu]
    return text_responses[0]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python gemma2_predict_tpu.py <GEMMA2_ENDPOINT_REGION> <GEMMA2_ENDPOINT_ID>"
        )
        sys.exit(1)

    ENDPOINT_REGION = sys.argv[1]
    ENDPOINT_ID = sys.argv[2]
    gemma2_predict_tpu(ENDPOINT_REGION, ENDPOINT_ID)
