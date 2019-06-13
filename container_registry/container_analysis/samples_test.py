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

from os import environ
from os.path import basename
from time import sleep, time

from google.api_core.exceptions import InvalidArgument
from google.api_core.exceptions import NotFound
from google.cloud.pubsub import SubscriberClient

from grafeas.grafeas_v1.gapic.enums import DiscoveryOccurrence, NoteKind

import samples

PROJECT_ID = environ['GCLOUD_PROJECT']
SLEEP_TIME = 1
TRY_LIMIT = 20


class TestContainerAnalysisSamples:

    def setup_method(self, test_method):
        print("SETUP " + test_method.__name__)
        timestamp = str(int(time()))
        self.note_id = "note-" + timestamp + test_method.__name__
        self.image_url = "www." + timestamp + test_method.__name__ + ".com"
        self.note_obj = samples.create_note(self.note_id, PROJECT_ID)

    def teardown_method(self, test_method):
        print("TEAR DOWN " + test_method.__name__)
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
            sleep(SLEEP_TIME)
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
            sleep(SLEEP_TIME)
        assert new_count == 1
        assert orig_count == 0
        # clean up
        samples.delete_occurrence(basename(occ.name), PROJECT_ID)

    def test_pubsub(self):
        client = SubscriberClient()
        subscription_id = "drydockOccurrences"
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
            print('done. msg_count = ' + str(receiver.msg_count))
            success = receiver.msg_count == total_created
        assert receiver.msg_count == total_created
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
            assert False

        # create discovery occurrence
        note_id = "discovery-note-" + str(int(time()))
        client = samples.tmp_create_client()
        note = {
            "discovery": {
                "analysis_kind": NoteKind.DISCOVERY
            }
        }
        client.create_note(client.project_path(PROJECT_ID), note_id, note)
        occurrence = {
            "note_name": client.note_path(PROJECT_ID, note_id),
            "resource_uri": self.image_url,
            "discovery": {
                "analysis_status": DiscoveryOccurrence.AnalysisStatus
                                                      .FINISHED_SUCCESS
            }
        }
        created = client.create_occurrence(client.project_path(PROJECT_ID),
                                           occurrence)

        # poll again
        disc = samples.poll_discovery_finished(self.image_url, 10, PROJECT_ID)
        status = disc.discovery.analysis_status
        assert disc is not None
        assert status == DiscoveryOccurrence.AnalysisStatus.FINISHED_SUCCESS

        # clean up
        samples.delete_occurrence(basename(created.name), PROJECT_ID)
        samples.delete_note(note_id, PROJECT_ID)
