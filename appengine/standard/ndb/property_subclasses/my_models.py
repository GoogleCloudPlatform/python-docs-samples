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

from google.appengine.ext import ndb


class LongIntegerProperty(ndb.StringProperty):
    def _validate(self, value):
        if not isinstance(value, (int, long)):
            raise TypeError('expected an integer, got %s' % repr(value))

    def _to_base_type(self, value):
        return str(value)  # Doesn't matter if it's an int or a long

    def _from_base_type(self, value):
        return long(value)  # Always return a long


class BoundedLongIntegerProperty(ndb.StringProperty):
    def __init__(self, bits, **kwds):
        assert isinstance(bits, int)
        assert bits > 0 and bits % 4 == 0  # Make it simple to use hex
        super(BoundedLongIntegerProperty, self).__init__(**kwds)
        self._bits = bits

    def _validate(self, value):
        assert -(2 ** (self._bits - 1)) <= value < 2 ** (self._bits - 1)

    def _to_base_type(self, value):
        # convert from signed -> unsigned
        if value < 0:
            value += 2 ** self._bits
        assert 0 <= value < 2 ** self._bits
        # Return number as a zero-padded hex string with correct number of
        # digits:
        return '%0*x' % (self._bits // 4, value)

    def _from_base_type(self, value):
        value = int(value, 16)
        if value >= 2 ** (self._bits - 1):
            value -= 2 ** self._bits
        return value


# Define an entity class holding some long integers.
class MyModel(ndb.Model):
    name = ndb.StringProperty()
    abc = LongIntegerProperty(default=0)
    xyz = LongIntegerProperty(repeated=True)


class FuzzyDate(object):
    def __init__(self, first, last=None):
        assert isinstance(first, date)
        assert last is None or isinstance(last, date)
        self.first = first
        self.last = last or first


class FuzzyDateModel(ndb.Model):
    first = ndb.DateProperty()
    last = ndb.DateProperty()


class FuzzyDateProperty(ndb.StructuredProperty):
    def __init__(self, **kwds):
        super(FuzzyDateProperty, self).__init__(FuzzyDateModel, **kwds)

    def _validate(self, value):
        assert isinstance(value, FuzzyDate)

    def _to_base_type(self, value):
        return FuzzyDateModel(first=value.first, last=value.last)

    def _from_base_type(self, value):
        return FuzzyDate(value.first, value.last)


class MaybeFuzzyDateProperty(FuzzyDateProperty):
    def _validate(self, value):
        if isinstance(value, date):
            return FuzzyDate(value)  # Must return the converted value!
        # Otherwise, return None and leave validation to the base class


# Class to record historic people and events in their life.
class HistoricPerson(ndb.Model):
    name = ndb.StringProperty()
    birth = FuzzyDateProperty()
    death = FuzzyDateProperty()
    # Parallel lists:
    event_dates = FuzzyDateProperty(repeated=True)
    event_names = ndb.StringProperty(repeated=True)
