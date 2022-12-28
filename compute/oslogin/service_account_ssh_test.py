# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import json
import os
import random
from subprocess import CalledProcessError
import time

import backoff
from google.auth.exceptions import RefreshError
from google.oauth2 import service_account
import googleapiclient.discovery
import pytest

from service_account_ssh import main


'''
The service account that runs this test must have the following roles:
- roles/compute.instanceAdmin.v1
- roles/compute.securityAdmin
- roles/iam.serviceAccountAdmin
- roles/iam.serviceAccountKeyAdmin
- roles/iam.serviceAccountUser
The Project Editor legacy role is not sufficient because it does not grant
several necessary permissions.
'''


def test_main(capsys):
    pytest.skip("We are disabling this test, as it will be replaced.")
    # Initialize variables.
    cmd = 'uname -a'
    project = os.environ['GOOGLE_CLOUD_PROJECT']
    test_id = 'oslogin-test-{id}'.format(id=str(random.randint(0, 1000000)))
    zone = 'us-east1-d'
    image_family = 'projects/debian-cloud/global/images/family/debian-11'
    machine_type = 'zones/{zone}/machineTypes/f1-micro'.format(zone=zone)
    account_email = '{test_id}@{project}.iam.gserviceaccount.com'.format(
        test_id=test_id, project=project)

    # Initialize the necessary APIs.
    iam = googleapiclient.discovery.build(
        'iam', 'v1', cache_discovery=False)
    compute = googleapiclient.discovery.build(
        'compute', 'v1', cache_discovery=False)

    # Create the necessary test resources and retrieve the service account
    # email and account key.
    try:
        print('Creating test resources.')
        service_account_key = setup_resources(
            compute, iam, project, test_id, zone, image_family,
            machine_type, account_email)
    except Exception:
        print('Cleaning up partially created test resources.')
        cleanup_resources(compute, iam, project, test_id, zone, account_email)
        raise Exception('Could not set up the necessary test resources.')

    # Get the target host name for the instance
    hostname = compute.instances().get(
        project=project,
        zone=zone,
        instance=test_id,
        fields='networkInterfaces/accessConfigs/natIP'
    ).execute()['networkInterfaces'][0]['accessConfigs'][0]['natIP']

    # Create a credentials object and use it to initialize the OS Login API.
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(base64.b64decode(
            service_account_key['privateKeyData']).decode('utf-8')))

    oslogin = googleapiclient.discovery.build(
        'oslogin', 'v1', cache_discovery=False, credentials=credentials)
    account = 'users/' + account_email

    # More exceptions could be raised, keeping track of ones I could
    # find for now.
    @backoff.on_exception(backoff.expo,
                          (CalledProcessError,
                           RefreshError),
                          max_tries=5)
    def ssh_login():
        main(cmd, project, test_id, zone, oslogin, account, hostname)
        out, _ = capsys.readouterr()
        assert_value = '{test_id}'.format(test_id=test_id)
        assert assert_value in out

    # Test SSH to the instance.
    ssh_login()
    cleanup_resources(compute, iam, project, test_id, zone, account_email)


def setup_resources(
        compute, iam, project, test_id, zone,
        image_family, machine_type, account_email):

    # Create a temporary service account.
    iam.projects().serviceAccounts().create(
        name='projects/' + project,
        body={
            'accountId': test_id
        }).execute()

    # Wait for the creation to propagate through the system, so the
    # following calls don't fail sometimes.
    time.sleep(5)

    # Grant the service account access to itself.
    iam.projects().serviceAccounts().setIamPolicy(
        resource='projects/' + project + '/serviceAccounts/' + account_email,
        body={
         'policy': {
          'bindings': [
           {
            'members': [
             'serviceAccount:' + account_email
            ],
            'role': 'roles/iam.serviceAccountUser'
           }
          ]
         }
        }).execute()

    # Create a service account key.
    service_account_key = iam.projects().serviceAccounts().keys().create(
        name='projects/' + project + '/serviceAccounts/' + account_email,
        body={}
        ).execute()

    # Create a temporary firewall on the default network to allow SSH tests
    # only for instances with the temporary service account.
    firewall_config = {
        'name': test_id,
        'network': '/global/networks/default',
        'targetServiceAccounts': [
            account_email
        ],
        'sourceRanges': [
            '0.0.0.0/0'
        ],
        'allowed': [{
            'IPProtocol': 'tcp',
            'ports': [
                '22'
            ],
        }]
    }

    compute.firewalls().insert(
        project=project,
        body=firewall_config).execute()

    # Create a new test instance.
    instance_config = {
        'name': test_id,
        'machineType': machine_type,
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': image_family,
                }
            }
        ],
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],
        'serviceAccounts': [{
            'email': account_email,
            'scopes': [
                'https://www.googleapis.com/auth/cloud-platform'
            ]
        }],
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
        body=instance_config).execute()

    # Wait for the instance to start.
    while compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation['name']).execute()['status'] != 'DONE':
        time.sleep(5)

    # Wait for the OS of the instance to be ready to accept SSH connections
    time.sleep(10)

    # Grant the service account osLogin access on the test instance.
    compute.instances().setIamPolicy(
        project=project,
        zone=zone,
        resource=test_id,
        body={
         'bindings': [
          {
           'members': [
            'serviceAccount:' + account_email
           ],
           'role': 'roles/compute.osLogin'
          }
         ]
        }).execute()

    # Wait for the IAM policy to take effect.
    while compute.instances().getIamPolicy(
            project=project,
            zone=zone,
            resource=test_id,
            fields='bindings/role'
            ).execute()['bindings'][0]['role'] != 'roles/compute.osLogin':
        time.sleep(5)

    return service_account_key


def cleanup_resources(compute, iam, project, test_id, zone, account_email):

    # Delete the temporary firewall.
    try:
        compute.firewalls().delete(
                project=project,
                firewall=test_id).execute()
    except Exception:
        pass

    # Delete the test instance.
    try:
        delete = compute.instances().delete(
            project=project, zone=zone, instance=test_id).execute()

        while compute.zoneOperations().get(
                project=project, zone=zone, operation=delete['name']
                ).execute()['status'] != 'DONE':
            time.sleep(5)
    except Exception:
        pass

    # Delete the temporary service account and its associated keys.
    try:
        iam.projects().serviceAccounts().delete(
            name='projects/' + project + '/serviceAccounts/' + account_email
            ).execute()
    except Exception:
        pass
