# Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Common testing utilities between samples
"""

import contextlib
import logging
import sys

import httplib2
from six.moves import cStringIO


def silence_requests():
    """Silence requests' noisy logging."""
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urrlib3").setLevel(logging.WARNING)


@contextlib.contextmanager
def capture_stdout():
    """Capture stdout to a StringIO object."""
    fake_stdout = cStringIO()
    old_stdout = sys.stdout

    try:
        sys.stdout = fake_stdout
        yield fake_stdout
    finally:
        sys.stdout = old_stdout


class Http2Mock(object):
    """Mock httplib2.Http"""

    def __init__(self, responses):
        self.responses = responses

    def add_credentials(self, user, pwd):
        self.credentials = (user, pwd)

    def request(self, token_uri, method, body, headers=None, *args, **kwargs):
        response = self.responses.pop(0)
        self.status = response.get('status', 200)
        self.body = response.get('body', '')
        self.headers = response.get('headers', '')
        return (self, self.body)

    def __enter__(self):
        self.httplib2_orig = httplib2.Http
        httplib2.Http = self
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        httplib2.Http = self.httplib2_orig

    def __call__(self, *args, **kwargs):
        return self
