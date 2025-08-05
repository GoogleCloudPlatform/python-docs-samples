# flake8: noqa: E402, I100
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


# [START genappbuilder_create_session]
from google.cloud import discoveryengine_v1 as discoveryengine


def create_session(
    project_id: str,
    location: str,
    engine_id: str,
    user_pseudo_id: str,
) -> discoveryengine.Session:
    """Creates a session.

    Args:
        project_id: The ID of your Google Cloud project.
        location: The location of the app.
        engine_id: The ID of the app.
        user_pseudo_id: A unique identifier for tracking visitors. For example, this
          could be implemented with an HTTP cookie, which should be able to
          uniquely identify a visitor on a single device.
    Returns:
        discoveryengine.Session: The newly created Session.
    """

    client = discoveryengine.ConversationalSearchServiceClient()

    session = client.create_session(
        # The full resource name of the engine
        parent=f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}",
        session=discoveryengine.Session(user_pseudo_id=user_pseudo_id),
    )

    # Send Session name in `answer_query()`
    print(f"Session: {session.name}")
    return session


# [END genappbuilder_create_session]

# [START genappbuilder_get_session]
from google.cloud import discoveryengine_v1 as discoveryengine


def get_session(
    project_id: str,
    location: str,
    engine_id: str,
    session_id: str,
) -> discoveryengine.Session:
    """Retrieves a session.

    Args:
        project_id: The ID of your Google Cloud project.
        location: The location of the app.
        engine_id: The ID of the app.
        session_id: The ID of the session.
    """

    client = discoveryengine.ConversationalSearchServiceClient()

    # The full resource name of the session
    name = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/sessions/{session_id}"

    session = client.get_session(name=name)

    print(f"Session details: {session}")
    return session


# [END genappbuilder_get_session]


# [START genappbuilder_delete_session]
from google.cloud import discoveryengine_v1 as discoveryengine


def delete_session(
    project_id: str,
    location: str,
    engine_id: str,
    session_id: str,
) -> None:
    """Deletes a session.

    Args:
        project_id: The ID of your Google Cloud project.
        location: The location of the app.
        engine_id: The ID of the app.
        session_id: The ID of the session.
    """

    client = discoveryengine.ConversationalSearchServiceClient()

    # The full resource name of the session
    name = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/sessions/{session_id}"

    client.delete_session(name=name)

    print(f"Session {name} deleted.")


# [END genappbuilder_delete_session]


# [START genappbuilder_update_session]
from google.cloud import discoveryengine_v1 as discoveryengine
from google.protobuf import field_mask_pb2


def update_session(
    project_id: str,
    location: str,
    engine_id: str,
    session_id: str,
) -> discoveryengine.Session:
    """Updates a session.

    Args:
        project_id: The ID of your Google Cloud project.
        location: The location of the app.
        engine_id: The ID of the app.
        session_id: The ID of the session.
    Returns:
        discoveryengine.Session: The updated Session.
    """
    client = discoveryengine.ConversationalSearchServiceClient()

    # The full resource name of the session
    name = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/sessions/{session_id}"

    session = discoveryengine.Session(
        name=name,
        state=discoveryengine.Session.State.IN_PROGRESS,  # Options: IN_PROGRESS, STATE_UNSPECIFIED
    )

    # Fields to Update
    update_mask = field_mask_pb2.FieldMask(paths=["state"])

    session = client.update_session(session=session, update_mask=update_mask)
    print(f"Updated session: {session.name}")
    return session


# [END genappbuilder_update_session]


# [START genappbuilder_list_sessions]
from google.cloud import discoveryengine_v1 as discoveryengine


def list_sessions(
    project_id: str,
    location: str,
    engine_id: str,
) -> discoveryengine.ListSessionsResponse:
    """Lists all sessions associated with a data store.

    Args:
        project_id: The ID of your Google Cloud project.
        location: The location of the app.
        engine_id: The ID of the app.
    Returns:
        discoveryengine.ListSessionsResponse: The list of sessions.
    """

    client = discoveryengine.ConversationalSearchServiceClient()

    # The full resource name of the engine
    parent = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}"

    response = client.list_sessions(
        request=discoveryengine.ListSessionsRequest(
            parent=parent,
            filter='state="IN_PROGRESS"',  # Optional: Filter requests by userPseudoId or state
            order_by="update_time",  # Optional: Sort results
        )
    )

    print("Sessions:")
    for session in response.sessions:
        print(session)

    return response


# [END genappbuilder_list_sessions]
