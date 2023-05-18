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

import random
import socket
import sys
import time

from colors import bcolors

ADDR = ''
PORT = 10000
# Create a UDP socket
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (ADDR, PORT)

device_id = sys.argv[1]
if not device_id:
    sys.exit('The device id must be specified.')

print(f'Bringing up device {device_id}')


# return message received
def send_command(sock, message, log=True):
    sock.sendto(message, server_address)

    # Receive response
    response, _ = sock.recvfrom(4096)
    return response


def make_message(device_id, action, data=''):
    if data:
        return '{{ "device" : "{}", "action":"{}", "data" : "{}" }}'.format(
                device_id, action, data)
    else:
        return f'{{ "device" : "{device_id}", "action":"{action}" }}'


def run_action(action):
    message = make_message(device_id, action)
    if not message:
        return
    print(f'Sending data: {message}')
    event_response = send_command(client_sock, message.encode())
    print('Response {}'.format(event_response.decode("utf-8")))


def main():
    try:
        random.seed()
        run_action('detach')
        run_action('attach')

        h = 35.0
        t = 20.0

        while True:
            h += random.uniform(-1, 1)
            t += random.uniform(-1, 1)

            temperature_f = t * 9.0/5 + 32

            humidity = f"{h:.3f}"
            temperature = f"{temperature_f:.3f}"
            sys.stdout.write(
                '\r>> ' + bcolors.CGREEN + bcolors.CBOLD +
                f'Temp: {temperature} F, Hum: {humidity}%' +
                bcolors.ENDC + ' <<')
            sys.stdout.flush()

            message = make_message(
                device_id, 'event', f'temperature={t}, humidity={h}'
                ).encode()

            send_command(client_sock, message, False)
            time.sleep(2)
    finally:
        print('Closing socket')
        client_sock.close()


if __name__ == "__main__":
    main()
