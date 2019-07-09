#!/usr/bin/env python

# Copyright 2019 Google LLC
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


# [START datalabeling_create_instruction_beta]
def create_instruction(project_id, data_type, instruction_gcs_uri):
    """ Creates a data labeling PDF instruction for the given Google Cloud
    project. The PDF file should be uploaded to the project in
    Google Cloud Storage.
    """
    from google.cloud import datalabeling_v1beta1 as datalabeling
    client = datalabeling.DataLabelingServiceClient()

    project_path = client.project_path(project_id)

    pdf_instruction = datalabeling.types.PdfInstruction(
        gcs_file_uri=instruction_gcs_uri)

    instruction = datalabeling.types.Instruction(
        display_name='YOUR_INSTRUCTION_DISPLAY_NAME',
        description='YOUR_DESCRIPTION',
        data_type=data_type,
        pdf_instruction=pdf_instruction
    )

    operation = client.create_instruction(project_path, instruction)

    result = operation.result()

    # The format of the resource name:
    # project_id/{project_id}/instruction/{instruction_id}
    print('The instruction resource name: {}\n'.format(result.name))
    print('Display name: {}'.format(result.display_name))
    print('Description: {}'.format(result.description))
    print('Create time:')
    print('\tseconds: {}'.format(result.create_time.seconds))
    print('\tnanos: {}'.format(result.create_time.nanos))
    print('Data type: {}'.format(
        datalabeling.enums.DataType(result.data_type).name))
    print('Pdf instruction:')
    print('\tGcs file uri: {}'.format(
        result.pdf_instruction.gcs_file_uri))

    return result
# [END datalabeling_create_instruction_beta]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--project-id',
        help='Project ID. Required.',
        required=True
    )

    parser.add_argument(
        '--data-type',
        help='Data type. Only support IMAGE, VIDEO, TEXT and AUDIO. Required.',
        required=True
    )

    parser.add_argument(
        '--instruction-gcs-uri',
        help='The URI of Google Cloud Storage of the instruction. Required.',
        required=True
    )

    args = parser.parse_args()

    create_instruction(
        args.project_id,
        args.data_type,
        args.instruction_gcs_uri
    )
