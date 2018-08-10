#!/usr/bin/env python

# Copyright 2017 Google LLC
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

"""DialogFlow API EntityType Python sample showing how to manage entity types.

Examples:
  python entity_type_management.py -h
  python entity_type_management.py --project-id PROJECT_ID list
  python entity_type_management.py --project-id PROJECT_ID create employee
  python entity_type_management.py --project-id PROJECT_ID delete \
  e57238e2-e692-44ea-9216-6be1b2332e2a
"""

import argparse


def list_entity_types(project_id):
    import dialogflow_v2 as dialogflow
    entity_types_client = dialogflow.EntityTypesClient()

    parent = entity_types_client.project_agent_path(project_id)

    entity_types = entity_types_client.list_entity_types(parent)

    for entity_type in entity_types:
        print('Entity type name: {}'.format(entity_type.name))
        print('Entity type display name: {}'.format(entity_type.display_name))
        print('Number of entities: {}\n'.format(len(entity_type.entities)))


# [START dialogflow_create_entity_type]
def create_entity_type(project_id, display_name, kind):
    """Create an entity type with the given display name."""
    import dialogflow_v2 as dialogflow
    entity_types_client = dialogflow.EntityTypesClient()

    parent = entity_types_client.project_agent_path(project_id)
    entity_type = dialogflow.types.EntityType(
        display_name=display_name, kind=kind)

    response = entity_types_client.create_entity_type(parent, entity_type)

    print('Entity type created: \n{}'.format(response))
# [END dialogflow_create_entity_type]


# [START dialogflow_delete_entity_type]
def delete_entity_type(project_id, entity_type_id):
    """Delete entity type with the given entity type name."""
    import dialogflow_v2 as dialogflow
    entity_types_client = dialogflow.EntityTypesClient()

    entity_type_path = entity_types_client.entity_type_path(
        project_id, entity_type_id)

    entity_types_client.delete_entity_type(entity_type_path)
# [END dialogflow_delete_entity_type]


# Helper to get entity_type_id from display name.
def _get_entity_type_ids(project_id, display_name):
    import dialogflow_v2 as dialogflow
    entity_types_client = dialogflow.EntityTypesClient()

    parent = entity_types_client.project_agent_path(project_id)
    entity_types = entity_types_client.list_entity_types(parent)
    entity_type_names = [
        entity_type.name for entity_type in entity_types
        if entity_type.display_name == display_name]

    entity_type_ids = [
        entity_type_name.split('/')[-1] for entity_type_name
        in entity_type_names]

    return entity_type_ids


if __name__ == '__main__':
    import dialogflow_v2
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--project-id',
        help='Project/agent id.  Required.',
        required=True)

    subparsers = parser.add_subparsers(dest='command')

    list_parser = subparsers.add_parser(
        'list', help=list_entity_types.__doc__)

    create_parser = subparsers.add_parser(
        'create', help=create_entity_type.__doc__)
    create_parser.add_argument(
        'display_name',
        help='The display name of the entity.')
    create_parser.add_argument(
        '--kind',
        help='The kind of entity.  KIND_MAP (default) or KIND_LIST.',
        default=dialogflow_v2.enums.EntityType.Kind.KIND_MAP)

    delete_parser = subparsers.add_parser(
        'delete', help=delete_entity_type.__doc__)
    delete_parser.add_argument(
        'entity_type_id',
        help='The id of the entity_type.')

    args = parser.parse_args()

    if args.command == 'list':
        list_entity_types(args.project_id)
    elif args.command == 'create':
        create_entity_type(args.project_id, args.display_name, args.kind)
    elif args.command == 'delete':
        delete_entity_type(args.project_id, args.entity_type_id)
