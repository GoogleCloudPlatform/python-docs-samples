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

import time

from google.api_core.exceptions import AlreadyExists
from google.cloud.pubsub import SubscriberClient

from grafeas.grafeas_v1 import GrafeasClient
from grafeas.grafeas_v1.gapic.enums import DiscoveryOccurrence
from grafeas.grafeas_v1.gapic.enums import Version
from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport


def tmp_create_client():
    address = "containeranalysis.googleapis.com:443"
    scopes = ("https://www.googleapis.com/auth/cloud-platform")
    transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)
    return GrafeasClient(transport)


# [START containeranalysis_create_note]
def create_note(note_id, project_id):
    client = tmp_create_client()
    project_name = client.project_path(project_id)
    note = {
        "vulnerability": {
            "details": [
                {
                    "affected_cpe_uri": "your-uri-here",
                    "affected_package": "your-package-here",
                    "min_affected_version": {
                        "kind": Version.VersionKind.MINIMUM
                    },
                    "fixed_version": {
                        "kind": Version.VersionKind.MAXIMUM
                    }
                }
            ]
        }
    }
    response = client.create_note(project_name, note_id, note)
    return response
# [END containeranalysis_create_note]


# [START containeranalysis_delete_note]
def delete_note(note_id, project_id):
    client = tmp_create_client()
    note_name = client.note_path(project_id, note_id)

    client.delete_note(note_name)
# [END containeranalysis_delete_note]


# [START ccontaineranalysis_create_occurrence]
def create_occurrence(resource_url, note_id, occurrence_project, note_project):
    client = tmp_create_client()
    formatted_note = client.note_path(note_project, note_id)
    formatted_project = client.project_path(occurrence_project)

    occurrence = {
        "note_name": formatted_note,
        "resource_uri": resource_url,
        "vulnerability": {
            "package_issue": [
                {
                    "affected_cpe_uri": "your-uri-here",
                    "affected_package": "your-package-here",
                    "min_affected_version": {
                        "kind": Version.VersionKind.MINIMUM
                    },
                    "fixed_version": {
                        "kind": Version.VersionKind.MAXIMUM
                    }
                }
            ]
        }
    }

    return client.create_occurrence(formatted_project, occurrence)
# [END containeranalysis_create_occurrence]


# [START containeranalysis_delete_occurrence]
def delete_occurrence(occurrence_id, project_id):
    client = tmp_create_client()
    formatted_parent = client.occurrence_path(project_id, occurrence_id)
    client.delete_occurrence(formatted_parent)
# [END containeranalysis_delete_occurrence]


# [START containeranalysis_get_note]
def get_note(note_id, project_id):
    client = tmp_create_client()
    note_name = client.note_path(project_id, note_id)
    response = client.get_note(note_name)
    return response
# [END containeranalysis_get_note]


# [START containeranalysis_get_occurrence]
def get_occurrence(occurrence_id, project_id):
    client = tmp_create_client()
    formatted_parent = client.occurrence_path(project_id, occurrence_id)
    return client.get_occurrence(formatted_parent)
# [END containeranalysis_get_occurrence]


# [START containeranalysis_discovery_info]
def get_discovery_info(resource_url, project_id):
    filter_str = "kind=\"DISCOVERY\" AND resourceUrl=\"" + resource_url + "\""
    client = tmp_create_client()
    project_name = client.project_path(project_id)
    response = client.list_occurrences(project_name, filter_=filter_str)
    for occ in response:
        print(occ)
# [END containeranalysis_discovery_info]


# [START containeranalysis_occurrences_for_note]
def get_occurrences_for_note(note_id, project_id):
    client = tmp_create_client()
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
    filter_str = "resourceUrl=\"" + resource_url + "\""
    client = tmp_create_client()
    project_name = client.project_path(project_id)

    response = client.list_occurrences(project_name, filter_=filter_str)
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
    for _ in range(timeout_seconds):
        time.sleep(1)
    # print and return the number of pubsub messages received
    print(receiver.msg_count)
    return receiver.msg_count


class MessageReceiver:
    """
    Custom class to handle incoming pubsub messages
    In this case, we will simply print and count each message as it comes in
    """
    def __init__(self):
        # initialize counter to 0 on initialization
        self.msg_count = 0

    def pubsub_callback(self, message):
        # every time a pubsub message comes in, print it and count it
        self.msg_count += 1
        print("Message {}: {}".format(self.msg_count, message.data))
        message.ack()


def create_occurrence_subscription(subscription_id, project_id):
    topic_id = "container-analysis-occurrences-v1beta1"
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


# [START containeranalysis_poll_discovery_occurrence_finished]
def poll_discovery_finished(resource_url, timeout_seconds, project_id):
    deadline = time.time() + timeout_seconds

    client = tmp_create_client()
    project_name = client.project_path(project_id)

    discovery_occurrence = None
    while discovery_occurrence is None:
        time.sleep(1)
        filter_str = 'resourceUrl="{}" \
                      AND noteProjectId="goog-analysis" \
                      AND noteId="PACKAGE_VULNERABILITY"'.format(resource_url)
        # [END containeranalysis_poll_discovery_occurrence_finished]
        # The above filter isn't testable, since it looks for occurrences in a
        # locked down project fall back to a more permissive filter for testing
        filter_str = 'kind="DISCOVERY" AND resourceUrl="{}"'\
            .format(resource_url)
        # [START containeranalysis_poll_discovery_occurrence_finished]
        print(filter_str)
        result = client.list_occurrences(project_name, filter_str)
        # only one occurrence should ever be returned by ListOccurrences
        # and the given filter
        for item in result:
            discovery_occurrence = item
        if time.time() > deadline:
            raise RuntimeError('timeout while retrieving discovery occurrence')

    status = DiscoveryOccurrence.AnalysisStatus.PENDING
    while status != DiscoveryOccurrence.AnalysisStatus.FINISHED_UNSUPPORTED \
            and status != DiscoveryOccurrence.AnalysisStatus.FINISHED_FAILED \
            and status != DiscoveryOccurrence.AnalysisStatus.FINISHED_SUCCESS:
        time.sleep(1)
        updated = client.get_occurrence(discovery_occurrence.name)
        status = updated.discovery.analysis_status
        if time.time() > deadline:
            raise RuntimeError('timeout while waiting for terminal state')
    return discovery_occurrence
# [END containeranalysis_poll_discovery_occurrence_finished]
