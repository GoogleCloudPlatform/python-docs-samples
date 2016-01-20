# Copyright 2015 Google Inc. All Rights Reserved.
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

import logging
import multiprocessing
import os
import sys
import time
import unittest

import requests
from werkzeug.serving import run_simple


logging.getLogger("requests").setLevel(logging.WARNING)


def run_app(path, port, entrypoint):
    path = os.path.realpath(path)
    sys.path.insert(1, path)
    os.chdir(path)

    module_name, wsgi_app_name = entrypoint.rsplit('.', 1)

    module = __import__(module_name)
    wsgi_app = getattr(module, wsgi_app_name)

    wsgi_app.debug = True
    run_simple('localhost', port, wsgi_app, use_debugger=True)


def run_app_multiprocessing(path, port=43125, entrypoint='main.app'):
    process = multiprocessing.Process(
        target=run_app, args=(path, port, entrypoint))
    process.start()

    try:
        _wait_for_server(port)
    except:
        process.terminate()
        raise

    return process


def _wait_for_server(port):
    start = time.time()
    while True:
        try:
            requests.get('http://localhost:{}/_ah/health'.format(port))
            # Break on first successful request, regardless of status, as it
            # means the server is accepting connections.
            break
        except requests.ConnectionError:
            if time.time() - start > 5:
                raise RuntimeError('Server failed to respond to requests.')


class RunServerTestCase(unittest.TestCase):
    server_host = 'locahost'
    server_port = 43125
    server_url = 'http://localhost:43125/'

    application_path = None
    application_entrypoint = 'main.app'
    _server_process = None

    @classmethod
    def setUpClass(cls):
        cls._server_process = run_app_multiprocessing(
            cls.application_path,
            entrypoint=cls.application_entrypoint)

    @classmethod
    def tearDownClass(cls):
        if cls._server_process:
            cls._server_process.terminate()
