# Copyright 2016, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import datetime

# [START build_service]
from google.cloud import datastore


def create_client(project_id):
    return datastore.Client(project_id)
# [END build_service]


# [START add_entity]
def add_task(client, description):
    key = client.key('Task')

    task = datastore.Entity(
        key, exclude_from_indexes=['description'])

    task.update({
        'created': datetime.datetime.utcnow(),
        'description': description,
        'done': False
    })

    client.put(task)

    return task.key
# [END add_entity]


# [START update_entity]
def mark_done(client, task_id):
    with client.transaction():
        key = client.key('Task', task_id)
        task = client.get(key)

        if not task:
            raise ValueError(
                'Task {} does not exist.'.format(task_id))

        task['done'] = True

        client.put(task)
# [END update_entity]


# [START retrieve_entities]
def list_tasks(client):
    query = client.query(kind='Task')
    query.order = ['created']

    return list(query.fetch())
# [END retrieve_entities]


# [START delete_entity]
def delete_task(client, task_id):
    key = client.key('Task', task_id)
    client.delete(key)
# [END delete_entity]


# [START format_results]
def format_tasks(tasks):
    lines = []
    for task in tasks:
        if task['done']:
            status = 'done'
        else:
            status = 'created {}'.format(task['created'])

        lines.append('{}: {} ({})'.format(
            task.key.id, task['description'], status))

    return '\n'.join(lines)
# [END format_results]


def new_command(client, args):
    """Adds a task with description <description>."""
    task_key = add_task(client, args.description)
    print('Task {} added.'.format(task_key.id))


def done_command(client, args):
    """Marks a task as done."""
    mark_done(client, args.task_id)
    print('Task {} marked done.'.format(args.task_id))


def list_command(client, args):
    """Lists all tasks by creation time."""
    print(format_tasks(list_tasks(client)))


def delete_command(client, args):
    """Deletes a task."""
    delete_task(client, args.task_id)
    print('Task {} deleted.'.format(args.task_id))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser.add_argument('--project-id', help='Your cloud project ID.')

    new_parser = subparsers.add_parser('new', help=new_command.__doc__)
    new_parser.set_defaults(func=new_command)
    new_parser.add_argument('description', help='New task description.')

    done_parser = subparsers.add_parser('done', help=done_command.__doc__)
    done_parser.set_defaults(func=done_command)
    done_parser.add_argument('task_id', help='Task ID.', type=int)

    list_parser = subparsers.add_parser('list', help=list_command.__doc__)
    list_parser.set_defaults(func=list_command)

    delete_parser = subparsers.add_parser(
        'delete', help=delete_command.__doc__)
    delete_parser.set_defaults(func=delete_command)
    delete_parser.add_argument('task_id', help='Task ID.', type=int)

    args = parser.parse_args()

    client = create_client(args.project_id)
    args.func(client, args)
