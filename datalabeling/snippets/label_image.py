#!/usr/bin/env python

# Copyright 2022 Google LLC
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

import argparse
import os

from google.api_core.client_options import ClientOptions


# [START datalabeling_label_image_beta]
def label_image(
    dataset_resource_name, instruction_resource_name, annotation_spec_set_resource_name
):
    """Labels an image dataset."""
    from google.cloud import datalabeling_v1beta1 as datalabeling

    client = datalabeling.DataLabelingServiceClient()
    # [END datalabeling_label_image_beta]
    # If provided, use a provided test endpoint - this will prevent tests on
    # this snippet from triggering any action by a real human
    if "DATALABELING_ENDPOINT" in os.environ:
        opts = ClientOptions(api_endpoint=os.getenv("DATALABELING_ENDPOINT"))
        client = datalabeling.DataLabelingServiceClient(client_options=opts)
    # [START datalabeling_label_image_beta]

    basic_config = datalabeling.HumanAnnotationConfig(
        instruction=instruction_resource_name,
        annotated_dataset_display_name="YOUR_ANNOTATED_DATASET_DISPLAY_NAME",
        label_group="YOUR_LABEL_GROUP",
        replica_count=1,
    )

    feature = datalabeling.LabelImageRequest.Feature.CLASSIFICATION

    # annotation_spec_set_resource_name needs to be created beforehand.
    # See the examples in the following:
    # https://cloud.google.com/ai-platform/data-labeling/docs/label-sets
    config = datalabeling.ImageClassificationConfig(
        annotation_spec_set=annotation_spec_set_resource_name,
        allow_multi_label=False,
        answer_aggregation_type=datalabeling.StringAggregationType.MAJORITY_VOTE,
    )

    response = client.label_image(
        request={
            "parent": dataset_resource_name,
            "basic_config": basic_config,
            "feature": feature,
            "image_classification_config": config,
        }
    )

    print("Label_image operation name: {}".format(response.operation.name))
    return response


# [END datalabeling_label_image_beta]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--dataset-resource-name",
        help="Dataset resource name. Required.",
        required=True,
    )

    parser.add_argument(
        "--instruction-resource-name",
        help="Instruction resource name. Required.",
        required=True,
    )

    parser.add_argument(
        "--annotation-spec-set-resource-name",
        help="Annotation spec set resource name. Required.",
        required=True,
    )

    args = parser.parse_args()

    label_image(
        args.dataset_resource_name,
        args.instruction_resource_name,
        args.annotation_spec_set_resource_name,
    )
