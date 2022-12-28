# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import uuid

import backoff

from cloudevents.http import CloudEvent

from google.cloud import compute_v1

import main


INSTANCE_PROJECT = os.getenv('GCLOUD_PROJECT')
INSTANCE_ZONE = os.getenv('FUNCTIONS_COMPUTE_ZONE')
INSTANCE_NAME = os.getenv('FUNCTIONS_COMPUTE_INSTANCE')

instances_client = compute_v1.InstancesClient()

# Avoid race conditions from parallel multi-Python-version CI builds
PYTHON_VERSION = os.getenv('RUN_TESTS_SESSION', '').replace('.', '')
if PYTHON_VERSION:
    INSTANCE_NAME += f'-{PYTHON_VERSION}'


def test_functions_label_gce_instance_should_set_label():
    example_subject = 'compute.googleapis.com/'

    example_subject += f'projects/{INSTANCE_PROJECT}/'
    example_subject += f'zones/{INSTANCE_ZONE}/'
    example_subject += f'instances/{INSTANCE_NAME}'

    example_email = f'{uuid.uuid4().hex}@example.com'

    attributes = {
        'type': '',
        'source': '',
        'subject': example_subject
    }

    data = {
        'protoPayload': {
            'authenticationInfo': {
                'principalEmail': example_email
            },
        }
    }

    event = CloudEvent(attributes, data)

    # Call function
    main.label_gce_instance(event)

    # Run assertions, with exponential backoff
    @backoff.on_exception(backoff.expo, AssertionError, max_time=120)
    def run_assertions():
        # Get labeled instance
        expected_label = re.sub('\\W', '_', example_email)
        labels = instances_client.get(
            project=INSTANCE_PROJECT,
            zone=INSTANCE_ZONE,
            instance=INSTANCE_NAME
        ).labels

        # Check that instance was labelled
        assert 'creator' in labels
        assert labels.get('creator') == expected_label

    run_assertions()
