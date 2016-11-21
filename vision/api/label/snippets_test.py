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


import snippets


def test_crop_hint_response_count(resource):
    result = snippets.crop_hint(resource('cat.jpg'))
    assert len(result['responses']) == 1


def test_crop_hint_response_dim(resource):
    result = snippets.crop_hint(resource('cat.jpg'))
    crop_hint = result['responses'][0]
    crop_hint_annotation = crop_hint['cropHintsAnnotation']['cropHints'][0]
    confidence = crop_hint_annotation['confidence']

    assert 0.5 < confidence < 0.9


def test_web_annotations(resource):
    result = snippets.web_annotation(resource('cat.jpg'))
    web_annotation = result['responses'][0]['webAnnotation']
    web_entities = web_annotation['webEntities']

    assert len(web_entities) == 10
    assert web_entities[0]['entityId'] == '/m/012cc2'
    assert web_entities[0]['description'] == 'Russian Blue'
