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


# [START datalabeling_create_annotation_spec_set_beta]
def create_annotation_spec_set(project_id):
    """Creates a data labeling annotation spec set for the given
    Google Cloud project.
    """
    from google.cloud import datalabeling_v1beta1 as datalabeling

    client = datalabeling.DataLabelingServiceClient()
    # [END datalabeling_create_annotation_spec_set_beta]
    # If provided, use a provided test endpoint - this will prevent tests on
    # this snippet from triggering any action by a real human
    if "DATALABELING_ENDPOINT" in os.environ:
        opts = ClientOptions(api_endpoint=os.getenv("DATALABELING_ENDPOINT"))
        client = datalabeling.DataLabelingServiceClient(client_options=opts)
    # [START datalabeling_create_annotation_spec_set_beta]

    project_path = f"projects/{project_id}"

    annotation_spec_1 = datalabeling.AnnotationSpec(
        display_name="label_1", description="label_description_1"
    )

    annotation_spec_2 = datalabeling.AnnotationSpec(
        display_name="label_2", description="label_description_2"
    )

    annotation_spec_set = datalabeling.AnnotationSpecSet(
        display_name="YOUR_ANNOTATION_SPEC_SET_DISPLAY_NAME",
        description="YOUR_DESCRIPTION",
        annotation_specs=[annotation_spec_1, annotation_spec_2],
    )

    response = client.create_annotation_spec_set(
        request={"parent": project_path, "annotation_spec_set": annotation_spec_set}
    )

    # The format of the resource name:
    # project_id/{project_id}/annotationSpecSets/{annotationSpecSets_id}
    print(f"The annotation_spec_set resource name: {response.name}")
    print(f"Display name: {response.display_name}")
    print(f"Description: {response.description}")
    print("Annotation specs:")
    for annotation_spec in response.annotation_specs:
        print(f"\tDisplay name: {annotation_spec.display_name}")
        print(f"\tDescription: {annotation_spec.description}\n")

    return response


# [END datalabeling_create_annotation_spec_set_beta]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--project-id", help="Project ID. Required.", required=True)

    args = parser.parse_args()

    create_annotation_spec_set(args.project_id)
