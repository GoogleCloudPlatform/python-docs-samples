#!/usr/bin/env python

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def list_model_evaluations(project_id, model_id):
    """List model evaluations."""
    # [START automl_list_model_evaluations]
    from google.cloud import automl

    # TODO(developer): Uncomment and set the following variables
    # project_id = 'YOUR_PROJECT_ID'
    # model_id = 'YOUR_MODEL_ID'

    client = automl.AutoMlClient()
    # Get the full path of the model.
    model_full_id = client.model_path(project_id, 'us-central1', model_id)

    print('List of model evaluations:')
    for evaluation in client.list_model_evaluations(model_full_id, ''):
        print(u'Model evaluation name: {}'.format(evaluation.name))
        print(
            u'Model annotation spec id: {}'.format(
                evaluation.annotation_spec_id))
        print(u'Create Time:')
        print(u'\tseconds: {}'.format(evaluation.create_time.seconds))
        print(u'\tnanos: {}'.format(evaluation.create_time.nanos / 1e9))
        print(u'Evaluation example count: {}'.format(
            evaluation.evaluated_example_count))
        print(u'Model evaluation metrics: {}'.format(
            evaluation.translation_evaluation_metrics))
    # [END automl_list_model_evaluations]
