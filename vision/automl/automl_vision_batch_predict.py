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

# DO NOT EDIT! This is a generated sample ("LongRunningPromise",  "automl_vision_batch_predict")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-automl

# sample-metadata
#   title: AutoML Batch Predict (AutoML Vision)
#   description: AutoML Batch Predict using AutoML Vision
#   usage: python3 samples/v1beta1/automl_vision_batch_predict.py [--input_uri "gs://[BUCKET-NAME]/path/to/file-with-image-urls.csv"] [--output_uri "gs://[BUCKET-NAME]/directory-for-output-files/"] [--project "[Google Cloud Project ID]"] [--model_id "[Model ID]"]

# [START automl_vision_batch_predict]
from google.cloud import automl_v1beta1


def sample_batch_predict(input_uri, output_uri, project, model_id):
    """
    AutoML Batch Predict using AutoML Vision

    Args:
      input_uri Google Cloud Storage URI to CSV file in your bucket that contains the
      paths to the images to annotate, e.g. gs://[BUCKET-NAME]/path/to/images.csv
      Each line specifies a separate path to an image in Google Cloud Storage.
      output_uri Identifies where to store the output of your prediction request
      in your Google Cloud Storage bucket.
      You must have write permissions to the Google Cloud Storage bucket.
      project Required. Your Google Cloud Project ID.
      model_id Model ID, e.g. VOT1234567890123456789
    """

    client = automl_v1beta1.PredictionServiceClient()

    # input_uri = 'gs://[BUCKET-NAME]/path/to/file-with-image-urls.csv'
    # output_uri = 'gs://[BUCKET-NAME]/directory-for-output-files/'
    # project = '[Google Cloud Project ID]'
    # model_id = '[Model ID]'
    name = client.model_path(project, "us-central1", model_id)
    input_uris = [input_uri]
    gcs_source = {"input_uris": input_uris}
    input_config = {"gcs_source": gcs_source}
    gcs_destination = {"output_uri_prefix": output_uri}
    output_config = {"gcs_destination": gcs_destination}

    # A value from 0.0 to 1.0. When the model detects objects on video frames,
    # it will only produce bounding boxes that have at least this confidence score.
    # The default is 0.5.
    params_item = "0.0"
    params = {"score_threshold": params_item}

    operation = client.batch_predict(name, input_config, output_config, params=params)

    print(u"Waiting for operation to complete...")
    response = operation.result()

    print(u"Batch Prediction results saved to specified Cloud Storage bucket.")


# [END automl_vision_batch_predict]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_uri",
        type=str,
        default="gs://[BUCKET-NAME]/path/to/file-with-image-urls.csv",
    )
    parser.add_argument(
        "--output_uri",
        type=str,
        default="gs://[BUCKET-NAME]/directory-for-output-files/",
    )
    parser.add_argument("--project", type=str, default="[Google Cloud Project ID]")
    parser.add_argument("--model_id", type=str, default="[Model ID]")
    args = parser.parse_args()

    sample_batch_predict(args.input_uri, args.output_uri, args.project, args.model_id)


if __name__ == "__main__":
    main()
