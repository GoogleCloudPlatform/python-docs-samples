#!/usr/bin/env python

# Copyright 2018 Google LLC
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

"""Dialogflow API Python sample showing how to manage Knowledge bases.

Examples:
  python knowledge_base_management.py -h
  python knowledge_base_management.py --project-id PROJECT_ID \
  create --display-name DISPLAY_NAME
"""

import argparse


# [START dialogflow_create_knowledge_base]
def create_knowledge_base(project_id, display_name):
    """Creates a Knowledge base.

    Args:
        project_id: The GCP project linked with the agent.
        display_name: The display name of the Knowledge base."""
    from google.cloud import dialogflow_v2beta1 as dialogflow
    client = dialogflow.KnowledgeBasesClient()
    project_path = client.common_project_path(project_id)

    knowledge_base = dialogflow.KnowledgeBase(
        display_name=display_name)

    response = client.create_knowledge_base(
        parent=project_path,
        knowledge_base=knowledge_base
    )

    print('Knowledge Base created:\n')
    print('Display Name: {}\n'.format(response.display_name))
    print('Knowledge ID: {}\n'.format(response.name))
# [END dialogflow_create_knowledge_base]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--project-id', help='Project/agent id.', required=True)

    subparsers = parser.add_subparsers(dest='command')

    create_parser = subparsers.add_parser(
        'create', help='Create a new Knowledge base.')
    create_parser.add_argument(
        '--display-name',
        help='A name of the Knowledge base, used for display purpose, '
             'can not be used to identify the Knowledge base.',
        default=str(''))

    args = parser.parse_args()

    if args.command == 'create':
        create_knowledge_base(args.project_id, args.display_name)
