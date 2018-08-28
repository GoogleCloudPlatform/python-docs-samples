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

"""DialogFlow API SessionEntityType Python sample showing how to manage
session entity types.

Examples:
  python session_entity_type_management.py -h
  python session_entity_type_management.py --project-id PROJECT_ID list \
  --session-id SESSION_ID
  python session_entity_type_management.py --project-id PROJECT_ID create \
  --session-id SESSION_ID \
  --entity-type-display-name room --entity-values C D E F
  python session_entity_type_management.py --project-id PROJECT_ID delete \
  --session-id SESSION_ID \
  --entity-type-display-name room
"""

import argparse


# [START dialogflow_list_session_entity_types]
def list_session_entity_types(project_id, session_id):
    import dialogflow_v2 as dialogflow
    session_entity_types_client = dialogflow.SessionEntityTypesClient()

    session_path = session_entity_types_client.session_path(
        project_id, session_id)

    session_entity_types = (
        session_entity_types_client.
        list_session_entity_types(session_path))

    print('SessionEntityTypes for session {}:\n'.format(session_path))
    for session_entity_type in session_entity_types:
        print('\tSessionEntityType name: {}'.format(session_entity_type.name))
        print('\tNumber of entities: {}\n'.format(
            len(session_entity_type.entities)))
# [END dialogflow_list_session_entity_types]


# [START dialogflow_create_session_entity_type]
def create_session_entity_type(project_id, session_id, entity_values,
                               entity_type_display_name, entity_override_mode):
    """Create a session entity type with the given display name."""
    import dialogflow_v2 as dialogflow
    session_entity_types_client = dialogflow.SessionEntityTypesClient()

    session_path = session_entity_types_client.session_path(
        project_id, session_id)
    session_entity_type_name = (
        session_entity_types_client.session_entity_type_path(
            project_id, session_id, entity_type_display_name))

    # Here we use the entity value as the only synonym.
    entities = [
        dialogflow.types.EntityType.Entity(value=value, synonyms=[value])
        for value in entity_values]
    session_entity_type = dialogflow.types.SessionEntityType(
        name=session_entity_type_name,
        entity_override_mode=entity_override_mode,
        entities=entities)

    response = session_entity_types_client.create_session_entity_type(
        session_path, session_entity_type)

    print('SessionEntityType created: \n\n{}'.format(response))
# [END dialogflow_create_session_entity_type]


# [START dialogflow_delete_session_entity_type]
def delete_session_entity_type(project_id, session_id,
                               entity_type_display_name):
    """Delete session entity type with the given entity type display name."""
    import dialogflow_v2 as dialogflow
    session_entity_types_client = dialogflow.SessionEntityTypesClient()

    session_entity_type_name = (
        session_entity_types_client.session_entity_type_path(
            project_id, session_id, entity_type_display_name))

    session_entity_types_client.delete_session_entity_type(
        session_entity_type_name)
# [END dialogflow_delete_session_entity_type]


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
        'list', help=list_session_entity_types.__doc__)
    list_parser.add_argument(
        '--session-id',
        required=True)

    create_parser = subparsers.add_parser(
        'create', help=create_session_entity_type.__doc__)
    create_parser.add_argument(
        '--session-id',
        required=True)
    create_parser.add_argument(
        '--entity-type-display-name',
        help='The DISPLAY NAME of the entity type to be overridden '
        'in the session.',
        required=True)
    create_parser.add_argument(
        '--entity-values',
        nargs='*',
        help='The entity values of the session entity type.',
        required=True)
    create_parser.add_argument(
        '--entity-override-mode',
        help='ENTITY_OVERRIDE_MODE_OVERRIDE (default) or '
        'ENTITY_OVERRIDE_MODE_SUPPLEMENT',
        default=(dialogflow_v2.enums.SessionEntityType.EntityOverrideMode.
                 ENTITY_OVERRIDE_MODE_OVERRIDE))

    delete_parser = subparsers.add_parser(
        'delete', help=delete_session_entity_type.__doc__)
    delete_parser.add_argument(
        '--session-id',
        required=True)
    delete_parser.add_argument(
        '--entity-type-display-name',
        help='The DISPLAY NAME of the entity type.',
        required=True)

    args = parser.parse_args()

    if args.command == 'list':
        list_session_entity_types(args.project_id, args.session_id)
    elif args.command == 'create':
        create_session_entity_type(
            args.project_id, args.session_id, args.entity_values,
            args.entity_type_display_name, args.entity_override_mode)
    elif args.command == 'delete':
        delete_session_entity_type(
            args.project_id, args.session_id, args.entity_type_display_name)
