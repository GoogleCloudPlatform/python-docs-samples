# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Wrappers for protocol buffer enum types."""


class NullValue(object):
    """
    ``NullValue`` is a singleton enumeration to represent the null value for the
    ``Value`` type union.

     The JSON representation for ``NullValue`` is JSON ``null``.

    Attributes:
      NULL_VALUE (int): Null value.
    """
    NULL_VALUE = 0


class Asset(object):
    class State(object):
        """
        State of the asset.

        When querying across two points in time this describes
        the change between the two points: NOT_FOUND, ADDED, REMOVED, or
        ACTIVE_AT_BOTH.

        When querying for a single point in time this describes the
        state at that time: NOT_FOUND, ACTIVE, REMOVED.

        Attributes:
          STATE_UNSPECIFIED (int): Invalid state.
          ACTIVE (int): Asset was active for the point in time.
          NOT_FOUND (int): Asset was not found for the point(s) in time.
          ADDED (int): Asset was added between the points in time.
          REMOVED (int): Asset was removed between the points in time.
          ACTIVE_AT_BOTH (int): Asset was active at both point(s) in time.
        """
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        NOT_FOUND = 2
        ADDED = 3
        REMOVED = 4
        ACTIVE_AT_BOTH = 5
