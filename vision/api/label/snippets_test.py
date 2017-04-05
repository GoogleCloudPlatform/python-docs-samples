#!/usr/bin/env python

# Copyright 2016 Google, Inc
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
import os

import snippets

RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')


def test_crop_hint_response_count(capsys):
    snippets.crop_hint(os.path.join(RESOURCES, 'cat.jpg'))
    stdout, _ = capsys.readouterr()
    result = json.loads(stdout)
    assert len(result['responses']) == 1


def test_crop_hint_response_dim(capsys):
    snippets.crop_hint(os.path.join(RESOURCES, 'cat.jpg'))
    stdout, _ = capsys.readouterr()
    result = json.loads(stdout)
    crop_hint = result['responses'][0]
    crop_hint_annotation = crop_hint['cropHintsAnnotation']['cropHints'][0]
    confidence = crop_hint_annotation['confidence']

    assert 0.5 < confidence < 0.9


def test_web_annotations(capsys):
    snippets.web_annotation(os.path.join(RESOURCES, 'cat.jpg'))
    stdout, _ = capsys.readouterr()
    result = json.loads(stdout)
    web_annotation = result['responses'][0]['webDetection']
    web_entities = web_annotation['webEntities']

    assert len(web_entities)
