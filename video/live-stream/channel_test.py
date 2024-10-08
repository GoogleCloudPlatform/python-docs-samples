# Copyright 2022 Google LLC.
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

import os
import uuid

from google.api_core.exceptions import FailedPrecondition, NotFound
from google.protobuf import empty_pb2 as empty
import pytest

import create_channel
import create_channel_with_backup_input
import create_input
import delete_channel
import delete_channel_event
import delete_input
import get_channel
import list_channel_events
import list_channels
import start_channel
import stop_channel
import update_channel
import utils

project_name = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "us-central1"
input_id = f"python-test-input-{uuid.uuid4()}"
updated_input_id = f"python-test-up-input-{uuid.uuid4()}"
channel_id = f"python-test-channel-{uuid.uuid4()}"
output_bucket_name = f"python-test-bucket-{uuid.uuid4()}"
output_uri = f"gs://{output_bucket_name}/channel-test/"


def test_channel_operations(capsys: pytest.fixture) -> None:
    # Clean up old resources in the test project
    channel_responses = list_channels.list_channels(project_name, location)

    for response in channel_responses:
        next_channel_id = response.name.rsplit("/", 1)[-1]
        input_attachments = response.input_attachments
        if utils.is_resource_stale(response.create_time):
            try:
                event_responses = list_channel_events.list_channel_events(
                    project_name, location, next_channel_id
                )
                for response in event_responses:
                    next_event_id = response.name.rsplit("/", 1)[-1]
                    try:
                        delete_channel_event.delete_channel_event(
                            project_name, location, next_channel_id, next_event_id
                        )
                    except NotFound as e:
                        print(f"Ignoring NotFound, details: {e}")
                try:
                    stop_channel.stop_channel(project_name, location, next_channel_id)
                except FailedPrecondition as e:
                    print(f"Ignoring FailedPrecondition, details: {e}")
                try:
                    delete_channel.delete_channel(
                        project_name, location, next_channel_id
                    )
                except FailedPrecondition as e:
                    print(f"Ignoring FailedPrecondition, try to stop channel: {e}")
                    try:
                        stop_channel.stop_channel(
                            project_name, location, next_channel_id
                        )
                    except FailedPrecondition as e:
                        print(f"Ignoring FailedPrecondition, details: {e}")
                except NotFound as e:
                    print(f"Ignoring NotFound, details: {e}")
            except NotFound as e:
                print(f"Ignoring NotFound, details: {e}")

            for input_attachment in input_attachments:
                next_input_id = input_attachment.input.rsplit("/", 1)[-1]
                try:
                    delete_input.delete_input(project_name, location, next_input_id)
                except NotFound as e:
                    print(f"Ignoring NotFound, details: {e}")

    # Set up

    channel_name_project_id = (
        f"projects/{project_name}/locations/{location}/channels/{channel_id}"
    )

    create_input.create_input(project_name, location, input_id)
    create_input.create_input(project_name, location, updated_input_id)

    # Tests

    response = create_channel.create_channel(
        project_name, location, channel_id, input_id, output_uri
    )
    assert channel_name_project_id in response.name

    list_channels.list_channels(project_name, location)
    out, _ = capsys.readouterr()
    assert channel_name_project_id in out

    response = update_channel.update_channel(
        project_name, location, channel_id, updated_input_id
    )
    assert channel_name_project_id in response.name
    for input_attachment in response.input_attachments:
        assert "updated-input" in input_attachment.key

    response = get_channel.get_channel(project_name, location, channel_id)
    assert channel_name_project_id in response.name

    start_channel.start_channel(project_name, location, channel_id)
    out, _ = capsys.readouterr()
    assert "Started channel" in out

    stop_channel.stop_channel(project_name, location, channel_id)
    out, _ = capsys.readouterr()
    assert "Stopped channel" in out

    response = delete_channel.delete_channel(project_name, location, channel_id)
    assert response == empty.Empty()

    response = create_channel_with_backup_input.create_channel_with_backup_input(
        project_name, location, channel_id, input_id, updated_input_id, output_uri
    )
    assert channel_name_project_id in response.name

    # Clean up

    delete_channel.delete_channel(project_name, location, channel_id)
    delete_input.delete_input(project_name, location, input_id)
    delete_input.delete_input(project_name, location, updated_input_id)
