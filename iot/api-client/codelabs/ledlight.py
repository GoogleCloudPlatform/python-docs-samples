# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import socket
import sys

from colors import bcolors

ADDR = ''
PORT = 10000
BUFF_SIZE = 4096
device_id = None
server_address = (ADDR, PORT)
# Create a UDP socket
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_command(sock, message):
    sock.sendto(message.encode(), server_address)

    # Receive response
    print('Waiting for response.....')
    response = sock.recv(BUFF_SIZE)

    return response


def make_message(device_id, action, data=''):
    if data:
        return '{{ "device" : "{}", "action":"{}", "data" : "{}" }}'.format(
            device_id, action, data)
    else:
        return f'{{ "device" : "{device_id}", "action":"{action}" }}'


def run_action(device_id, action, data=''):
    message = make_message(device_id, action, data)
    if not message:
        return
    print(f'Send message: {message}')

    event_response = send_command(client_sock, message).decode('utf-8')
    print(f'Received response: {event_response}')


def main():
    device_id = sys.argv[1]
    if not device_id:
        sys.exit('The device id must be specified.')

    print(f'Bringing up device {device_id}')
    try:
        run_action(device_id, 'detach')
        run_action(device_id, 'attach')
        run_action(device_id, 'event', 'LED is online')
        run_action(device_id, 'subscribe')

        while True:
            response = client_sock.recv(BUFF_SIZE)
            message = response.decode('utf-8')
            if message.find("ON") != -1:
                sys.stdout.write(
                    '\r>> ' + bcolors.CGREEN + bcolors.CBLINK +
                    " LED is ON " + bcolors.ENDC + ' <<')
                sys.stdout.flush()
            elif message.find("OFF") != -1:
                sys.stdout.write(
                    '\r >>' + bcolors.CRED + bcolors.BOLD +
                    " LED is OFF " + bcolors.ENDC + ' <<')
                sys.stdout.flush()

    finally:
        print('closing socket')
        client_sock.close()


if __name__ == '__main__':
    main()
