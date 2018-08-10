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

"""DialogFlow API Context Python sample showing how to manage session
contexts.

Examples:
  python context_management.py -h
  python context_management.py --project-id PROJECT_ID \
  list --session-id SESSION_ID
  python context_management.py --project-id PROJECT_ID \
  create --session-id SESSION_ID --context-id CONTEXT_ID
  python context_management.py --project-id PROJECT_ID \
  delete --session-id SESSION_ID --context-id CONTEXT_ID
"""

import argparse


def list_contexts(project_id, session_id):
    import dialogflow_v2 as dialogflow
    contexts_client = dialogflow.ContextsClient()

    session_path = contexts_client.session_path(project_id, session_id)

    contexts = contexts_client.list_contexts(session_path)

    print('Contexts for session {}:\n'.format(session_path))
    for context in contexts:
        print('Context name: {}'.format(context.name))
        print('Lifespan count: {}'.format(context.lifespan_count))
        print('Fields:')
        for field, value in context.parameters.fields.items():
            if value.string_value:
                print('\t{}: {}'.format(field, value))


# [START dialogflow_create_context]
def create_context(project_id, session_id, context_id, lifespan_count):
    import dialogflow_v2 as dialogflow
    contexts_client = dialogflow.ContextsClient()

    session_path = contexts_client.session_path(project_id, session_id)
    context_name = contexts_client.context_path(
        project_id, session_id, context_id)

    context = dialogflow.types.Context(
        name=context_name, lifespan_count=lifespan_count)

    response = contexts_client.create_context(session_path, context)

    print('Context created: \n{}'.format(response))
# [END dialogflow_create_context]


# [START dialogflow_delete_context]
def delete_context(project_id, session_id, context_id):
    import dialogflow_v2 as dialogflow
    contexts_client = dialogflow.ContextsClient()

    context_name = contexts_client.context_path(
        project_id, session_id, context_id)

    contexts_client.delete_context(context_name)
# [END dialogflow_delete_context]


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
        'list', help=list_contexts.__doc__)
    list_parser.add_argument(
        '--session-id',
        required=True)

    create_parser = subparsers.add_parser(
        'create', help=create_context.__doc__)
    create_parser.add_argument(
        '--session-id',
        required=True)
    create_parser.add_argument(
        '--context-id',
        help='The id of the context.',
        required=True)
    create_parser.add_argument(
        '--lifespan-count',
        help='The lifespan_count of the context.  Defaults to 1.',
        default=1)

    delete_parser = subparsers.add_parser(
        'delete', help=delete_context.__doc__)
    delete_parser.add_argument(
        '--session-id',
        required=True)
    delete_parser.add_argument(
        '--context-id',
        help='The id of the context.',
        required=True)

    args = parser.parse_args()

    if args.command == 'list':
        list_contexts(args.project_id, args.session_id, )
    elif args.command == 'create':
        create_context(
            args.project_id, args.session_id, args.context_id,
            args.lifespan_count)
    elif args.command == 'delete':
        delete_context(args.project_id, args.session_id, args.context_id)
