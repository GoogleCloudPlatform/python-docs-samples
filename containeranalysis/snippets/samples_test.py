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

from os import environ
from os.path import basename
import threading
import time
import uuid

from google.api_core.exceptions import AlreadyExists
from google.api_core.exceptions import InvalidArgument
from google.api_core.exceptions import NotFound
from google.cloud.devtools import containeranalysis_v1
from google.cloud.pubsub import PublisherClient, SubscriberClient

from grafeas.grafeas_v1 import DiscoveryOccurrence
from grafeas.grafeas_v1 import NoteKind
from grafeas.grafeas_v1 import Severity
from grafeas.grafeas_v1 import Version
import pytest

import samples

PROJECT_ID = environ['GOOGLE_CLOUD_PROJECT']
SLEEP_TIME = 1
TRY_LIMIT = 20


class MessageReceiver:
    """Custom class to handle incoming Pub/Sub messages."""
    def __init__(self, expected_msg_nums, done_event):
        # initialize counter to 0 on initialization
        self.msg_count = 0
        self.expected_msg_nums = expected_msg_nums
        self.done_event = done_event

    def pubsub_callback(self, message):
        # every time a pubsub message comes in, print it and count it
        self.msg_count += 1
        print(f'Message {self.msg_count}: {message.data}')
        message.ack()
        if (self.msg_count == self.expected_msg_nums):
            self.done_event.set()


class TestContainerAnalysisSamples:

    def setup_method(self, test_method):
        print(f'SETUP {test_method.__name__}')
        self.note_id = f'note-{uuid.uuid4()}'
        self.image_url = f'{uuid.uuid4()}.{test_method.__name__}'
        self.note_obj = samples.create_note(self.note_id, PROJECT_ID)

    def teardown_method(self, test_method):
        print(f'TEAR DOWN {test_method.__name__}')
        try:
            samples.delete_note(self.note_id, PROJECT_ID)
        except NotFound:
            pass

    def test_create_note(self):
        new_note = samples.get_note(self.note_id, PROJECT_ID)
        assert new_note.name == self.note_obj.name

    def test_delete_note(self):
        samples.delete_note(self.note_id, PROJECT_ID)
        try:
            samples.get_note(self.note_obj, PROJECT_ID)
        except InvalidArgument:
            pass
        else:
            # didn't raise exception we expected
            assert (False)

    def test_create_occurrence(self):
        created = samples.create_occurrence(self.image_url,
                                            self.note_id,
                                            PROJECT_ID,
                                            PROJECT_ID)
        retrieved = samples.get_occurrence(basename(created.name), PROJECT_ID)
        assert created.name == retrieved.name
        # clean up
        samples.delete_occurrence(basename(created.name), PROJECT_ID)

    def test_delete_occurrence(self):
        created = samples.create_occurrence(self.image_url,
                                            self.note_id,
                                            PROJECT_ID,
                                            PROJECT_ID)
        samples.delete_occurrence(basename(created.name), PROJECT_ID)
        try:
            samples.get_occurrence(basename(created.name), PROJECT_ID)
        except NotFound:
            pass
        else:
            # didn't raise exception we expected
            assert False

    def test_occurrences_for_image(self):
        orig_count = samples.get_occurrences_for_image(self.image_url,
                                                       PROJECT_ID)
        occ = samples.create_occurrence(self.image_url,
                                        self.note_id,
                                        PROJECT_ID,
                                        PROJECT_ID)
        new_count = 0
        tries = 0
        while new_count != 1 and tries < TRY_LIMIT:
            tries += 1
            new_count = samples.get_occurrences_for_image(self.image_url,
                                                          PROJECT_ID)
            time.sleep(SLEEP_TIME)
        assert new_count == 1
        assert orig_count == 0
        # clean up
        samples.delete_occurrence(basename(occ.name), PROJECT_ID)

    def test_occurrences_for_note(self):
        orig_count = samples.get_occurrences_for_note(self.note_id,
                                                      PROJECT_ID)
        occ = samples.create_occurrence(self.image_url,
                                        self.note_id,
                                        PROJECT_ID,
                                        PROJECT_ID)
        new_count = 0
        tries = 0
        while new_count != 1 and tries < TRY_LIMIT:
            tries += 1
            new_count = samples.get_occurrences_for_note(self.note_id,
                                                         PROJECT_ID)
            time.sleep(SLEEP_TIME)
        assert new_count == 1
        assert orig_count == 0
        # clean up
        samples.delete_occurrence(basename(occ.name), PROJECT_ID)

    @pytest.mark.flaky(max_runs=3, min_passes=1)
    def test_pubsub(self):
        # create topic if needed
        client = SubscriberClient()
        try:
            topic_id = 'container-analysis-occurrences-v1'
            topic_name = {"name": f"projects/{PROJECT_ID}/topics/{topic_id}"}
            publisher = PublisherClient()
            publisher.create_topic(topic_name)
        except AlreadyExists:
            pass

        subscription_id = f'container-analysis-test-{uuid.uuid4()}'
        subscription_name = client.subscription_path(PROJECT_ID,
                                                     subscription_id)
        samples.create_occurrence_subscription(subscription_id, PROJECT_ID)

        # I can not make it pass with multiple messages. My guess is
        # the server started to dedup?
        message_count = 1
        try:
            job_done = threading.Event()
            receiver = MessageReceiver(message_count, job_done)
            client.subscribe(subscription_name, receiver.pubsub_callback)

            for i in range(message_count):
                occ = samples.create_occurrence(
                    self.image_url, self.note_id, PROJECT_ID, PROJECT_ID)
                time.sleep(SLEEP_TIME)
                samples.delete_occurrence(basename(occ.name), PROJECT_ID)
                time.sleep(SLEEP_TIME)
            # We saw occational failure with 60 seconds timeout, so we bumped it
            # to 180 seconds.
            # See also: python-docs-samples/issues/2894
            job_done.wait(timeout=180)
            print(f'done. msg_count = {receiver.msg_count}')
            assert message_count <= receiver.msg_count
        finally:
            # clean up
            client.delete_subscription({"subscription": subscription_name})

    def test_poll_discovery_occurrence_fails(self):
        # try with no discovery occurrence
        try:
            samples.poll_discovery_finished(self.image_url, 5, PROJECT_ID)
        except RuntimeError:
            pass
        else:
            # we expect timeout error
            assert False

    @pytest.mark.flaky(max_runs=3, min_passes=1)
    def test_poll_discovery_occurrence(self):
        # create discovery occurrence
        note_id = f'discovery-note-{uuid.uuid4()}'
        client = containeranalysis_v1.ContainerAnalysisClient()
        grafeas_client = client.get_grafeas_client()
        note = {
            'discovery': {
                'analysis_kind': NoteKind.DISCOVERY
            }
        }
        grafeas_client.\
            create_note(parent=f"projects/{PROJECT_ID}", note_id=note_id, note=note)
        occurrence = {
            'note_name': f"projects/{PROJECT_ID}/notes/{note_id}",
            'resource_uri': self.image_url,
            'discovery': {
                'analysis_status': DiscoveryOccurrence.AnalysisStatus
                                                      .FINISHED_SUCCESS
            }
        }
        created = grafeas_client.\
            create_occurrence(parent=f"projects/{PROJECT_ID}",
                              occurrence=occurrence)

        disc = samples.poll_discovery_finished(self.image_url, 10, PROJECT_ID)
        status = disc.discovery.analysis_status
        assert disc is not None
        assert status == DiscoveryOccurrence.AnalysisStatus.FINISHED_SUCCESS

        # clean up
        samples.delete_occurrence(basename(created.name), PROJECT_ID)
        samples.delete_note(note_id, PROJECT_ID)

    def test_find_vulnerabilities_for_image(self):
        occ_list = samples.find_vulnerabilities_for_image(self.image_url,
                                                          PROJECT_ID)
        assert len(occ_list) == 0

        created = samples.create_occurrence(self.image_url,
                                            self.note_id,
                                            PROJECT_ID,
                                            PROJECT_ID)
        tries = 0
        count = 0
        while count != 1 and tries < TRY_LIMIT:
            tries += 1
            occ_list = samples.find_vulnerabilities_for_image(self.image_url,
                                                              PROJECT_ID)
            count = len(occ_list)
            time.sleep(SLEEP_TIME)
        assert len(occ_list) == 1
        samples.delete_occurrence(basename(created.name), PROJECT_ID)

    def test_find_high_severity_vulnerabilities(self):
        occ_list = samples.find_high_severity_vulnerabilities_for_image(
                self.image_url,
                PROJECT_ID)
        assert len(occ_list) == 0

        # create new high severity vulnerability
        note_id = f'discovery-note-{uuid.uuid4()}'
        client = containeranalysis_v1.ContainerAnalysisClient()
        grafeas_client = client.get_grafeas_client()
        note = {
            'vulnerability': {
                'severity': Severity.CRITICAL,
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
        grafeas_client.\
            create_note(parent=f"projects/{PROJECT_ID}", note_id=note_id, note=note)
        occurrence = {
            'note_name': f"projects/{PROJECT_ID}/notes/{note_id}",
            'resource_uri': self.image_url,
            'vulnerability': {
                'effective_severity': Severity.CRITICAL,
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
        created = grafeas_client.\
            create_occurrence(parent=f"projects/{PROJECT_ID}",
                              occurrence=occurrence)
        # query again
        tries = 0
        count = 0
        while count != 1 and tries < TRY_LIMIT:
            tries += 1
            occ_list = samples.find_vulnerabilities_for_image(self.image_url,
                                                              PROJECT_ID)
            count = len(occ_list)
            time.sleep(SLEEP_TIME)
        assert len(occ_list) == 1
        # clean up
        samples.delete_occurrence(basename(created.name), PROJECT_ID)
        samples.delete_note(note_id, PROJECT_ID)
