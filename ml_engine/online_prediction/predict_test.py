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

BYTESTRING = b'\n\xdb\x02\n\x15\n\x0ccapital_gain\x12\x05\x1a\x03\n\x01\x00\n\x0c\n\x03age\x12\x05\x1a\x03\n\x01\x19\n\x16\n\teducation\x12\t\n\x07\n\x05 11th\n\x15\n\x0ccapital_loss\x12\x05\x1a\x03\n\x01\x00\n\x17\n\x0ehours_per_week\x12\x05\x1a\x03\n\x01(\n\x13\n\x06gender\x12\t\n\x07\n\x05 Male\n\x1e\n\x0crelationship\x12\x0e\n\x0c\n\n Own-child\n$\n\noccupation\x12\x16\n\x14\n\x12 Machine-op-inspct\n$\n\x0emarital_status\x12\x12\n\x10\n\x0e Never-married\n\x12\n\x04race\x12\n\n\x08\n\x06 Black\n$\n\x0enative_country\x12\x12\n\x10\n\x0e United-States\n\x16\n\reducation_num\x12\x05\x1a\x03\n\x01\x07\n\x19\n\tworkclass\x12\x0c\n\n\n\x08 Private'


def test_predict_json():
    result = predict.predict_json(
        PROJECT, MODEL, [JSON, JSON], version=JSON_VERSION)
    assert [EXPECTED_OUTPUT, EXPECTED_OUTPUT] == result


def test_predict_json_error():
    with pytest.raises(RuntimeError):
        predict.predict_json(
            PROJECT, MODEL, [{"foo": "bar"}], version=JSON_VERSION)


@pytest.mark.slow
def test_census_example_to_bytes():
    b = predict.census_to_example_bytes(JSON)
    assert base64.b64encode(b) is not None


def test_predict_examples():
    result = predict.predict_examples(
        PROJECT, MODEL, [BYTESTRING, BYTESTRING], version=EXAMPLES_VERSION)
    assert [EXPECTED_OUTPUT, EXPECTED_OUTPUT] == result
