#!/usr/bin/env python

# Copyright 2018 Google LLC
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

import os

import pytest

import list_models
import get_model
import list_model_evaluations
import get_model_evaluation
import list_operation_status
import get_operation_status
import create_model
import delete_model

project_id = os.environ['GCLOUD_PROJECT']
dataset_id = 'TRL3876092572857648864'


@pytest.mark.slow
def test_list_get_eval_model(capsys):
    list_models.list_models(project_id)
    out, _ = capsys.readouterr()
    model_id = out.split('Model id: ')[1].split('\n')[0]
    assert 'Model id: ' in out

    get_model.get_model(project_id, model_id)
    out, _ = capsys.readouterr()
    assert 'Model id: ' in out

    list_model_evaluations.list_model_evaluations(project_id, model_id)
    out, _ = capsys.readouterr()
    model_evaluation_id = \
        out.split('{}/modelEvaluations/'.format(model_id))[1].split('\n')[0]
    assert 'Model evaluation name: ' in out

    get_model_evaluation.get_model_evaluation(
        project_id, model_id, model_evaluation_id)
    out, _ = capsys.readouterr()
    assert 'Model evaluation name: ' in out


@pytest.mark.slow
def test_list_get_operation_status(capsys):
    list_operation_status.list_operation_status(project_id)
    out, _ = capsys.readouterr()
    operation_id = out.split('Name: ')[1].split('\n')[0]
    assert 'Operation details' in out

    get_operation_status.get_operation_status(operation_id)
    out, _ = capsys.readouterr()
    assert 'Operation details' in out


@pytest.mark.slow
def test_create_model(capsys):
    create_model.create_model(
        project_id, dataset_id, 'translation_test_create_model')
    out, _ = capsys.readouterr()
    assert 'Training started' in out

    operation_id = out.split('Training operation name: ')[1].split('\n')[0]
    from google.cloud import automl
    client = automl.AutoMlClient()
    client.transport._operations_client.cancel_operation(operation_id)


@pytest.mark.slow
def test_delete_model(capsys):
    # As model creation can take many hours, instead try to delete a
    # nonexistent model and confirm that the model was not found, but other
    # elements of the request were valid.
    delete_model.delete_model(project_id, 'TRL0000000000000000000')
    out, _ = capsys.readouterr()
    assert 'status = StatusCode.NOT_FOUND' in out
    assert 'details = "The model does not exist."' in out
