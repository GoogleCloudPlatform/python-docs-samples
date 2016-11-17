# Copyright 2016 Google Inc. All Rights Reserved.
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

from contextlib import contextmanager

from grpc.beta import interfaces


Code = interfaces.StatusCode


class StatusException(Exception):
  """An exception thrown to indicate failed GRPC call."""

  def __init__(self, code, details):
    self._code = code
    self._details = details

  def fill(self, context):
    """Fills in a GRPC server-side context with exception info."""
    context.code(self._code)
    context.details(self._details)


@contextmanager
def context(grpc_context):
  """A context manager that automatically handles StatusException."""
  try:
    yield
  except StatusException as exc:
    exc.fill(grpc_context)
