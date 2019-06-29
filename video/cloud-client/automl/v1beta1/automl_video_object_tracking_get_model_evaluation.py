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

# DO NOT EDIT! This is a generated sample ("Request",  "automl_video_object_tracking_get_model_evaluation")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-automl

# sample-metadata
#   title: Get Model Evaluation
#   description: Get Model Evaluation
#   usage: python3 samples/v1beta1/automl_video_object_tracking_get_model_evaluation.py [--evaluation_id "[Model Evaluation ID]"] [--model_id "[Model ID]"] [--project "[Google Cloud Project ID]"]
import sys

# [START automl_video_object_tracking_get_model_evaluation]

from google.cloud import automl_v1beta1


def sample_get_model_evaluation(evaluation_id, model_id, project):
    """
    Get Model Evaluation

    Args:
      model_id Model ID, e.g. VOT1234567890123456789
      project Required. Your Google Cloud Project ID.
    """

    client = automl_v1beta1.AutoMlClient()

    # evaluation_id = '[Model Evaluation ID]'
    # model_id = '[Model ID]'
    # project = '[Google Cloud Project ID]'
    name = client.model_evaluation_path(project, "us-central1", model_id, evaluation_id)

    response = client.get_model_evaluation(name)
    evaluation = response
    print(u"Model evaluation: {}".format(evaluation.name))
    print(u"Display name: {}".format(evaluation.display_name))
    print(u"Evaluated example count: {}".format(evaluation.evaluated_example_count))
    video_metrics = evaluation.video_object_tracking_evaluation_metrics
    # The number of video frames used to create this evaluation.
    print(u"Evaluated Frame Count: {}".format(video_metrics.evaluated_frame_count))
    # The total number of bounding boxes (i.e. summed over all frames)
    # the ground truth used to create this evaluation had.
    #
    print(
        u"Evaluated Bounding Box Count: {}".format(
            video_metrics.evaluated_bounding_box_count
        )
    )
    # The single metric for bounding boxes evaluation: the mean_average_precision
    # averaged over all bounding_box_metrics_entries.
    #
    print(
        u"Bounding Box Mean Average Precision: {}".format(
            video_metrics.bounding_box_mean_average_precision
        )
    )
    # The bounding boxes match metrics for each Intersection-over-union threshold
    # 0.05,0.10,...,0.95,0.96,0.97,0.98,0.99 and each label confidence threshold
    # 0.05,0.10,...,0.95,0.96,0.97,0.98,0.99 pair.
    #
    for bounding_box_metrics_entry in video_metrics.bounding_box_metrics_entries:
        # The intersection-over-union threshold value used to compute this metrics entry.
        #
        print(u"IoU Threshold: {}".format(bounding_box_metrics_entry.iou_threshold))
        # The mean average precision, most often close to au_prc.
        #
        print(
            u"Mean Average Precision: {}".format(
                bounding_box_metrics_entry.mean_average_precision
            )
        )
        # Metrics for each label-match confidence_threshold from
        # 0.05,0.10,...,0.95,0.96,0.97,0.98,0.99. =
        # Precision-recall curve is derived from them.
        #
        for (
            confidence_metrics_entry
        ) in bounding_box_metrics_entry.confidence_metrics_entries:
            # The confidence threshold value used to compute the metrics.
            print(
                u"Confidence Threshold: {}".format(
                    confidence_metrics_entry.confidence_threshold
                )
            )
            # Recall under the given confidence threshold.
            print(u"Recall {}".format(confidence_metrics_entry.recall))
            # Precision under the given confidence threshold.
            print(u"Precision: {}".format(confidence_metrics_entry.precision))
            # The harmonic mean of recall and precision.
            print(u"F1 Score: {}".format(confidence_metrics_entry.f1_score))


# [END automl_video_object_tracking_get_model_evaluation]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--evaluation_id", type=str, default="[Model Evaluation ID]")
    parser.add_argument("--model_id", type=str, default="[Model ID]")
    parser.add_argument("--project", type=str, default="[Google Cloud Project ID]")
    args = parser.parse_args()

    sample_get_model_evaluation(args.evaluation_id, args.model_id, args.project)


if __name__ == "__main__":
    main()
