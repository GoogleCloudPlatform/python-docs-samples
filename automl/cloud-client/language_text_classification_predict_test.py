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

import language_text_classification_predict

PROJECT_ID = os.environ['GCLOUD_PROJECT']
MODEL_ID = 'TCN3472481026502981088'


def test_predict(capsys):
    text = 'Fruit and nut flavour'
    language_text_classification_predict.predict(PROJECT_ID, MODEL_ID, text)
    out, _ = capsys.readouterr()
    assert 'Predicted class name: ' in out
