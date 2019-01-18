# Copyright 2019, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time
import random
from gcp_devrel.testing.flaky import flaky
import googleapiclient.discovery
from service_account_ssh import main


@flaky
def test_main(capsys):

    compute = googleapiclient.discovery.build('compute', 'v1')

    instance = 'oslogin-service-account-test-' + str(random.randint(0,100000))
    project = os.environ['GCLOUD_PROJECT']
    cmd = 'sudo apt install cowsay -y && cowsay "Test complete!"'
    zone = 'us-central1-f'
    image_family = "projects/debian-cloud/global/images/family/debian-9"
    machine_type = "zones/%s/machineTypes/f1-micro" % zone

    config = {
        'name': instance,
        'machineType': machine_type,

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': image_family,
                }
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/cloud-platform'
            ]
        }],

        # Enable os-login in this instance's metadata.
        'metadata': {
            'items': [{
                'key': 'enable-oslogin',
                'value': 'TRUE'
            }]
        }
    }

    operation = compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()

    while compute.zoneOperations().get(
            project=project, 
            zone=zone, 
            operation=operation['name']).execute()['status'] != 'DONE':
        time.sleep(5)

    # Run the main method from service_account_ssh
    main(cmd, project, instance, zone)

    # Capture the command line output
    out, _ = capsys.readouterr()

    # Test the command line output to make sure the test command is successful.
    assert '< Test complete! >' in out

    # Delete the test instance.
    operation = compute.instances().delete(
            project=project,
            zone=zone,
            instance=instance).execute()

    while compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation['name']).execute()['status'] != 'DONE':
        time.sleep(5)
