#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""
The service account that runs this test must have the following roles:
- roles/compute.instanceAdmin.v1
- roles/compute.securityAdmin
- roles/iam.serviceAccountAdmin
- roles/iam.serviceAccountKeyAdmin
- roles/iam.serviceAccountUser
The Project Editor legacy role is not sufficient because it does not grant
several necessary permissions.
"""
import base64
import json
import time
import uuid

from google.api_core.exceptions import BadRequest, NotFound
import google.auth
from google.cloud import compute_v1
from google.cloud import oslogin_v1
from google.oauth2 import service_account
import googleapiclient.discovery
import googleapiclient.errors
import pytest

from oslogin_service_account_ssh import main

PROJECT = google.auth.default()[1]
ZONE = 'europe-north1-a'
TEST_ID = f'oslogin-test-{uuid.uuid4().hex[:10]}'
FIREWALL_TAG = 'ssh-oslogin-test'


@pytest.fixture(scope='module')
def oslogin_service_account():
    account_email = f'{TEST_ID}@{PROJECT}.iam.gserviceaccount.com'

    iam = googleapiclient.discovery.build(
        'iam', 'v1', cache_discovery=False)

    # Create a temporary service account.
    iam.projects().serviceAccounts().create(
        name=f'projects/{PROJECT}',
        body={
            'accountId': TEST_ID
        }).execute()

    # Wait for the creation to propagate through the system, so the
    # following calls don't fail sometimes.
    time.sleep(5)

    # Grant the service account access to itself.
    iam.projects().serviceAccounts().setIamPolicy(
        resource=f'projects/{PROJECT}/serviceAccounts/{account_email}',
        body={
            'policy': {
                'bindings': [
                    {
                        'members': [
                            f'serviceAccount:{account_email}'
                        ],
                        'role': 'roles/iam.serviceAccountUser'
                    }
                ]
            }
        }).execute()

    # Create a service account key.
    service_account_key = iam.projects().serviceAccounts().keys().create(
        name=f'projects/{PROJECT}/serviceAccounts/{account_email}',
        body={},
    ).execute()

    # Create a credentials object and use it to initialize the OS Login API.
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(base64.b64decode(
            service_account_key['privateKeyData']).decode('utf-8')))

    yield {'name': account_email, 'credentials': credentials}

    # Cleanup
    # Delete the temporary service account and its associated keys.
    try:
        iam.projects().serviceAccounts().delete(
            name=f'projects/{PROJECT}/serviceAccounts/{account_email}'
        ).execute()
    except googleapiclient.errors.Error:
        pass


@pytest.fixture()
def ssh_firewall():
    request = compute_v1.InsertFirewallRequest()
    request.project = PROJECT
    request.firewall_resource = compute_v1.Firewall()
    request.firewall_resource.network = '/global/networks/default'
    request.firewall_resource.name = TEST_ID
    request.firewall_resource.target_tags = [FIREWALL_TAG]
    request.firewall_resource.source_ranges = ['0.0.0.0/0']
    request.firewall_resource.allowed = [compute_v1.Allowed()]
    request.firewall_resource.allowed[0].I_p_protocol = "tcp"
    request.firewall_resource.allowed[0].ports = ['22']

    firewall_client = compute_v1.FirewallsClient()
    firewall_client.insert(request).result()

    yield firewall_client.get(project=PROJECT, firewall=TEST_ID)
    try:
        firewall_client.delete(project=PROJECT, firewall=TEST_ID)
    except (NotFound, BadRequest):
        # That means the GCE Enforcer deleted it before us
        pass


@pytest.fixture()
def oslogin_instance(ssh_firewall, oslogin_service_account):
    instance = compute_v1.Instance()
    instance.name = TEST_ID

    disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_image = (
        "projects/ubuntu-os-cloud/global/images/family/ubuntu-2204-lts"
    )
    initialize_params.disk_size_gb = 25
    initialize_params.disk_type = f"zones/{ZONE}/diskTypes/pd-standard"
    disk.initialize_params = initialize_params
    disk.auto_delete = True
    disk.boot = True

    network_interface = compute_v1.NetworkInterface()
    network_interface.name = "global/networks/default"

    access = compute_v1.AccessConfig()
    access.type_ = compute_v1.AccessConfig.Type.ONE_TO_ONE_NAT.name
    access.name = "External NAT"
    access.network_tier = access.NetworkTier.PREMIUM.name
    network_interface.access_configs = [access]

    instance.disks = [disk]
    instance.machine_type = f"zones/{ZONE}/machineTypes/e2-micro"
    instance.network_interfaces = [network_interface]
    instance.tags = compute_v1.Tags()
    instance.tags.items = [FIREWALL_TAG]

    sa = compute_v1.ServiceAccount()
    sa.email = oslogin_service_account['name']
    sa.scopes = ['https://www.googleapis.com/auth/cloud-platform']
    instance.service_accounts = [sa]

    instance.metadata = compute_v1.Metadata()
    item = compute_v1.Items()
    item.key = 'enable-oslogin'
    item.value = 'TRUE'
    instance.metadata.items = [item]
    instance.zone = ZONE

    client = compute_v1.InstancesClient()
    request = compute_v1.InsertInstanceRequest()
    request.project = PROJECT
    request.instance_resource = instance
    request.zone = ZONE

    client.insert(request).result()

    policy = compute_v1.ZoneSetPolicyRequest()
    binding = compute_v1.Binding()
    binding.members = [f'serviceAccount:{oslogin_service_account["name"]}']
    binding.role = 'roles/compute.osLogin'
    policy.bindings = [binding]
    client.set_iam_policy(project=PROJECT, zone=ZONE, resource=TEST_ID, zone_set_policy_request_resource=policy)

    # Wait for everything to propagate
    time.sleep(5)

    yield client.get(project=PROJECT, zone=ZONE, instance=instance.name)

    client.delete(project=PROJECT, zone=ZONE, instance=instance.name).result()


def test_oslogin_ssh(oslogin_instance, oslogin_service_account, capsys):
    account = f'users/{oslogin_service_account["name"]}'
    oslogin_client = oslogin_v1.OsLoginServiceClient(credentials=oslogin_service_account['credentials'])
    # Letting everything settle down...
    time.sleep(60)

    main('uname -a', PROJECT, account=account,
         hostname=oslogin_instance.network_interfaces[0].access_configs[0].nat_i_p,
         oslogin=oslogin_client)

    out, _ = capsys.readouterr()
    assert_value = 'Linux {test_id}'.format(test_id=TEST_ID)
    try:
        assert assert_value in out
    except AssertionError as err:
        fw_client = compute_v1.FirewallsClient()
        try:
            fw_client.get(project=PROJECT, firewall=TEST_ID)
        except NotFound:
            # The test probably failed due to the firewall rule being removed too soon.
            pytest.skip("The test was interrupted by removal of SSH firewall rule.")
        else:
            # The test failed due to some other reason.
            raise err
