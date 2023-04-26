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

import uuid

import flaky

import google.auth
from google.cloud import batch_v1
from google.cloud import compute_v1
from google.cloud import resourcemanager_v3
import pytest


from .test_basics import _test_body

from ..create.create_with_template import create_script_job_with_template

PROJECT = google.auth.default()[1]

PROJECT_NUMBER = resourcemanager_v3.ProjectsClient().get_project(name=f"projects/{PROJECT}").name.split("/")[1]

REGION = 'europe-north1'

TIMEOUT = 600  # 10 minutes

WAIT_STATES = {
    batch_v1.JobStatus.State.STATE_UNSPECIFIED,
    batch_v1.JobStatus.State.QUEUED,
    batch_v1.JobStatus.State.RUNNING,
    batch_v1.JobStatus.State.SCHEDULED,
}


@pytest.fixture
def job_name():
    return f"test-job-{uuid.uuid4().hex[:10]}"


@pytest.fixture
def instance_template():
    disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_image = (
        "projects/ubuntu-os-cloud/global/images/family/ubuntu-2204-lts"
    )
    initialize_params.disk_size_gb = 25
    initialize_params.disk_type = 'pd-balanced'
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

    template = compute_v1.InstanceTemplate()
    template.name = "test-template-" + uuid.uuid4().hex[:10]
    template.properties = compute_v1.InstanceProperties()
    template.properties.disks = [disk]
    template.properties.machine_type = "e2-standard-16"
    template.properties.network_interfaces = [network_interface]

    template.properties.scheduling = compute_v1.Scheduling()
    template.properties.scheduling.on_host_maintenance = compute_v1.Scheduling.OnHostMaintenance.MIGRATE.name
    template.properties.scheduling.provisioning_model = compute_v1.Scheduling.ProvisioningModel.STANDARD.name
    template.properties.scheduling.automatic_restart = True

    template.properties.service_accounts = [
        {
            "email": f"{PROJECT_NUMBER}-compute@developer.gserviceaccount.com",
            "scopes": [
                "https://www.googleapis.com/auth/devstorage.read_only",
                "https://www.googleapis.com/auth/logging.write",
                "https://www.googleapis.com/auth/monitoring.write",
                "https://www.googleapis.com/auth/servicecontrol",
                "https://www.googleapis.com/auth/service.management.readonly",
                "https://www.googleapis.com/auth/trace.append"
            ]
        }
    ]

    template_client = compute_v1.InstanceTemplatesClient()
    operation_client = compute_v1.GlobalOperationsClient()
    op = template_client.insert_unary(
        project=PROJECT, instance_template_resource=template
    )
    operation_client.wait(project=PROJECT, operation=op.name)

    template = template_client.get(project=PROJECT, instance_template=template.name)

    yield template

    op = template_client.delete_unary(project=PROJECT, instance_template=template.name)
    operation_client.wait(project=PROJECT, operation=op.name)


@flaky(max_runs=3, min_passes=1)
def test_template_job(job_name, instance_template):
    job = create_script_job_with_template(PROJECT, REGION, job_name, instance_template.self_link)
    _test_body(job)
