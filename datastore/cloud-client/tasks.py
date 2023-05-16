# Copyright 2016 Google, Inc.
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

from __future__ import annotations

import argparse
import datetime

# [START datastore_add_entity]
# [START datastore_build_service]
# [START datastore_update_entity]
# [START datastore_retrieve_entities]
# [START datastore_delete_entity]
from google.cloud import datastore

# [END datastore_add_entity]
# [END datastore_build_service]
# [END datastore_update_entity]
# [END datastore_retrieve_entities]
# [END datastore_delete_entity]


# [START datastore_build_service]
def create_client(project_id):
    return datastore.Client(project_id)


# [END datastore_build_service]


# [START datastore_add_entity]
def add_task(client: datastore.Client, description: str):
    # Create an incomplete key for an entity of kind "Task". An incomplete
    # key is one where Datastore will automatically generate an Id
    key = client.key("Task")

    # Create an unsaved Entity object, and tell Datastore not to index the
    # `description` field
    task = datastore.Entity(key, exclude_from_indexes=("description",))

    # Apply new field values and save the Task entity to Datastore
    task.update(
        {
            "created": datetime.datetime.now(tz=datetime.timezone.utc),
            "description": description,
            "done": False,
        }
    )
    client.put(task)
    return task.key


# [END datastore_add_entity]


# [START datastore_update_entity]
def mark_done(client: datastore.Client, task_id: str | int):
    with client.transaction():
        # Create a key for an entity of kind "Task", and with the supplied
        # `task_id` as its Id
        key = client.key("Task", task_id)
        # Use that key to load the entity
        task = client.get(key)

        if not task:
            raise ValueError(f"Task {task_id} does not exist.")

        # Update a field indicating that the associated
        # work has been completed
        task["done"] = True

        # Persist the change back to Datastore
        client.put(task)


# [END datastore_update_entity]


# [START datastore_retrieve_entities]
def list_tasks(client: datastore.Client):
    # Create a query against all of your objects of kind "Task"
    query = client.query(kind="Task")
    query.order = ["created"]

    return list(query.fetch())


# [END datastore_retrieve_entities]


# [START datastore_delete_entity]
def delete_task(client: datastore.Client, task_id: str | int):
    # Create a key for an entity of kind "Task", and with the supplied
    # `task_id` as its Id
    key = client.key("Task", task_id)
    # Use that key to delete its associated document, if it exists
    client.delete(key)


# [END datastore_delete_entity]


def format_tasks(tasks):
    lines = []
    for task in tasks:
        if task["done"]:
            status = "done"
        else:
            status = f"created {task['created']}"

        lines.append(f"{task.key.id}: {task['description']} ({status})")

    return "\n".join(lines)


def new_command(client, args):
    """Adds a task with description <description>."""
    task_key = add_task(client, args.description)
    print(f"Task {task_key.id} added.")


def done_command(client, args):
    """Marks a task as done."""
    mark_done(client, args.task_id)
    print(f"Task {args.task_id} marked done.")


def list_command(client, args):
    """Lists all tasks by creation time."""
    print(format_tasks(list_tasks(client)))


def delete_command(client, args):
    """Deletes a task."""
    delete_task(client, args.task_id)
    print(f"Task {args.task_id} deleted.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser.add_argument("--project-id", help="Your cloud project ID.")

    new_parser = subparsers.add_parser("new", help=new_command.__doc__)
    new_parser.set_defaults(func=new_command)
    new_parser.add_argument("description", help="New task description.")

    done_parser = subparsers.add_parser("done", help=done_command.__doc__)
    done_parser.set_defaults(func=done_command)
    done_parser.add_argument("task_id", help="Task ID.", type=int)

    list_parser = subparsers.add_parser("list", help=list_command.__doc__)
    list_parser.set_defaults(func=list_command)

    delete_parser = subparsers.add_parser("delete", help=delete_command.__doc__)
    delete_parser.set_defaults(func=delete_command)
    delete_parser.add_argument("task_id", help="Task ID.", type=int)

    args = parser.parse_args()

    client = create_client(args.project_id)
    args.func(client, args)
