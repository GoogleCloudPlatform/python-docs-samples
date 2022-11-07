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
import time
from typing import Callable
import uuid

import google.auth
from google.cloud import batch_v1
import pytest

from ..create.create_with_container_no_mounting import create_container_job
from ..create.create_with_script_no_mounting import create_script_job

from ..delete.delete_job import delete_job
from ..get.get_job import get_job
from ..get.get_task import get_task
from ..list.list_jobs import list_jobs
from ..list.list_tasks import list_tasks
from ..logs.read_job_logs import print_job_logs

PROJECT = google.auth.default()[1]
REGION = 'europe-north1'

TIMEOUT = 600  # 10 minutes

WAIT_STATES = {
    batch_v1.JobStatus.State.STATE_UNSPECIFIED,
    batch_v1.JobStatus.State.QUEUED,
    batch_v1.JobStatus.State.RUNNING,
    batch_v1.JobStatus.State.SCHEDULED,
    batch_v1.JobStatus.State.DELETION_IN_PROGRESS
}


@pytest.fixture
def job_name():
    return f"test-job-{uuid.uuid4().hex[:10]}"


def _test_body(test_job: batch_v1.Job, additional_test: Callable = None):
    start_time = time.time()
    try:
        while test_job.status.state in WAIT_STATES:
            if time.time() - start_time > TIMEOUT:
                pytest.fail("Timed out while waiting for job to complete!")
            test_job = get_job(PROJECT, REGION, test_job.name.rsplit('/', maxsplit=1)[1])
            time.sleep(5)

        assert test_job.status.state == batch_v1.JobStatus.State.SUCCEEDED

        for job in list_jobs(PROJECT, REGION):
            if test_job.uid == job.uid:
                break
        else:
            pytest.fail(f"Couldn't find job {test_job.uid} on the list of jobs.")

        if additional_test:
            additional_test()
    finally:
        delete_job(PROJECT, REGION, test_job.name.rsplit('/', maxsplit=1)[1]).result()

    for job in list_jobs(PROJECT, REGION):
        if job.uid == test_job.uid:
            pytest.fail("The test job should be deleted at this point!")


def _check_tasks(job_name):
    tasks = list_tasks(PROJECT, REGION, job_name, 'group0')
    assert len(list(tasks)) == 4
    for i in range(4):
        assert get_task(PROJECT, REGION, job_name, 'group0', i) is not None
    print('Tasks tested')


def _check_logs(job, capsys):
    print_job_logs(PROJECT, job)
    output = [line for line in capsys.readouterr().out.splitlines(keepends=False) if line != ""]
    assert len(output) == 4
    assert all("Hello world!" in log_msg for log_msg in output)


def test_script_job(job_name, capsys):
    job = create_script_job(PROJECT, REGION, job_name)
    _test_body(job, additional_test=lambda: _check_logs(job, capsys))


def test_container_job(job_name):
    job = create_container_job(PROJECT, REGION, job_name)
    _test_body(job, additional_test=lambda: _check_tasks(job_name))
