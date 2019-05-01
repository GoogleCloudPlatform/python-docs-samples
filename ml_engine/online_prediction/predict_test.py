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

import json
import socket

from gcp_devrel.testing.flaky import flaky
import pytest

import predict

MODEL = 'census'
JSON_VERSION = 'v1json'
EXAMPLES_VERSION = 'v1example'
PROJECT = 'python-docs-samples-tests'
EXPECTED_OUTPUT = {
    u'confidence': 0.7760371565818787,
    u'predictions': u' <=50K'
}

# Raise the socket timeout. The requests involved in the sample can take
# a long time to complete.
socket.setdefaulttimeout(60)


with open('resources/census_test_data.json') as f:
    JSON = json.load(f)


with open('resources/census_example_bytes.pb', 'rb') as f:
    BYTESTRING = f.read()


@flaky
def test_predict_json():
    result = predict.predict_json(
        PROJECT, MODEL, [JSON, JSON], version=JSON_VERSION)
    assert [EXPECTED_OUTPUT, EXPECTED_OUTPUT] == result


@flaky
def test_predict_json_error():
    with pytest.raises(RuntimeError):
        predict.predict_json(
            PROJECT, MODEL, [{"foo": "bar"}], version=JSON_VERSION)


@flaky
def test_census_example_to_bytes():
    import tensorflow as tf
    b = predict.census_to_example_bytes(JSON)
    assert tf.train.Example.FromString(b) == tf.train.Example.FromString(
        BYTESTRING)


@flaky(max_runs=6)
def test_predict_examples():
    result = predict.predict_examples(
        PROJECT, MODEL, [BYTESTRING, BYTESTRING], version=EXAMPLES_VERSION)
    assert [EXPECTED_OUTPUT, EXPECTED_OUTPUT] == result
