#!/usr/bin/env python
#
# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

"""Script to run a Dataflow template."""


def run(project, job, template, parameters=None):
    """Runs a Dataflow template.

    Args:
        project (str): Google Cloud project ID to run on.
        job (str): Unique Dataflow job name.
        template (str): Google Cloud Storage path to Dataflow template.
        parameters (dict): Dictionary of parameters for the specified template.
    Returns:
        The response from the Dataflow service after running the template.
    """
    parameters = parameters or {}

    # [START dataflow_run_template]
    from googleapiclient.discovery import build

    # project = 'your-gcp-project'
    # job = 'unique-job-name'
    # template = 'gs://dataflow-templates/latest/Word_Count'
    # parameters = {
    #     'inputFile': 'gs://dataflow-samples/shakespeare/kinglear.txt',
    #     'output': 'gs://<your-gcs-bucket>/wordcount/outputs',
    # }

    dataflow = build('dataflow', 'v1b3')
    request = dataflow.projects().templates().launch(
        projectId=project,
        gcsPath=template,
        body={
            'jobName': job,
            'parameters': parameters,
        }
    )

    response = request.execute()
    # [END dataflow_run_template]
    return response


def run_template(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    parameters = request.get_json(silent=True) or {}  # application/json
    parameters.update(request.form.to_dict())         # Form request data
    parameters.update(request.args.to_dict())         # URL parameters

    project = parameters.pop('project')
    job = parameters.pop('job')
    template = parameters.pop('template')
    response = run(
        project=project,
        job=job,
        template=template,
        parameters=parameters,
    )
    return json.dumps(response, separators=(',', ':'))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--project', required=True,
                        help='Google Cloud project ID to run on.')
    parser.add_argument('--job', required=True,
                        help='Unique Dataflow job name.')
    parser.add_argument('--template', required=True,
                        help='Google Cloud Storage path to Dataflow template.')
    args, unknown_args = parser.parse_known_args()

    # Parse the template parameters.
    template_argparser = argparse.ArgumentParser()
    for arg in unknown_args:
        if arg.startswith('-'):
            template_argparser.add_argument(arg)
    parameters = template_argparser.parse_args(unknown_args)

    response = run(
        project=args.project,
        job=args.job,
        template=args.template,
        parameters=parameters.__dict__,
    )
    print(json.dumps(response, indent=2))
