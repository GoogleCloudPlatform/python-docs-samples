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
from time import sleep, time

from google.api_core.exceptions import AlreadyExists
from google.api_core.exceptions import InvalidArgument
from google.api_core.exceptions import NotFound
from google.cloud.devtools import containeranalysis_v1
from google.cloud.pubsub import PublisherClient, SubscriberClient

from grafeas.grafeas_v1.gapic.enums import DiscoveryOccurrence
from grafeas.grafeas_v1.gapic.enums import NoteKind
from grafeas.grafeas_v1.gapic.enums import Severity
from grafeas.grafeas_v1.gapic.enums import Version

import samples

PROJECT_ID = environ['GCLOUD_PROJECT']
SLEEP_TIME = 1
TRY_LIMIT = 20


class TestContainerAnalysisSamples:

    def setup_method(self, test_method):
        print('SETUP {}'.format(test_method.__name__))
        timestamp = str(int(time()))
        self.note_id = 'note-{}-{}'.format(timestamp, test_method.__name__)
        self.image_url = '{}.{}'.format(timestamp, test_method.__name__)
        self.note_obj = samples.create_note(self.note_id, PROJECT_ID)

    def teardown_method(self, test_method):
        print('TEAR DOWN {}'.format(test_method.__name__))
        try:
            samples.delete_note(self.note_id, PROJECT_ID)
        except NotFound:
            pass

    def test_create_note(self):
        new_note = samples.get_note(self.note_id, PROJECT_ID)
        if new_note.name != self.note_obj.name:
            raise AssertionError

    def test_delete_note(self):
        samples.delete_note(self.note_id, PROJECT_ID)
        try:
            samples.get_note(self.note_obj, PROJECT_ID)
        except InvalidArgument:
            pass
        else:
            # didn't raise exception we expected
            if not (False):
                raise AssertionError

    def test_create_occurrence(self):
        created = samples.create_occurrence(self.image_url,
                                            self.note_id,
                                            PROJECT_ID,
                                            PROJECT_ID)
        retrieved = samples.get_occurrence(basename(created.name), PROJECT_ID)
        if created.name != retrieved.name:
            raise AssertionError
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
            if not False:
                raise AssertionError

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
            sleep(SLEEP_TIME)
        if new_count != 1:
            raise AssertionError
        if orig_count != 0:
            raise AssertionError
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
            sleep(SLEEP_TIME)
        if new_count != 1:
            raise AssertionError
        if orig_count != 0:
            raise AssertionError
        # clean up
        samples.delete_occurrence(basename(occ.name), PROJECT_ID)

    def test_pubsub(self):
        # create topic if needed
        client = SubscriberClient()
        try:
            topic_id = 'container-analysis-occurrences-v1'
            topic_name = client.topic_path(PROJECT_ID, topic_id)
            publisher = PublisherClient()
            publisher.create_topic(topic_name)
        except AlreadyExists:
            pass

        subscription_id = 'drydockOccurrences'
        subscription_name = client.subscription_path(PROJECT_ID,
                                                     subscription_id)
        samples.create_occurrence_subscription(subscription_id, PROJECT_ID)
        tries = 0
        success = False
        while not success and tries < TRY_LIMIT:
            print(tries)
            tries += 1
            receiver = samples.MessageReceiver()
            client.subscribe(subscription_name, receiver.pubsub_callback)

            # test adding 3 more occurrences
            total_created = 3
            for _ in range(total_created):
                occ = samples.create_occurrence(self.image_url,
                                                self.note_id,
                                                PROJECT_ID,
                                                PROJECT_ID)
                sleep(SLEEP_TIME)
                samples.delete_occurrence(basename(occ.name), PROJECT_ID)
                sleep(SLEEP_TIME)
            print('done. msg_count = {}'.format(receiver.msg_count))
            success = receiver.msg_count == total_created
        if receiver.msg_count != total_created:
            raise AssertionError
        # clean up
        client.delete_subscription(subscription_name)

    def test_poll_discovery_occurrence(self):
        # try with no discovery occurrence
        try:
            samples.poll_discovery_finished(self.image_url, 5, PROJECT_ID)
        except RuntimeError:
            pass
        else:
            # we expect timeout error
            if not False:
                raise AssertionError

        # create discovery occurrence
        note_id = 'discovery-note-{}'.format(int(time()))
        client = containeranalysis_v1.ContainerAnalysisClient()
        grafeas_client = client.get_grafeas_client()
        note = {
            'discovery': {
                'analysis_kind': NoteKind.DISCOVERY
            }
        }
        grafeas_client.\
            create_note(grafeas_client.project_path(PROJECT_ID), note_id, note)
        occurrence = {
            'note_name': grafeas_client.note_path(PROJECT_ID, note_id),
            'resource_uri': self.image_url,
            'discovery': {
                'analysis_status': DiscoveryOccurrence.AnalysisStatus
                                                      .FINISHED_SUCCESS
            }
        }
        created = grafeas_client.\
            create_occurrence(grafeas_client.project_path(PROJECT_ID),
                              occurrence)

        # poll again
        disc = samples.poll_discovery_finished(self.image_url, 10, PROJECT_ID)
        status = disc.discovery.analysis_status
        if disc is None:
            raise AssertionError
        if status != DiscoveryOccurrence.AnalysisStatus.FINISHED_SUCCESS:
            raise AssertionError

        # clean up
        samples.delete_occurrence(basename(created.name), PROJECT_ID)
        samples.delete_note(note_id, PROJECT_ID)

    def test_find_vulnerabilities_for_image(self):
        occ_list = samples.find_vulnerabilities_for_image(self.image_url,
                                                          PROJECT_ID)
        if len(occ_list) != 0:
            raise AssertionError

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
            sleep(SLEEP_TIME)
        if len(occ_list) != 1:
            raise AssertionError
        samples.delete_occurrence(basename(created.name), PROJECT_ID)

    def test_find_high_severity_vulnerabilities(self):
        occ_list = samples.find_high_severity_vulnerabilities_for_image(
                self.image_url,
                PROJECT_ID)
        if len(occ_list) != 0:
            raise AssertionError

        # create new high severity vulnerability
        note_id = 'discovery-note-{}'.format(int(time()))
        client = containeranalysis_v1.ContainerAnalysisClient()
        grafeas_client = client.get_grafeas_client()
        note = {
            'vulnerability': {
                'severity': Severity.CRITICAL,
                'details': [
                    {
                        'affected_cpe_uri': 'your-uri-here',
                        'affected_package': 'your-package-here',
                        'min_affected_version': {
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
            create_note(grafeas_client.project_path(PROJECT_ID), note_id, note)
        occurrence = {
            'note_name': client.note_path(PROJECT_ID, note_id),
            'resource_uri': self.image_url,
            'vulnerability': {
                'package_issue': [
                    {
                        'affected_cpe_uri': 'your-uri-here',
                        'affected_package': 'your-package-here',
                        'min_affected_version': {
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
            create_occurrence(grafeas_client.project_path(PROJECT_ID),
                              occurrence)
        # query again
        tries = 0
        count = 0
        while count != 1 and tries < TRY_LIMIT:
            tries += 1
            occ_list = samples.find_vulnerabilities_for_image(self.image_url,
                                                              PROJECT_ID)
            count = len(occ_list)
            sleep(SLEEP_TIME)
        if len(occ_list) != 1:
            raise AssertionError
        # clean up
        samples.delete_occurrence(basename(created.name), PROJECT_ID)
        samples.delete_note(note_id, PROJECT_ID)
