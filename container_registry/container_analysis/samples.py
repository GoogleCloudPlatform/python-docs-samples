#!/bin/python
# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from time import sleep

from google.api_core.exceptions import AlreadyExists
from google.cloud.devtools.containeranalysis_v1 \
    import container_analysis_client
from google.cloud.devtools.containeranalysis_v1.proto \
    import containeranalysis_pb2
from google.cloud.pubsub import SubscriberClient


# [START create_note]
def create_note(note_id, project_id):
    """Creates and returns a new note

    :param note_id: A user-specified identifier for the note.
    :param project_id: the GCP project the note will be created under
    :return: the newly created note
    :raises
        google.api_core.exceptions.GoogleAPICallError: If the request
            failed for any reason.
        google.api_core.exceptions.RetryError: If the request failed due
            to a retryable error and retry attempts failed.
        ValueError: If the parameters are invalid.
    """
    client = container_analysis_client.ContainerAnalysisClient()
    parent = client.project_path(project_id)

    type = package_vulnerability_pb2.VulnerabilityType()
    note = containeranalysis_pb2.Note(vulnerability_type=type)
    response = client.create_note(parent, note_id, note)
    return response
# [END create_note]


# [START create_occurrence]
def create_occurrence(image_url, parent_note_id, project_id):
    """Creates and returns a new occurrence

    :param image_url: the Container Registry URL associated with the image
                example: "https://gcr.io/project/image@sha256:foo"
    :param parent_note_id: the identifier of the associated note
    :param project_id: the GCP project the occurrence will be created under
    :return: the newly created occurrence
    :raises
        google.api_core.exceptions.GoogleAPICallError: If the request
            failed for any reason.
        google.api_core.exceptions.RetryError: If the request failed due
            to a retryable error and retry attempts failed.
        ValueError: If the parameters are invalid.
    """
    client = container_analysis_client.ContainerAnalysisClient()
    parent_name = client.note_path(project_id, parent_note_id)
    project_name = client.project_path(project_id)
    vul = package_vulnerability_pb2.VulnerabilityType.VulnerabilityDetails()

    occurrence = containeranalysis_pb2.Occurrence(note_name=parent_name,
                                                  resource_url=image_url,
                                                  vulnerability_details=vul)
    return client.create_occurrence(project_name, occurrence)
# [END create_occurrence]


# [START update_note]
def update_note(updated, note_id, project_id):
    """Makes an update to an existing note

    :param updated: a Note object representing the desired updates to push
    :param note_id: the identifier of the existing note
    :param project_id: the GCP project the occurrence will be created under.
    :raises
        google.api_core.exceptions.GoogleAPICallError: If the request
            failed for any reason.
        google.api_core.exceptions.RetryError: If the request failed due
            to a retryable error and retry attempts failed.
        ValueError: If the parameters are invalid.
    """
    client = container_analysis_client.ContainerAnalysisClient()
    note_name = client.note_path(project_id, note_id)

    client.update_note(note_name, updated)
# [END update_note]


# [START update_occurrence]
def update_occurrence(updated, occurrence_name):
    """Makes an update to an existing occurrence

    :param updated: an Occurrence object representing the desired updates
    :param occurrence_name: the name of the occurrence to delete.
                in format "projects/{projectId}/occurrences/{occurrence_id}"
    :raises
        google.api_core.exceptions.GoogleAPICallError: If the request
            failed for any reason.
        google.api_core.exceptions.RetryError: If the request failed due
            to a retryable error and retry attempts failed.
        ValueError: If the parameters are invalid.
    """
    client = container_analysis_client.ContainerAnalysisClient()
    client.update_occurrence(occurrence_name, updated)
# [END update_occurrence]


# [START delete_note]
def delete_note(note_id, project_id):
    """Deletes an existing note

    :param note_id: the identifier of the note to delete
    :param project_id: the GCP project the occurrence will be created under
    :raises
        google.api_core.exceptions.GoogleAPICallError: If the request
            failed for any reason.
        google.api_core.exceptions.RetryError: If the request failed due
            to a retryable error and retry attempts failed.
        ValueError: If the parameters are invalid.
    """
    client = container_analysis_client.ContainerAnalysisClient()
    note_name = client.note_path(project_id, note_id)

    client.delete_note(note_name)
# [END delete_note]


# [START delete_occurrence]
def delete_occurrence(occurrence_name):
    """Deletes an existing occurrence

    :param occurrence_name: the name of the occurrence to delete.
                in format "projects/{projectId}/occurrences/{occurrence_id}"
    :raises
        google.api_core.exceptions.GoogleAPICallError: If the request
            failed for any reason.
        google.api_core.exceptions.RetryError: If the request failed due
            to a retryable error and retry attempts failed.
        ValueError: If the parameters are invalid.
    """
    client = container_analysis_client.ContainerAnalysisClient()
    client.delete_occurrence(occurrence_name)
# [END delete_occurrence]


# [START get_note]
def get_note(note_id, project_id):
    """Retrieves a note based on it's noteId and projectId

    :param note_id: the note's unique identifier
    :param project_id: the project's unique identifier
    :return: the specified Note object
    :raises
        google.api_core.exceptions.GoogleAPICallError: If the request
            failed for any reason.
        google.api_core.exceptions.RetryError: If the request failed due
            to a retryable error and retry attempts failed.
        ValueError: If the parameters are invalid.
    """
    client = container_analysis_client.ContainerAnalysisClient()
    note_name = client.note_path(project_id, note_id)
    response = client.get_note(note_name)
    return response
# [END get_note]


# [START get_occurrence]
def get_occurrence(occurrence_name):
    """Retrieves an occurrence based on it's name

    :param occurrence_name: the name of the occurrence to delete.
                in format "projects/{projectId}/occurrences/{occurrence_id}"
    :return: the specified Occurrence object
    :raises
        google.api_core.exceptions.GoogleAPICallError: If the request
            failed for any reason.
        google.api_core.exceptions.RetryError: If the request failed due
            to a retryable error and retry attempts failed.
        ValueError: If the parameters are invalid.
    """
    client = container_analysis_client.ContainerAnalysisClient()
    return client.get_occurrence(occurrence_name)
# [END get_occurrence]


# [START discovery_info]
def get_discovery_info(image_url, project_id):
    """prints the Discovery occurrence created for a specified image
    This occurrence contains information about the initial scan on the image

    :param image_url:  the Container Registry URL associated with the image
                example: "https://gcr.io/project/image@sha256:foo"
    :param project_id: the GCP project the occurrence will be created under
    :raises
        google.api_core.exceptions.GoogleAPICallError: If the request
            failed for any reason.
        google.api_core.exceptions.RetryError: If the request failed due
            to a retryable error and retry attempts failed.
        ValueError: If the parameters are invalid.
    """
    filterStr = "kind=\"DISCOVERY\" AND resourceUrl=\"" + image_url + "\""
    client = container_analysis_client.ContainerAnalysisClient()
    project_name = client.project_path(project_id)
    response = client.list_occurrences(project_name, filter_=filterStr)
    for occ in response:
        print(occ)
# [END discovery_info]


# [START occurrences_for_note]
def get_occurrences_for_note(note_id, project_id):
    """Retrieves all the occurrences associated with a specified note

    :param note_id: the note's unique identifier
    :param project_id: the project's unique identifier
    :return: number of occurrences found
    :raises
        google.api_core.exceptions.GoogleAPICallError: If the request
            failed for any reason.
        google.api_core.exceptions.RetryError: If the request failed due
            to a retryable error and retry attempts failed.
        ValueError: If the parameters are invalid.
    """
    client = container_analysis_client.ContainerAnalysisClient()
    note_name = client.note_path(project_id, note_id)

    response = client.list_note_occurrences(note_name)
    count = 0
    for o in response:
        # do something with the retrieved occurrence
        # in this sample, we will simply count each one
        count += 1
    return count
# [END occurrences_for_note]


# [START occurrences_for_image]
def get_occurrences_for_image(image_url, project_id):
    """Retrieves all the occurrences associated with a specified image

    :param note_id: the note's unique identifier
    :param project_id: the project's unique identifier
    :return: number of occurrences found
    :raises
        google.api_core.exceptions.GoogleAPICallError: If the request
            failed for any reason.
        google.api_core.exceptions.RetryError: If the request failed due
            to a retryable error and retry attempts failed.
        ValueError: If the parameters are invalid.
    """
    filterStr = "resourceUrl=\"" + image_url + "\""
    client = container_analysis_client.ContainerAnalysisClient()
    project_name = client.project_path(project_id)

    response = client.list_occurrences(project_name, filter_=filterStr)
    count = 0
    for o in response:
        # do something with the retrieved occurrence
        # in this sample, we will simply count each one
        count += 1
    return count
# [END occurrences_for_image]


# [START pubsub]
def pubsub(subscription_id, timeout, project_id):
    """Handle incoming occurrences using a pubsub subscription

    :param subscription_id: the user-specified identifier for the subscription
    :param timeout: the number of seconds to listen for pubsub messages
    :param project_id: the project's unique identifier
    :return: number of occurrence pubsub messages received
    """
    client = SubscriberClient()
    subscription_name = client.subscription_path(project_id, subscription_id)
    receiver = MessageReceiver()
    client.subscribe(subscription_name, receiver.pubsub_callback)

    # listen for 'timeout' seconds
    print("listening")
    for _ in range(timeout):
        sleep(1)
    # print and return the number of pubsub messages received
    print(receiver.msg_count)
    return receiver.msg_count


class MessageReceiver:
    """Custom class to handle incoming pubsub messages
    In this case, we will simply print and count each message as it comes in
    """
    def __init__(self):
        # initialize counter to 0 on initialization
        self.msg_count = 0

    def pubsub_callback(self, message):
        # every time a pubsub message comes in, print it and count it
        self.msg_count += 1
        print("Message " + str(self.msg_count) + ": " + message.data)
        message.ack()


def create_occurrence_subscription(subscription_id, project_id):
    """Creates and returns a pubsub subscription listening to the
    occurrence topic. This topic provides updates when occurrences are modified

    :param subscription_id: the user-specified identifier for the subscription
    :param project_id: the project's unique identifier
    :return: a bool indicating whether the subscription is ready to use
             if the subscription was already created, it will return True
    :raises
        google.api_core.exceptions.GoogleAPICallError: If the request
            failed for any reason.
        google.api_core.exceptions.RetryError: If the request failed due
            to a retryable error and retry attempts failed.
        ValueError: If the parameters are invalid.
    """
    topic_id = "resource-notes-occurrences-v1alpha1"
    client = SubscriberClient()
    topic_name = client.topic_path(project_id, topic_id)
    subscription_name = client.subscription_path(project_id, subscription_id)
    success = True
    try:
        client.create_subscription(subscription_name, topic_name)
    except AlreadyExists:
        # if subscription already exists, do nothing
        pass
    else:
        success = False
    return success
# [END pubsub]
