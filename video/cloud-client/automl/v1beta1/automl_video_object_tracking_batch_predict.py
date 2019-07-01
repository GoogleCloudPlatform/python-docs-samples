# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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

# DO NOT EDIT! This is a generated sample ("LongRunningPromise",  "automl_video_object_tracking_batch_predict")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-automl

# sample-metadata
#   title: AutoML Batch Predict
#   description: AutoML Batch Predict
#   usage: python3 samples/v1beta1/automl_video_object_tracking_batch_predict.py [--gcs_output_prefix "[gs://your-output-bucket/your-object-id]"] [--model_id "[Model ID]"] [--project "[Google Cloud Project ID]"]
import sys

# [START automl_video_object_tracking_batch_predict]

from google.cloud import automl_v1beta1


def sample_batch_predict(gcs_output_prefix, model_id, project):
    """
    AutoML Batch Predict

    Args:
      gcs_output_prefix Identifies where to store the output of your prediction
      request
      in your Google Cloud Storage bucket.
      You must have write permissions to the Google Cloud Storage bucket.
      model_id Model ID, e.g. VOT1234567890123456789
      project Required. Your Google Cloud Project ID.
    """

    client = automl_v1beta1.PredictionServiceClient()

    # gcs_output_prefix = '[gs://your-output-bucket/your-object-id]'
    # model_id = '[Model ID]'
    # project = '[Google Cloud Project ID]'
    name = client.model_path(project, "us-central1", model_id)
    input_uris_element = (
        "gs://automl-video-datasets/youtube_8m_videos_animal_batchpredict.csv"
    )
    input_uris = [input_uris_element]
    gcs_source = {"input_uris": input_uris}
    input_config = {"gcs_source": gcs_source}
    gcs_destination = {"output_uri_prefix": gcs_output_prefix}
    output_config = {"gcs_destination": gcs_destination}

    # A value from 0.0 to 1.0. When the model detects objects on video frames,
    # it will only produce bounding boxes that have at least this confidence score.
    # The default is 0.5.
    params_item = "0.0"
    params = {"score_threshold": params_item}

    operation = client.batch_predict(name, input_config, output_config, params=params)

    print(u"Waiting for operation to complete...")
    response = operation.result()

    print(u"Batch Prediction results saved to Cloud Storage")


# [END automl_video_object_tracking_batch_predict]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gcs_output_prefix",
        type=str,
        default="[gs://your-output-bucket/your-object-id]",
    )
    parser.add_argument("--model_id", type=str, default="[Model ID]")
    parser.add_argument("--project", type=str, default="[Google Cloud Project ID]")
    args = parser.parse_args()

    sample_batch_predict(args.gcs_output_prefix, args.model_id, args.project)


if __name__ == "__main__":
    main()
