#!/usr/bin/env python

# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import base64

from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
import requests

from train_model import with_retries


def run(
    project: str, region: str, model_endpoint_id: str, image_file: str
) -> list[tuple[str, float]]:
    """Sends an image from the LILA WCS database for prediction.

    Args:
        project: Google Cloud Project ID.
        region: Location for AI Platform resources.
        model_endpoint_id: Deployed model endpoint ID.
        image_file: The image file path from LILA.

    Returns:
        The predictions as a list of (category, confidence) tuples, sorted by confidence.
    """
    client = aiplatform.gapic.PredictionServiceClient(
        client_options={
            "api_endpoint": "us-central1-prediction-aiplatform.googleapis.com"
        }
    )

    base_url = "https://lilablobssc.blob.core.windows.net/wcs-unzipped"
    image_bytes = with_retries(lambda: requests.get(f"{base_url}/{image_file}").content)

    response = client.predict(
        endpoint=client.endpoint_path(
            project=project, location=region, endpoint=model_endpoint_id
        ),
        instances=[
            predict.instance.ImageClassificationPredictionInstance(
                content=base64.b64encode(image_bytes).decode("utf-8"),
            ).to_value()
        ],
        parameters=predict.params.ImageClassificationPredictionParams(
            confidence_threshold=0.1,
            max_predictions=5,
        ).to_value(),
    )

    prediction = [dict(pred) for pred in response.predictions][0]
    return sorted(
        [
            (category, confidence)
            for category, confidence in zip(
                prediction["displayNames"], prediction["confidences"]
            )
        ],
        reverse=True,
        key=lambda x: x[1],
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project",
        required=True,
        help="Google Cloud Project Id",
    )
    parser.add_argument(
        "--region",
        required=True,
        help="Location for AI Platform resources",
    )
    parser.add_argument(
        "--model-endpoint-id",
        required=True,
        help="Deployed model endpoint ID",
    )
    parser.add_argument(
        "--image-file",
        required=True,
        help="The image file path from LILA",
    )
    args = parser.parse_args()

    predictions = run(
        args.project, args.region, args.model_endpoint_id, args.image_file
    )
    for category, confidence in predictions:
        print(f"{category}: {confidence * 100.0 : .2f}% confidence")
