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

import socket
import subprocess

import pytest
import requests
from retrying import retry
import websocket


@pytest.fixture(scope='module')
def server():
    """Provides the address of a test HTTP/websocket server.
    The test server is automatically created before
    a test and destroyed at the end.
    """
    # Ask the OS to allocate a port.
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]

    # Free the port and pass it to a subprocess.
    sock.close()

    bind_to = f'127.0.0.1:{port}'
    server = subprocess.Popen(
        ['gunicorn', '-b', bind_to, '-k' 'flask_sockets.worker', 'main:app'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # With btlr, there can be many processes are spawned and the
    # server might be in a tight memory situation, so let's wait for 2
    # mins.
    # Wait until the server responds before proceeding.
    @retry(wait_fixed=50, stop_max_delay=120000)
    def check_server(url):
        requests.get(url)

    check_server(f'http://{bind_to}/')

    yield bind_to

    server.kill()

    # Dump the logs for debugging
    out, err = server.communicate()
    print(f"gunicorn stdout: {out}")
    print(f"gunicorn stderr: {err}")


def test_http(server):
    result = requests.get(f'http://{server}/')
    assert 'Python Websockets Chat' in result.text


def test_websocket(server):
    url = f'ws://{server}/chat'
    ws_one = websocket.WebSocket()
    ws_one.connect(url)

    ws_two = websocket.WebSocket()
    ws_two.connect(url)

    message = 'Hello, World'
    ws_one.send(message)

    assert ws_one.recv() == message
    assert ws_two.recv() == message
