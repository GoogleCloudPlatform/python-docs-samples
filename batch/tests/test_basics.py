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
from __future__ import annotations

from collections.abc import Callable
import time
from typing import Tuple
import uuid

from flaky import flaky

import google.auth
from google.cloud import batch_v1, resourcemanager_v3
import pytest

from ..create.create_with_allocation_policy_labels import (
    create_job_with_custom_allocation_policy_labels,
)
from ..create.create_with_container_no_mounting import create_container_job
from ..create.create_with_custom_status_events import create_job_with_status_events
from ..create.create_with_gpu_no_mounting import create_gpu_job
from ..create.create_with_job_labels import create_job_with_custom_job_labels
from ..create.create_with_nfs import create_job_with_network_file_system
from ..create.create_with_persistent_disk import create_with_pd_job
from ..create.create_with_pubsub_notifications import (
    create_with_pubsub_notification_job,
)
from ..create.create_with_runnables_labels import (
    create_job_with_custom_runnables_labels,
)
from ..create.create_with_script_no_mounting import create_script_job
from ..create.create_with_secret_manager import create_with_secret_manager
from ..create.create_with_service_account import create_with_custom_service_account_job
from ..create.create_with_specific_network import create_with_custom_network
from ..create.create_with_ssd import create_local_ssd_job

from ..delete.delete_job import delete_job
from ..get.get_job import get_job
from ..get.get_task import get_task
from ..list.list_jobs import list_jobs
from ..list.list_tasks import list_tasks
from ..logs.read_job_logs import print_job_logs

PROJECT = google.auth.default()[1]
REGION = "europe-central2"
ZONE = "europe-central2-b"
SECRET_NAME = "PERMANENT_BATCH_TESTING"
PROJECT_NUMBER = (
    resourcemanager_v3.ProjectsClient()
    .get_project(name=f"projects/{PROJECT}")
    .name.split("/")[1]
)
LABELS_KEYS = ["label_key1", "label_key2"]
LABELS_VALUES = ["label_value1", "label_value2"]

TIMEOUT = 600  # 10 minutes

WAIT_STATES = {
    batch_v1.JobStatus.State.STATE_UNSPECIFIED,
    batch_v1.JobStatus.State.QUEUED,
    batch_v1.JobStatus.State.RUNNING,
    batch_v1.JobStatus.State.SCHEDULED,
    batch_v1.JobStatus.State.DELETION_IN_PROGRESS,
}


@pytest.fixture
def job_name():
    return f"test-job-{uuid.uuid4().hex[:10]}"


@pytest.fixture()
def service_account() -> str:
    return f"{PROJECT_NUMBER}-compute@developer.gserviceaccount.com"


@pytest.fixture
def disk_name():
    return f"test-disk-{uuid.uuid4().hex[:10]}"


def _test_body(
    test_job: batch_v1.Job,
    additional_test: Callable = None,
    region=REGION,
    project=PROJECT,
):
    start_time = time.time()
    try:
        while test_job.status.state in WAIT_STATES:
            if time.time() - start_time > TIMEOUT:
                pytest.fail("Timed out while waiting for job to complete!")
            test_job = get_job(
                project, region, test_job.name.rsplit("/", maxsplit=1)[1]
            )
            time.sleep(5)

        assert test_job.status.state == batch_v1.JobStatus.State.SUCCEEDED

        for job in list_jobs(project, region):
            if test_job.uid == job.uid:
                break
        else:
            pytest.fail(f"Couldn't find job {test_job.uid} on the list of jobs.")

        if additional_test:
            additional_test()
    finally:
        delete_job(project, region, test_job.name.rsplit("/", maxsplit=1)[1]).result()

    for job in list_jobs(project, region):
        if job.uid == test_job.uid:
            pytest.fail("The test job should be deleted at this point!")


def _check_tasks(job_name):
    tasks = list_tasks(PROJECT, REGION, job_name, "group0")
    assert len(list(tasks)) == 4
    for i in range(4):
        assert get_task(PROJECT, REGION, job_name, "group0", i) is not None
    print("Tasks tested")


def _check_policy(job: batch_v1.Job, job_name: str, disk_names: Tuple[str]):
    assert job_name in job.name
    assert job.allocation_policy.instances[0].policy.disks[0].device_name in disk_names
    assert job.allocation_policy.instances[0].policy.disks[1].device_name in disk_names


def _check_logs(job, capsys):
    print_job_logs(PROJECT, job)
    output = [
        line
        for line in capsys.readouterr().out.splitlines(keepends=False)
        if line != ""
    ]
    assert len(output) == 4
    assert all("Hello world!" in log_msg for log_msg in output)


def _check_service_account(job: batch_v1.Job, service_account_email: str):
    assert job.allocation_policy.service_account.email == service_account_email


def _check_secret_set(job: batch_v1.Job, secret_name: str):
    assert secret_name in job.task_groups[0].task_spec.environment.secret_variables


def _check_notification(job, test_topic):
    notification_found = sum(
        1
        for notif in job.notifications
        if notif.message.new_task_state == batch_v1.TaskStatus.State.FAILED
        or notif.message.new_job_state == batch_v1.JobStatus.State.SUCCEEDED
    )
    assert (
        job.notifications[0].pubsub_topic == f"projects/{PROJECT}/topics/{test_topic}"
    )
    assert notification_found == len(job.notifications)
    assert len(job.notifications) == 2


def _check_custom_events(job: batch_v1.Job):
    display_names = ["Script 1", "Barrier 1", "Script 2"]
    custom_event_found = False
    barrier_name_found = False

    for runnable in job.task_groups[0].task_spec.runnables:
        if runnable.display_name in display_names:
            display_names.remove(runnable.display_name)
        if runnable.barrier.name == "hello-barrier":
            barrier_name_found = True
        if '{"batch/custom/event": "EVENT_DESCRIPTION"}' in runnable.script.text:
            custom_event_found = True

    assert not display_names
    assert custom_event_found
    assert barrier_name_found


def _check_nfs_mounting(
    job: batch_v1.Job, mount_path: str, nfc_ip_address: str, nfs_path: str
):
    expected_script_text = f"{mount_path}/output_task_${{BATCH_TASK_INDEX}}.txt"
    assert job.task_groups[0].task_spec.volumes[0].nfs.server == nfc_ip_address
    assert job.task_groups[0].task_spec.volumes[0].nfs.remote_path == nfs_path
    assert job.task_groups[0].task_spec.volumes[0].mount_path == mount_path
    assert expected_script_text in job.task_groups[0].task_spec.runnables[0].script.text


def _check_custom_networks(job, network_name, subnet_name):
    assert (
        f"/networks/{network_name}"
        in job.allocation_policy.network.network_interfaces[0].network
    )
    assert (
        f"/subnetworks/{subnet_name}"
        in job.allocation_policy.network.network_interfaces[0].subnetwork
    )


def _check_job_labels(job: batch_v1.Job):
    assert job.labels[LABELS_KEYS[0]] == LABELS_VALUES[0]
    assert job.labels[LABELS_KEYS[1]] == LABELS_VALUES[1]


def _check_job_allocation_policy_labels(job: batch_v1.Job):
    assert job.allocation_policy.labels[LABELS_KEYS[0]] == LABELS_VALUES[0]
    assert job.allocation_policy.labels[LABELS_KEYS[1]] == LABELS_VALUES[1]


def _check_runnables_labels(job: batch_v1.Job):
    assert (
        job.task_groups[0].task_spec.runnables[0].labels[LABELS_KEYS[0]]
        == LABELS_VALUES[0]
    )


@flaky(max_runs=3, min_passes=1)
def test_script_job(job_name, capsys):
    job = create_script_job(PROJECT, REGION, job_name)
    _test_body(job, additional_test=lambda: _check_logs(job, capsys))


@flaky(max_runs=3, min_passes=1)
def test_container_job(job_name):
    job = create_container_job(PROJECT, REGION, job_name)
    _test_body(job, additional_test=lambda: _check_tasks(job_name))


@flaky(max_runs=3, min_passes=1)
def test_create_gpu_job(job_name):
    job = create_gpu_job(PROJECT, REGION, ZONE, job_name)
    _test_body(job, additional_test=lambda: _check_tasks)


@flaky(max_runs=3, min_passes=1)
def test_service_account_job(job_name, service_account):
    job = create_with_custom_service_account_job(
        PROJECT, REGION, job_name, service_account
    )
    _test_body(
        job, additional_test=lambda: _check_service_account(job, service_account)
    )


@flaky(max_runs=3, min_passes=1)
def test_secret_manager_job(job_name, service_account):
    secrets = {
        SECRET_NAME: f"projects/{PROJECT_NUMBER}/secrets/{SECRET_NAME}/versions/latest"
    }
    job = create_with_secret_manager(
        PROJECT, REGION, job_name, secrets, service_account
    )
    _test_body(job, additional_test=lambda: _check_secret_set(job, SECRET_NAME))


@flaky(max_runs=3, min_passes=1)
def test_ssd_job(job_name: str, disk_name: str, capsys: "pytest.CaptureFixture[str]"):
    job = create_local_ssd_job(PROJECT, REGION, job_name, disk_name)
    _test_body(job, additional_test=lambda: _check_logs(job, capsys))


@flaky(max_runs=3, min_passes=1)
def test_pd_job(job_name, disk_name):
    region = "europe-north1"
    zone = "europe-north1-c"
    existing_disk_name = "permanent-batch-testing"
    job = create_with_pd_job(
        PROJECT, region, job_name, disk_name, zone, existing_disk_name
    )
    disk_names = (disk_name, existing_disk_name)
    _test_body(
        job,
        additional_test=lambda: _check_policy(job, job_name, disk_names),
        region=region,
    )


@flaky(max_runs=3, min_passes=1)
def test_create_job_with_custom_events(job_name):
    job = create_job_with_status_events(PROJECT, REGION, job_name)
    _test_body(job, additional_test=lambda: _check_custom_events(job))


@flaky(max_runs=3, min_passes=1)
def test_check_notification_job(job_name):
    test_topic = "test_topic"
    job = create_with_pubsub_notification_job(PROJECT, REGION, job_name, test_topic)
    _test_body(job, additional_test=lambda: _check_notification(job, test_topic))


@flaky(max_runs=3, min_passes=1)
def test_check_nfs_job(job_name):
    mount_path = "/mnt/nfs"
    nfc_ip_address = "10.180.103.74"
    nfs_path = "/vol1"
    project_with_nfs_filestore = "python-docs-samples-tests"
    job = create_job_with_network_file_system(
        project_with_nfs_filestore,
        "us-central1",
        job_name,
        mount_path,
        nfc_ip_address,
        nfs_path,
    )
    _test_body(
        job,
        additional_test=lambda: _check_nfs_mounting(
            job, mount_path, nfc_ip_address, nfs_path
        ),
        region="us-central1",
        project=project_with_nfs_filestore,
    )


@flaky(max_runs=3, min_passes=1)
def test_job_with_custom_network(job_name):
    network_name = "default"
    subnet = "default"
    job = create_with_custom_network(PROJECT, REGION, network_name, subnet, job_name)
    _test_body(
        job, additional_test=lambda: _check_custom_networks(job, network_name, subnet)
    )


@flaky(max_runs=3, min_passes=1)
def test_create_job_with_labels(job_name):
    job = create_job_with_custom_job_labels(
        PROJECT,
        REGION,
        job_name,
        labels={LABELS_KEYS[0]: LABELS_VALUES[0], LABELS_KEYS[1]: LABELS_VALUES[1]},
    )
    _test_body(job, additional_test=lambda: _check_job_labels(job))


@flaky(max_runs=3, min_passes=1)
def test_create_job_with_labels_runnables(job_name):
    job = create_job_with_custom_runnables_labels(
        PROJECT, REGION, job_name, {LABELS_KEYS[0]: LABELS_VALUES[0]}
    )
    _test_body(job, additional_test=lambda: _check_runnables_labels(job))


@flaky(max_runs=3, min_passes=1)
def test_create_job_with_labels_allocation_policy(job_name):
    job = create_job_with_custom_allocation_policy_labels(
        PROJECT,
        REGION,
        job_name,
        labels={LABELS_KEYS[0]: LABELS_VALUES[0], LABELS_KEYS[1]: LABELS_VALUES[1]},
    )
    print(job.allocation_policy.labels)
    _test_body(job, additional_test=lambda: _check_job_allocation_policy_labels(job))
