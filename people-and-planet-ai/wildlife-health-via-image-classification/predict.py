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

import base64
import requests

from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict


def instance_from_lila(image_file):
    base_url = "https://lilablobssc.blob.core.windows.net/wcs-unzipped"
    image_bytes = requests.get(f"{base_url}/{image_file}").content
    return predict.instance.ImageClassificationPredictionInstance(
        content=base64.b64encode(image_bytes).decode("utf-8"),
    ).to_value()


def run(project, region, model_endpoint_id, image_file):
    client = aiplatform.gapic.PredictionServiceClient(
        client_options={
            "api_endpoint": "us-central1-prediction-aiplatform.googleapis.com"
        }
    )

    # See gs://google-cloud-aiplatform/schema/predict/params/image_classification_1.0.0.yaml for the format of the parameters.
    response = client.predict(
        endpoint=client.endpoint_path(
            project=project, location=region, endpoint=model_endpoint_id
        ),
        instances=[instance_from_lila(image_file)],
        parameters=predict.params.ImageClassificationPredictionParams(
            confidence_threshold=0.1,
            max_predictions=5,
        ).to_value(),
    )

    # See gs://google-cloud-aiplatform/schema/predict/prediction/classification.yaml for the format of the predictions.
    for prediction in response.predictions:
        pred = dict(prediction)
        return sorted(
            [
                (category, confidence)
                for category, confidence in zip(
                    pred["displayNames"], pred["confidences"]
                )
            ],
            reverse=True,
            key=lambda x: x[1],
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--model-endpoint-id", required=True)
    parser.add_argument("--image-file", required=True)
    args = parser.parse_args()

    predictions = run(
        args.project, args.region, args.model_endpoint_id, args.image_file
    )
    for category, confidence in predictions:
        print(f"{category}: {confidence * 100.0 : .2f}% confidence")
