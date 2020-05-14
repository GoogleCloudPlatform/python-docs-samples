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
import time
import uuid

import flask
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pytest
import backoff
from werkzeug.urls import url_encode

import main


PROJECT = os.environ['GCLOUD_PROJECT']
BUCKET = os.environ['CLOUD_STORAGE_BUCKET']

dataflow = build('dataflow', 'v1b3')


# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)




@pytest.fixture(scope="function")
def dataflow_job_id(request):
    label = request.param
    print("label")
    print(label)
    job_id = datetime.now().strftime('{}-%Y%m%d-%H%M%S-{}'.format(
        label, uuid.uuid4().hex[:5]))
    print(job_id)

    
    yield job_id

    dataflow_jobs_cancel(job_id)

#TODO address infinite loop
@backoff.on_exception(backoff.expo, HttpError, max_time=120)
def dataflow_jobs_cancel(job_id):
     # Wait time until the job can be cancelled.
        state = None
        while state != 'JOB_STATE_RUNNING':
            job = dataflow.projects().jobs().get(
                projectId=PROJECT,
                jobId=job_id
            ).execute()
            state = job['currentState']
            time.sleep(1)

        # Cancel the Dataflow job.
        request = dataflow.projects().jobs().update(
            projectId=PROJECT,
            jobId=job_id,
            body={'requestedState': 'JOB_STATE_CANCELLED'}
        )
        request.execute()




@pytest.mark.parametrize('dataflow_job_id',[('test_run_template_empty')], indirect=True)
def test_run_template_python_empty_args(app, dataflow_job_id):
    project = PROJECT
    template = 'gs://dataflow-templates/latest/Word_Count'
    with pytest.raises(HttpError):
        main.run(project, dataflow_job_id, template)

@pytest.mark.parametrize('dataflow_job_id',[('test_run_template_python')], indirect=True)
def test_run_template_python(app, dataflow_job_id):
    project = PROJECT
    template = 'gs://dataflow-templates/latest/Word_Count'
    parameters = {
        'inputFile': 'gs://apache-beam-samples/shakespeare/kinglear.txt',
        'output': 'gs://{}/dataflow/wordcount/outputs'.format(BUCKET),
    }
    res = main.run(project, dataflow_job_id, template, parameters)

def test_run_template_http_empty_args(app):
    with app.test_request_context():
        with pytest.raises(KeyError):
            main.run_template(flask.request)

@pytest.mark.parametrize('dataflow_job_id',[('test_run_template_url')], indirect=True)
def test_run_template_http_url(app, dataflow_job_id):
    args = {
        'project': PROJECT,
        'job': dataflow_job_id,
        'template': 'gs://dataflow-templates/latest/Word_Count',
        'inputFile': 'gs://apache-beam-samples/shakespeare/kinglear.txt',
        'output': 'gs://{}/dataflow/wordcount/outputs'.format(BUCKET),
    }
    with app.test_request_context('/?' + url_encode(args)):
        res = main.run_template(flask.request)
        data = json.loads(res)

@pytest.mark.parametrize('dataflow_job_id',[('test_run_template_data')], indirect=True)
def test_run_template_http_data(app, dataflow_job_id):
    args = {
        'project': PROJECT,
        'job': dataflow_job_id,
        'template': 'gs://dataflow-templates/latest/Word_Count',
        'inputFile': 'gs://apache-beam-samples/shakespeare/kinglear.txt',
        'output': 'gs://{}/dataflow/wordcount/outputs'.format(BUCKET),
    }
    with app.test_request_context(data=args):
        res = main.run_template(flask.request)
        data = json.loads(res)

@pytest.mark.parametrize('dataflow_job_id',[('test_run_template_json')], indirect=True)
def test_run_template_http_json(app, dataflow_job_id):
    args = {
        'project': PROJECT,
        'job': dataflow_job_id,
        'template': 'gs://dataflow-templates/latest/Word_Count',
        'inputFile': 'gs://apache-beam-samples/shakespeare/kinglear.txt',
        'output': 'gs://{}/dataflow/wordcount/outputs'.format(BUCKET),
    }
    with app.test_request_context(json=args):
        res = main.run_template(flask.request)
        data = json.loads(res)
