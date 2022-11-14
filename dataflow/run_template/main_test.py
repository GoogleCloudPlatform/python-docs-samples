# Copyright 2019 Google LLC
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

# To run the tests:
#   nox -s "lint(sample='./dataflow/run_template')"
#   nox -s "py27(sample='./dataflow/run_template')"
#   nox -s "py36(sample='./dataflow/run_template')"

from datetime import datetime
import json
import os
import uuid

import backoff
import flask

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pytest

from werkzeug.urls import url_encode

# Relative imports cannot be found when running in `nox`, but we still
# try to import it for the autocomplete when writing the tests.
try:
    from . import main
except ImportError:
    import main


RETRY_MAX_TIME = 5 * 60  # 5 minutes in seconds

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BUCKET = os.environ["CLOUD_STORAGE_BUCKET"]

dataflow = build("dataflow", "v1b3")


# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


# fixture used to create user-friendly names with UUIDs for Dataflow jobs
# indirect parametrization inspired by this post https://stackoverflow.com/questions/42228895/how-to-parametrize-a-pytest-fixture
@pytest.fixture(scope="function")
def dataflow_job_name(request):
    label = request.param
    job_name = datetime.now().strftime(
        "{}-%Y%m%d-%H%M%S-{}".format(label, uuid.uuid4().hex[:5])
    )

    yield job_name

    # cancel the Dataflow job after running the test
    # no need to cancel after the empty_args test - it won't create a job and cancellation will throw an error
    if label != "test-run-template-empty":
        dataflow_jobs_cancel(job_name)
    else:
        print("No active jobs to cancel, cancelling skipped.")


# Takes in a Dataflow job name and returns its job ID
def get_job_id_from_name(job_name):
    # list the 50 most recent Dataflow jobs
    jobs_request = (
        dataflow.projects()
        .jobs()
        .list(
            projectId=PROJECT,
            filter="ACTIVE",
            pageSize=50,  # only return the 50 most recent results - our job is likely to be in here. If the job is not found, first try increasing this number. For more info see:https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.jobs/list
        )
    )
    response = jobs_request.execute()

    try:
        # search for the job in the list that has our name (names are unique)
        for job in response["jobs"]:
            if job["name"] == job_name:
                return job["id"]
        # if we don't find a job, just return
        return
    except Exception as e:
        raise ValueError(f"response:\n{response}") from e


# We retry the cancel operation a few times until the job is in a state where it can be cancelled
@backoff.on_exception(backoff.expo, HttpError, max_time=RETRY_MAX_TIME)
def dataflow_jobs_cancel(job_name):
    # to cancel a dataflow job, we need its ID, not its name
    job_id = get_job_id_from_name(job_name)

    if job_id:
        # Cancel the Dataflow job if it exists. If it doesn't, job_id will be equal to None. For more info, see: https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.jobs/update
        request = (
            dataflow.projects()
            .jobs()
            .update(
                projectId=PROJECT,
                jobId=job_id,
                body={"requestedState": "JOB_STATE_CANCELLED"},
            )
        )
        request.execute()


@pytest.mark.parametrize(
    "dataflow_job_name", [("test-run-template-empty")], indirect=True
)
def test_run_template_python_empty_args(app, dataflow_job_name):
    project = PROJECT
    template = "gs://dataflow-templates/latest/Word_Count"
    with pytest.raises(HttpError):
        main.run(project, dataflow_job_name, template)


@pytest.mark.parametrize(
    "dataflow_job_name", [("test-run-template-python")], indirect=True
)
def test_run_template_python(app, dataflow_job_name):
    project = PROJECT
    template = "gs://dataflow-templates/latest/Word_Count"
    parameters = {
        "inputFile": "gs://apache-beam-samples/shakespeare/kinglear.txt",
        "output": "gs://{}/dataflow/wordcount/outputs".format(BUCKET),
    }
    res = main.run(project, dataflow_job_name, template, parameters)
    assert dataflow_job_name in res["job"]["name"]


def test_run_template_http_empty_args(app):
    with app.test_request_context():
        with pytest.raises(KeyError):
            main.run_template(flask.request)


@pytest.mark.parametrize(
    "dataflow_job_name", [("test-run-template-url")], indirect=True
)
def test_run_template_http_url(app, dataflow_job_name):
    args = {
        "project": PROJECT,
        "job": dataflow_job_name,
        "template": "gs://dataflow-templates/latest/Word_Count",
        "inputFile": "gs://apache-beam-samples/shakespeare/kinglear.txt",
        "output": "gs://{}/dataflow/wordcount/outputs".format(BUCKET),
    }
    with app.test_request_context("/?" + url_encode(args)):
        res = main.run_template(flask.request)
        data = json.loads(res)
        assert dataflow_job_name in data["job"]["name"]


@pytest.mark.parametrize(
    "dataflow_job_name", [("test-run-template-data")], indirect=True
)
def test_run_template_http_data(app, dataflow_job_name):
    args = {
        "project": PROJECT,
        "job": dataflow_job_name,
        "template": "gs://dataflow-templates/latest/Word_Count",
        "inputFile": "gs://apache-beam-samples/shakespeare/kinglear.txt",
        "output": "gs://{}/dataflow/wordcount/outputs".format(BUCKET),
    }
    with app.test_request_context(data=args):
        res = main.run_template(flask.request)
        data = json.loads(res)
        assert dataflow_job_name in data["job"]["name"]


@pytest.mark.parametrize(
    "dataflow_job_name", [("test-run-template-json")], indirect=True
)
def test_run_template_http_json(app, dataflow_job_name):
    args = {
        "project": PROJECT,
        "job": dataflow_job_name,
        "template": "gs://dataflow-templates/latest/Word_Count",
        "inputFile": "gs://apache-beam-samples/shakespeare/kinglear.txt",
        "output": "gs://{}/dataflow/wordcount/outputs".format(BUCKET),
    }
    with app.test_request_context(json=args):
        res = main.run_template(flask.request)
        data = json.loads(res)
        assert dataflow_job_name in data["job"]["name"]
