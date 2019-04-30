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

from datetime import date

import my_models


def create_entity():
    # Create an entity and write it to the Datastore.
    entity = my_models.MyModel(name='booh', xyz=[10**100, 6**666])
    assert entity.abc == 0
    key = entity.put()
    return key


def read_and_update_entity(key):
    # Read an entity back from the Datastore and update it.
    entity = key.get()
    entity.abc += 1
    entity.xyz.append(entity.abc//3)
    entity.put()


def query_entity():
    # Query for a MyModel entity whose xyz contains 6**666.
    # (NOTE: using ordering operations don't work, but == does.)
    results = my_models.MyModel.query(
        my_models.MyModel.xyz == 6**666).fetch(10)
    return results


def create_and_query_columbus():
    columbus = my_models.HistoricPerson(
        name='Christopher Columbus',
        birth=my_models.FuzzyDate(date(1451, 8, 22), date(1451, 10, 31)),
        death=my_models.FuzzyDate(date(1506, 5, 20)),
        event_dates=[my_models.FuzzyDate(
            date(1492, 1, 1), date(1492, 12, 31))],
        event_names=['Discovery of America'])
    columbus.put()

    # Query for historic people born no later than 1451.
    results = my_models.HistoricPerson.query(
        my_models.HistoricPerson.birth.last <= date(1451, 12, 31)).fetch()
    return results
