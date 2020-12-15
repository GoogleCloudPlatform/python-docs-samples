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

import flask
import json
import os
import pytest
import subprocess as sp
import time

from datetime import datetime
from werkzeug.urls import url_encode

import main

PROJECT = os.environ['GCLOUD_PROJECT']
BUCKET = os.environ['CLOUD_STORAGE_BUCKET']

# Wait time until a job can be cancelled, as a best effort.
# If it fails to be cancelled, the job will run for ~8 minutes.
WAIT_TIME = 5  # seconds

# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


def test_run_template_empty_args(app):
    with app.test_request_context():
        with pytest.raises(KeyError):
            main.run_template(flask.request)


def test_run_template_url(app):
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
        job_id = data['job']['id']
        time.sleep(WAIT_TIME)
        if sp.call(['gcloud', 'dataflow', 'jobs', 'cancel', job_id]) != 0:
            raise AssertionError


def test_run_template_data(app):
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
        job_id = data['job']['id']
        time.sleep(WAIT_TIME)
        if sp.call(['gcloud', 'dataflow', 'jobs', 'cancel', job_id]) != 0:
            raise AssertionError


def test_run_template_json(app):
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
        job_id = data['job']['id']
        time.sleep(WAIT_TIME)
        if sp.call(['gcloud', 'dataflow', 'jobs', 'cancel', job_id]) != 0:
            raise AssertionError
