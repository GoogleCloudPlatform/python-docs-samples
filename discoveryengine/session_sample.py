# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# [START discoveryengine_create_session]
from google.cloud import discoveryengine_v1 as discoveryengine


def create_session(
    project_id: str,
    location: str,
    data_store_id: str,
    user_pseudo_id: str,
) -> discoveryengine.Session:
    """Creates a session.

    Args:
        project_id: The ID of your Google Cloud project.
        location: The location of the data store.
        data_store_id: The ID of the data store.
        user_pseudo_id: A unique identifier for tracking visitors. For example, this
          could be implemented with an HTTP cookie, which should be able to
          uniquely identify a visitor on a single device.
    Returns:
        discoveryengine.Session: The newly created Session.
    """

    client = discoveryengine.ConversationalSearchServiceClient()

    # The full resource name of the data store
    parent = client.data_store_path(
        project=project_id, location=location, data_store=data_store_id
    )

    session = discoveryengine.Session(user_pseudo_id=user_pseudo_id)

    response = client.create_session(parent=parent, session=session)

    print(f"Session: {response.name}")
    return response


# [END discoveryengine_create_session]


# [START discoveryengine_delete_session]
from google.cloud import discoveryengine_v1 as discoveryengine


def delete_session(
    project_id: str,
    location: str,
    data_store_id: str,
    session_id: str,
) -> None:
    """Deletes a session.

    Args:
        project_id: The ID of your Google Cloud project.
        location: The location of the data store.
        data_store_id: The ID of the data store.
        session_id: The ID of the session.
    """

    client = discoveryengine.ConversationalSearchServiceClient()

    # The full resource name of the session
    name = client.session_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        session=session_id,
    )

    client.delete_session(name=name)

    print(f"Session {name} deleted.")


# [END discoveryengine_delete_session]


# [START discoveryengine_update_session]
from google.cloud import discoveryengine_v1 as discoveryengine
from google.protobuf import field_mask_pb2


def update_session(
    project_id: str,
    location: str,
    data_store_id: str,
    session_id: str,
    new_state: discoveryengine.Session.State,
) -> discoveryengine.Session:
    """Updates a session.

    Args:
        project_id: The ID of your Google Cloud project.
        location: The location of the data store.
        data_store_id: The ID of the data store.
        session_id: The ID of the session.
        new_state: The new value for the state.
    Returns:
        discoveryengine.Session: The updated Session.
    """
    client = discoveryengine.ConversationalSearchServiceClient()

    # The full resource name of the session
    name = client.session_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        session=session_id,
    )

    session = discoveryengine.Session(name=name, state=new_state)
    update_mask = field_mask_pb2.FieldMask(paths=["state"])
    response = client.update_session(session=session, update_mask=update_mask)
    print(f"Updated session: {response.name}")
    return response


# [END discoveryengine_update_session]


# [START discoveryengine_list_sessions]
from google.cloud import discoveryengine_v1 as discoveryengine


def list_sessions(
    project_id: str, location: str, data_store_id: str
) -> discoveryengine.ListSessionsResponse:
    """Lists all sessions associated with a data store.

    Args:
        project_id: The ID of your Google Cloud project.
        location: The location of the data store.
        data_store_id: The ID of the data store.
    Returns:
        discoveryengine.ListSessionsResponse: The list of sessions.
    """

    client = discoveryengine.ConversationalSearchServiceClient()

    # The full resource name of the data store
    parent = client.data_store_path(
        project=project_id, location=location, data_store=data_store_id
    )

    response = client.list_sessions(parent=parent)
    print("Sessions:")
    for session in response.sessions:
        print(session)

    return response


# [END discoveryengine_list_sessions]


# [START discoveryengine_list_sessions_with_filter]
from google.cloud import discoveryengine_v1 as discoveryengine


def list_sessions_with_filter(
    project_id: str, location: str, data_store_id: str, user_pseudo_id: str
) -> discoveryengine.ListSessionsResponse:
    """Lists all sessions associated with a user or visitor.

    Args:
        project_id: The ID of your Google Cloud project.
        location: The location of the data store.
        data_store_id: The ID of the data store.
        user_pseudo_id: The pseudo ID of the user whose sessions you want to list.
    Returns:
        discoveryengine.ListSessionsResponse: The list of sessions.
    """

    client = discoveryengine.ConversationalSearchServiceClient()

    # The full resource name of the data store
    parent = client.data_store_path(
        project=project_id, location=location, data_store=data_store_id
    )
    filter = f'userPseudoId="{user_pseudo_id}"'

    response = client.list_sessions(parent=parent, filter=filter)
    print("Sessions:")
    for session in response.sessions:
        print(session)

    return response


# [END discoveryengine_list_sessions_with_filter]
