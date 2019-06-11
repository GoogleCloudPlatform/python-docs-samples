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


# [START containeranalysis_create_note]
def create_note(note_id, project_id):
    client = container_analysis_client.ContainerAnalysisClient()
    parent = client.project_path(project_id)

    type = package_vulnerability_pb2.VulnerabilityType()
    note = containeranalysis_pb2.Note(vulnerability_type=type)
    response = client.create_note(parent, note_id, note)
    return response
# [END containeranalysis_create_note]


# [START containeranalysis_delete_note]
def delete_note(note_id, project_id):
    client = container_analysis_client.ContainerAnalysisClient()
    note_name = client.note_path(project_id, note_id)

    client.delete_note(note_name)
# [END containeranalysis_delete_note]


# [START ccontaineranalysis_create_occurrence]
def create_occurrence(resource_url, note_id, occurrence_project, note_project):
    client = container_analysis_client.ContainerAnalysisClient()
    formatted_note = client.note_path(note_project, note_id)
    formatted_project = client.project_path(occurrence_project)
    vul = package_vulnerability_pb2.VulnerabilityType.VulnerabilityDetails()

    occurrence = containeranalysis_pb2.Occurrence(note_name=formatted_note,
                                                  resource_url=resource_url,
                                                  vulnerability_details=vul)
    return client.create_occurrence(formatted_project, occurrence)
# [END containeranalysis_create_occurrence]


# [START containeranalysis_delete_occurrence]
def delete_occurrence(occurrence_id, project_id):
    client = container_analysis_client.ContainerAnalysisClient()
    formatted_parent = client.occurrence_path(project_id, occurrence_id)
    client.delete_occurrence(formatted_parent)
# [END containeranalysis_delete_occurrence]


# [START containeranalysis_get_note]
def get_note(note_id, project_id):
    client = container_analysis_client.ContainerAnalysisClient()
    note_name = client.note_path(project_id, note_id)
    response = client.get_note(note_name)
    return response
# [END containeranalysis_get_note]


# [START containeranalysis_get_occurrence]
def get_occurrence(occurrence_id, project_id):
    client = container_analysis_client.ContainerAnalysisClient()
    formatted_parent = client.occurrence_path(project_id, occurrence_id)
    return client.get_occurrence(formatted_parent)
# [END containeranalysis_get_occurrence]


# [START containeranalysis_discovery_info]
def get_discovery_info(resource_url, project_id):
    filterStr = "kind=\"DISCOVERY\" AND resourceUrl=\"" + resource_url + "\""
    client = container_analysis_client.ContainerAnalysisClient()
    project_name = client.project_path(project_id)
    response = client.list_occurrences(project_name, filter_=filterStr)
    for occ in response:
        print(occ)
# [END containeranalysis_discovery_info]


# [START containeranalysis_occurrences_for_note]
def get_occurrences_for_note(note_id, project_id):
    client = container_analysis_client.ContainerAnalysisClient()
    note_name = client.note_path(project_id, note_id)

    response = client.list_note_occurrences(note_name)
    count = 0
    for o in response:
        # do something with the retrieved occurrence
        # in this sample, we will simply count each one
        count += 1
    return count
# [END containeranalysis_occurrences_for_note]


# [START containeranalysis_occurrences_for_image]
def get_occurrences_for_image(resource_url, project_id):
    filterStr = "resourceUrl=\"" + resource_url + "\""
    client = container_analysis_client.ContainerAnalysisClient()
    project_name = client.project_path(project_id)

    response = client.list_occurrences(project_name, filter_=filterStr)
    count = 0
    for o in response:
        # do something with the retrieved occurrence
        # in this sample, we will simply count each one
        count += 1
    return count
# [END containeranalysis_occurrences_for_image]


# [START containeranalysis_pubsub]
def pubsub(subscription_id, timeout_seconds, project_id):
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
# [END containeranalysis_pubsub]
