# Copyright 2016 Google Inc. All rights reserved.
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

import datetime

from google.appengine.ext import ndb
import pytest

import my_models
import snippets


def test_create_entity(testbed):
    assert my_models.MyModel.query().count() == 0
    snippets.create_entity()
    entities = my_models.MyModel.query().fetch()
    assert len(entities) == 1
    assert entities[0].name == 'booh'


def test_read_and_update_entity(testbed):
    key = snippets.create_entity()
    entities = my_models.MyModel.query().fetch()
    assert len(entities) == 1
    assert entities[0].abc == 0
    len_xyz = len(entities[0].xyz)

    snippets.read_and_update_entity(key)
    entities = my_models.MyModel.query().fetch()
    assert len(entities) == 1
    assert entities[0].abc == 1
    assert len(entities[0].xyz) == len_xyz + 1


def test_query_entity(testbed):
    results = snippets.query_entity()
    assert len(results) == 0

    snippets.create_entity()
    results = snippets.query_entity()
    assert len(results) == 1


def test_create_columbus(testbed):
    entities = snippets.create_and_query_columbus()
    assert len(entities) == 1
    assert entities[0].name == 'Christopher Columbus'
    assert (entities[0].birth.first < entities[0].birth.last <
            entities[0].death.first)


def test_long_integer_property(testbed):
    with pytest.raises(TypeError):
        my_models.MyModel(
            name='not integer test',
            xyz=['not integer'])


def test_bounded_long_integer_property(testbed):
    class TestBoundedLongIntegerProperty(ndb.Model):
        num = my_models.BoundedLongIntegerProperty(4)

    # Test out of the bounds
    with pytest.raises(AssertionError):
        TestBoundedLongIntegerProperty(num=0xF)
    with pytest.raises(AssertionError):
        TestBoundedLongIntegerProperty(num=-0xF)

    # This should work
    working_instance = TestBoundedLongIntegerProperty(num=0b111)
    assert working_instance.num == 0b111
    working_instance.num = 0b10
    assert working_instance.num == 2


def test_maybe_fuzzy_date_property(testbed):
    class TestMaybeFuzzyDateProperty(ndb.Model):
        first_date = my_models.MaybeFuzzyDateProperty()
        second_date = my_models.MaybeFuzzyDateProperty()

    two_types_of_dates = TestMaybeFuzzyDateProperty(
        first_date=my_models.FuzzyDate(
            datetime.date(1984, 2, 27), datetime.date(1984, 2, 29)),
        second_date=datetime.date(2015, 6, 27))

    assert isinstance(two_types_of_dates.first_date, my_models.FuzzyDate)
    assert isinstance(two_types_of_dates.second_date, my_models.FuzzyDate)
