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

"""DialogFlow API Entity Python sample showing how to manage entities.

Examples:
  python entity_management.py -h
  python entity_management.py --project-id PROJECT_ID \
  list --entity-type-id e57238e2-e692-44ea-9216-6be1b2332e2a
  python entity_management.py --project-id PROJECT_ID \
  create new_room --synonyms basement cellar \
  --entity-type-id e57238e2-e692-44ea-9216-6be1b2332e2a
  python entity_management.py --project-id PROJECT_ID \
  delete new_room \
  --entity-type-id e57238e2-e692-44ea-9216-6be1b2332e2a
"""

import argparse


def list_entities(project_id, entity_type_id):
    import dialogflow_v2 as dialogflow
    entity_types_client = dialogflow.EntityTypesClient()

    parent = entity_types_client.entity_type_path(
        project_id, entity_type_id)

    entities = entity_types_client.get_entity_type(parent).entities

    for entity in entities:
        print('Entity value: {}'.format(entity.value))
        print('Entity synonyms: {}\n'.format(entity.synonyms))


# [START dialogflow_create_entity]
def create_entity(project_id, entity_type_id, entity_value, synonyms):
    """Create an entity of the given entity type."""
    import dialogflow_v2 as dialogflow
    entity_types_client = dialogflow.EntityTypesClient()

    # Note: synonyms must be exactly [entity_value] if the
    # entity_type's kind is KIND_LIST
    synonyms = synonyms or [entity_value]

    entity_type_path = entity_types_client.entity_type_path(
        project_id, entity_type_id)

    entity = dialogflow.types.EntityType.Entity()
    entity.value = entity_value
    entity.synonyms.extend(synonyms)

    response = entity_types_client.batch_create_entities(
        entity_type_path, [entity])

    print('Entity created: {}'.format(response))
# [END dialogflow_create_entity]


# [START dialogflow_delete_entity]
def delete_entity(project_id, entity_type_id, entity_value):
    """Delete entity with the given entity type and entity value."""
    import dialogflow_v2 as dialogflow
    entity_types_client = dialogflow.EntityTypesClient()

    entity_type_path = entity_types_client.entity_type_path(
        project_id, entity_type_id)

    entity_types_client.batch_delete_entities(
        entity_type_path, [entity_value])
# [END dialogflow_delete_entity]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--project-id',
        help='Project/agent id.  Required.',
        required=True)

    subparsers = parser.add_subparsers(dest='command')

    list_parser = subparsers.add_parser(
        'list', help=list_entities.__doc__)
    list_parser.add_argument(
        '--entity-type-id',
        help='The id of the entity_type.')

    create_parser = subparsers.add_parser(
        'create', help=create_entity.__doc__)
    create_parser.add_argument(
        'entity_value',
        help='The entity value to be added.')
    create_parser.add_argument(
        '--entity-type-id',
        help='The id of the entity_type to which to add an entity.',
        required=True)
    create_parser.add_argument(
        '--synonyms',
        nargs='*',
        help='The synonyms that will map to the provided entity value.',
        default=[])

    delete_parser = subparsers.add_parser(
        'delete', help=delete_entity.__doc__)
    delete_parser.add_argument(
        '--entity-type-id',
        help='The id of the entity_type.',
        required=True)
    delete_parser.add_argument(
        'entity_value',
        help='The value of the entity to delete.')

    args = parser.parse_args()

    if args.command == 'list':
        list_entities(args.project_id, args.entity_type_id)
    elif args.command == 'create':
        create_entity(
            args.project_id, args.entity_type_id, args.entity_value,
            args.synonyms)
    elif args.command == 'delete':
        delete_entity(
            args.project_id, args.entity_type_id, args.entity_value)
