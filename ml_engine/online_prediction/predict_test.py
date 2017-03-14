# Copyright 2017 Google Inc. All Rights Reserved.
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

"""Tests for predict.py ."""

import base64

import pytest

import predict


MODEL = 'census'
JSON_VERSION = 'v1json'
EXAMPLES_VERSION = 'v1example'
PROJECT = 'python-docs-samples-tests'
JSON = {
    'age': 25,
    'workclass': ' Private',
    'education': ' 11th',
    'education_num': 7,
    'marital_status': ' Never-married',
    'occupation': ' Machine-op-inspct',
    'relationship': ' Own-child',
    'race': ' Black',
    'gender': ' Male',
    'capital_gain': 0,
    'capital_loss': 0,
    'hours_per_week': 40,
    'native_country': ' United-States'
}
EXPECTED_OUTPUT = {
    u'confidence': 0.7760371565818787,
    u'predictions': u' <=50K'
}


def test_predict_json():
    result = predict.predict_json(
        PROJECT, MODEL, [JSON, JSON], version=JSON_VERSION)
    assert [EXPECTED_OUTPUT, EXPECTED_OUTPUT] == result


def test_predict_json_error():
    with pytest.raises(RuntimeError):
        predict.predict_json(PROJECT, MODEL, [{"foo": "bar"}], version=JSON_VERSION)


@pytest.mark.slow
def test_census_example_to_bytes():
    b = predict.census_to_example_bytes(JSON)
    assert base64.b64encode(b) is not None


@pytest.mark.slow
def test_predict_examples():
    b = predict.census_to_example_bytes(JSON)
    result = predict.predict_examples(
        PROJECT, MODEL, [b, b], version=EXAMPLES_VERSION)
    assert [EXPECTED_OUTPUT, EXPECTED_OUTPUT] == result
