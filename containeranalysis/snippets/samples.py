#!/bin/python
# Copyright 2019 Google LLC
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


# [START containeranalysis_create_note]
def create_note(note_id, project_id):
    """Creates and returns a new vulnerability note."""
    # note_id = 'my-note'
    # project_id = 'my-gcp-project'

    from grafeas.grafeas_v1 import Version
    from google.cloud.devtools import containeranalysis_v1

    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    project_name = f"projects/{project_id}"
    note = {
        'vulnerability': {
            'details': [
                {
                    'affected_cpe_uri': 'your-uri-here',
                    'affected_package': 'your-package-here',
                    'affected_version_start': {
                        'kind': Version.VersionKind.MINIMUM
                    },
                    'fixed_version': {
                        'kind': Version.VersionKind.MAXIMUM
                    }
                }
            ]
        }
    }
    response = grafeas_client.create_note(parent=project_name, note_id=note_id, note=note)
    return response
# [END containeranalysis_create_note]


# [START containeranalysis_delete_note]
def delete_note(note_id, project_id):
    """Removes an existing note from the server."""
    # note_id = 'my-note'
    # project_id = 'my-gcp-project'

    from google.cloud.devtools import containeranalysis_v1

    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    note_name = f"projects/{project_id}/notes/{note_id}"

    grafeas_client.delete_note(name=note_name)
# [END containeranalysis_delete_note]


# [START containeranalysis_create_occurrence]
def create_occurrence(resource_url, note_id, occurrence_project, note_project):
    """ Creates and returns a new occurrence of a previously
    created vulnerability note."""
    # resource_url = 'https://gcr.io/my-project/my-image@sha256:123'
    # note_id = 'my-note'
    # occurrence_project = 'my-gcp-project'
    # note_project = 'my-gcp-project'

    from grafeas.grafeas_v1 import Version
    from google.cloud.devtools import containeranalysis_v1

    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    formatted_note = f"projects/{note_project}/notes/{note_id}"
    formatted_project = f"projects/{occurrence_project}"

    occurrence = {
        'note_name': formatted_note,
        'resource_uri': resource_url,
        'vulnerability': {
            'package_issue': [
                {
                    'affected_cpe_uri': 'your-uri-here',
                    'affected_package': 'your-package-here',
                    'affected_version': {
                        'kind': Version.VersionKind.MINIMUM
                    },
                    'fixed_version': {
                        'kind': Version.VersionKind.MAXIMUM
                    }
                }
            ]
        }
    }

    return grafeas_client.create_occurrence(parent=formatted_project, occurrence=occurrence)
# [END containeranalysis_create_occurrence]


# [START containeranalysis_delete_occurrence]
def delete_occurrence(occurrence_id, project_id):
    """Removes an existing occurrence from the server."""
    # occurrence_id = basename(occurrence.name)
    # project_id = 'my-gcp-project'

    from google.cloud.devtools import containeranalysis_v1

    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    parent = f"projects/{project_id}/occurrences/{occurrence_id}"
    grafeas_client.delete_occurrence(name=parent)
# [END containeranalysis_delete_occurrence]


# [START containeranalysis_get_note]
def get_note(note_id, project_id):
    """Retrieves and prints a specified note from the server."""
    # note_id = 'my-note'
    # project_id = 'my-gcp-project'

    from google.cloud.devtools import containeranalysis_v1

    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    note_name = f"projects/{project_id}/notes/{note_id}"
    response = grafeas_client.get_note(name=note_name)
    return response
# [END containeranalysis_get_note]


# [START containeranalysis_get_occurrence]
def get_occurrence(occurrence_id, project_id):
    """retrieves and prints a specified occurrence from the server."""
    # occurrence_id = basename(occurrence.name)
    # project_id = 'my-gcp-project'

    from google.cloud.devtools import containeranalysis_v1

    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    parent = f"projects/{project_id}/occurrences/{occurrence_id}"
    return grafeas_client.get_occurrence(name=parent)
# [END containeranalysis_get_occurrence]


# [START containeranalysis_discovery_info]
def get_discovery_info(resource_url, project_id):
    """Retrieves and prints the discovery occurrence created for a specified
    image. The discovery occurrence contains information about the initial
    scan on the image."""
    # resource_url = 'https://gcr.io/my-project/my-image@sha256:123'
    # project_id = 'my-gcp-project'

    from google.cloud.devtools import containeranalysis_v1

    filter_str = 'kind="DISCOVERY" AND resourceUrl="{}"'.format(resource_url)
    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    project_name = f"projects/{project_id}"
    response = grafeas_client.list_occurrences(parent=project_name,
                                               filter_=filter_str)
    for occ in response:
        print(occ)
# [END containeranalysis_discovery_info]


# [START containeranalysis_occurrences_for_note]
def get_occurrences_for_note(note_id, project_id):
    """Retrieves all the occurrences associated with a specified Note.
    Here, all occurrences are printed and counted."""
    # note_id = 'my-note'
    # project_id = 'my-gcp-project'

    from google.cloud.devtools import containeranalysis_v1

    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    note_name = f"projects/{project_id}/notes/{note_id}"

    response = grafeas_client.list_note_occurrences(name=note_name)
    count = 0
    for o in response:
        # do something with the retrieved occurrence
        # in this sample, we will simply count each one
        count += 1
    return count
# [END containeranalysis_occurrences_for_note]


# [START containeranalysis_occurrences_for_image]
def get_occurrences_for_image(resource_url, project_id):
    """Retrieves all the occurrences associated with a specified image.
    Here, all occurrences are simply printed and counted."""
    # resource_url = 'https://gcr.io/my-project/my-image@sha256:123'
    # project_id = 'my-gcp-project'

    from google.cloud.devtools import containeranalysis_v1

    filter_str = 'resourceUrl="{}"'.format(resource_url)
    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    project_name = f"projects/{project_id}"

    response = grafeas_client.list_occurrences(parent=project_name,
                                               filter=filter_str)
    count = 0
    for o in response:
        # do something with the retrieved occurrence
        # in this sample, we will simply count each one
        count += 1
    return count
# [END containeranalysis_occurrences_for_image]


# [START containeranalysis_pubsub]
def pubsub(subscription_id, timeout_seconds, project_id):
    """Respond to incoming occurrences using a Cloud Pub/Sub subscription."""
    # subscription_id := 'my-occurrences-subscription'
    # timeout_seconds = 20
    # project_id = 'my-gcp-project'

    import time
    from google.cloud.pubsub import SubscriberClient

    client = SubscriberClient()
    subscription_name = client.subscription_path(project_id, subscription_id)
    receiver = MessageReceiver()
    client.subscribe(subscription_name, receiver.pubsub_callback)

    # listen for 'timeout' seconds
    for _ in range(timeout_seconds):
        time.sleep(1)
    # print and return the number of pubsub messages received
    print(receiver.msg_count)
    return receiver.msg_count


class MessageReceiver:
    """Custom class to handle incoming Pub/Sub messages."""
    def __init__(self):
        # initialize counter to 0 on initialization
        self.msg_count = 0

    def pubsub_callback(self, message):
        # every time a pubsub message comes in, print it and count it
        self.msg_count += 1
        print('Message {}: {}'.format(self.msg_count, message.data))
        message.ack()


def create_occurrence_subscription(subscription_id, project_id):
    """Creates a new Pub/Sub subscription object listening to the
    Container Analysis Occurrences topic."""
    # subscription_id := 'my-occurrences-subscription'
    # project_id = 'my-gcp-project'

    from google.api_core.exceptions import AlreadyExists
    from google.cloud.pubsub import SubscriberClient

    topic_id = 'container-analysis-occurrences-v1'
    client = SubscriberClient()
    topic_name = f"projects/{project_id}/topics/{topic_id}"
    subscription_name = client.subscription_path(project_id, subscription_id)
    success = True
    try:
        client.create_subscription({"name": subscription_name, "topic": topic_name})
    except AlreadyExists:
        # if subscription already exists, do nothing
        pass
    else:
        success = False
    return success
# [END containeranalysis_pubsub]


# [START containeranalysis_poll_discovery_occurrence_finished]
def poll_discovery_finished(resource_url, timeout_seconds, project_id):
    """Returns the discovery occurrence for a resource once it reaches a
    terminal state."""
    # resource_url = 'https://gcr.io/my-project/my-image@sha256:123'
    # timeout_seconds = 20
    # project_id = 'my-gcp-project'

    import time
    from grafeas.grafeas_v1 import DiscoveryOccurrence
    from google.cloud.devtools import containeranalysis_v1

    deadline = time.time() + timeout_seconds

    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    project_name = f"projects/{project_id}"

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
        result = grafeas_client.list_occurrences(parent=project_name, filter=filter_str)
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
        updated = grafeas_client.get_occurrence(name=discovery_occurrence.name)
        status = updated.discovery.analysis_status
        if time.time() > deadline:
            raise RuntimeError('timeout while waiting for terminal state')
    return discovery_occurrence
# [END containeranalysis_poll_discovery_occurrence_finished]


# [START containeranalysis_vulnerability_occurrences_for_image]
def find_vulnerabilities_for_image(resource_url, project_id):
    """"Retrieves all vulnerability occurrences associated with a resource."""
    # resource_url = 'https://gcr.io/my-project/my-image@sha256:123'
    # project_id = 'my-gcp-project'

    from google.cloud.devtools import containeranalysis_v1

    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    project_name = f"projects/{project_id}"

    filter_str = 'kind="VULNERABILITY" AND resourceUrl="{}"'\
        .format(resource_url)
    return list(grafeas_client.list_occurrences(parent=project_name, filter=filter_str))
# [END containeranalysis_vulnerability_occurrences_for_image]


# [START containeranalysis_filter_vulnerability_occurrences]
def find_high_severity_vulnerabilities_for_image(resource_url, project_id):
    """Retrieves a list of only high vulnerability occurrences associated
    with a resource."""
    # resource_url = 'https://gcr.io/my-project/my-image@sha256:123'
    # project_id = 'my-gcp-project'

    from grafeas.grafeas_v1 import Severity
    from google.cloud.devtools import containeranalysis_v1

    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()
    project_name = f"projects/{project_id}"

    filter_str = 'kind="VULNERABILITY" AND resourceUrl="{}"'\
        .format(resource_url)
    vulnerabilities = grafeas_client.list_occurrences(parent=project_name, filter=filter_str)
    filtered_list = []
    for v in vulnerabilities:
        if v.vulnerability.effective_severity == Severity.HIGH or v.vulnerability.effective_severity == Severity.CRITICAL:
            filtered_list.append(v)
    return filtered_list
# [END containeranalysis_filter_vulnerability_occurrences]
