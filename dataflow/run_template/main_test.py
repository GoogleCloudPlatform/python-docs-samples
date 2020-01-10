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

import flask
import json
import os
import pytest
import time

from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from werkzeug.urls import url_encode

import main

PROJECT = os.environ['GCLOUD_PROJECT']
BUCKET = os.environ['CLOUD_STORAGE_BUCKET']

dataflow = build('dataflow', 'v1b3')

# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


def test_run_template_python_empty_args(app):
    project = PROJECT
    job = datetime.now().strftime('test_run_template_python-%Y%m%d-%H%M%S')
    template = 'gs://dataflow-templates/latest/Word_Count'
    with pytest.raises(HttpError):
        main.run(project, job, template)


def test_run_template_python(app):
    project = PROJECT
    job = datetime.now().strftime('test_run_template_python-%Y%m%d-%H%M%S')
    template = 'gs://dataflow-templates/latest/Word_Count'
    parameters = {
        'inputFile': 'gs://apache-beam-samples/shakespeare/kinglear.txt',
        'output': 'gs://{}/dataflow/wordcount/outputs'.format(BUCKET),
    }
    res = main.run(project, job, template, parameters)
    dataflow_jobs_cancel(res['job']['id'])


def test_run_template_http_empty_args(app):
    with app.test_request_context():
        with pytest.raises(KeyError):
            main.run_template(flask.request)


def test_run_template_http_url(app):
    args = {
        'project': PROJECT,
        'job': datetime.now().strftime('test_run_template_url-%Y%m%d-%H%M%S'),
        'template': 'gs://dataflow-templates/latest/Word_Count',
        'inputFile': 'gs://apache-beam-samples/shakespeare/kinglear.txt',
        'output': 'gs://{}/dataflow/wordcount/outputs'.format(BUCKET),
    }
    with app.test_request_context('/?' + url_encode(args)):
        res = main.run_template(flask.request)
        data = json.loads(res)
        dataflow_jobs_cancel(data['job']['id'])


def test_run_template_http_data(app):
    args = {
        'project': PROJECT,
        'job': datetime.now().strftime('test_run_template_data-%Y%m%d-%H%M%S'),
        'template': 'gs://dataflow-templates/latest/Word_Count',
        'inputFile': 'gs://apache-beam-samples/shakespeare/kinglear.txt',
        'output': 'gs://{}/dataflow/wordcount/outputs'.format(BUCKET),
    }
    with app.test_request_context(data=args):
        res = main.run_template(flask.request)
        data = json.loads(res)
        dataflow_jobs_cancel(data['job']['id'])


def test_run_template_http_json(app):
    args = {
        'project': PROJECT,
        'job': datetime.now().strftime('test_run_template_json-%Y%m%d-%H%M%S'),
        'template': 'gs://dataflow-templates/latest/Word_Count',
        'inputFile': 'gs://apache-beam-samples/shakespeare/kinglear.txt',
        'output': 'gs://{}/dataflow/wordcount/outputs'.format(BUCKET),
    }
    with app.test_request_context(json=args):
        res = main.run_template(flask.request)
        data = json.loads(res)
        dataflow_jobs_cancel(data['job']['id'])


def dataflow_jobs_cancel(job_id):
    # Wait time until a job can be cancelled, as a best effort.
    # If it fails to be cancelled, the job will run for ~8 minutes.
    time.sleep(5)  # seconds
    request = dataflow.projects().jobs().update(
        projectId=PROJECT,
        jobId=job_id,
        body={'requestedState': 'JOB_STATE_CANCELLED'}
    )
    request.execute()
