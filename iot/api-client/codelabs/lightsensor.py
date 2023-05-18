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

import errno
import json
import random
import socket
import sys
import time

from colors import bcolors

# Constants
ADDR = ''
PORT = 10000
BUFF_SIZE = 4096
SERVER_ADDRESS = (ADDR, PORT)


class LightSensor:
    # controls reporting of the sensor, can be {'on', 'off'}
    power = 'on'

    # represents interval in seconds for reporting sensor data
    interval = 1

    # lux being simulated by the virtual device
    lux = 350


def send_command(sock, message, should_wait):
    """Sends a command to the gateway.
      Args:
         sock: Socket to send the message.
         message: Bytes object that contains the command.
         should_wait: Boolean that determines if we should wait for a response
                      from the socket.
    """
    sock.sendto(message, SERVER_ADDRESS)

    # conditionally wait on the response from the gateway
    if should_wait:
        response = sock.recv(BUFF_SIZE)
        print('Response: {}'.format(response.decode("utf-8")))


def make_message(device_id, action, data=''):
    """Returns a formatted string based on actions"""
    if data:
        return '{{ "device" : "{}", "action":"{}", "data" : "{}" }}'.format(
                device_id, action, data)
    else:
        return f'{{ "device" : "{device_id}", "action":"{action}" }}'


def run_action(sock, device_id, action, data=''):
    """ Creates proper message format and sends a command to the gateway
    (blocking)."""
    message = make_message(device_id, action, data)
    if not message:
        return
    print(f'Send message: {message}')
    send_command(sock, message.encode(), True)


def detect_light(device_id, sock):
    """Simulates reading data from a virtual light sensor and reports data to
    gateway."""

    # Simulate minor light changes in an environment.
    LightSensor.lux += random.uniform(-10, 10)

    lux = f"{LightSensor.lux:.3f}"

    sys.stdout.write(
            '\r>> ' + bcolors.CGREEN + bcolors.CBOLD + f'Lux: {lux}' +
            bcolors.ENDC + ' <<')
    sys.stdout.flush()

    message = make_message(device_id, 'event', f'lux={lux}').encode()

    send_command(sock, message, False)
    time.sleep(LightSensor.interval)


def print_sensor_state():
    if LightSensor.power == 'on':
        print(
            '\nSensor is {}, reporting lux every {} seconds.'.format(
                LightSensor.power, LightSensor.interval))
    else:
        print(
            '\nSensor is {}. Send a configuration update to turn on'.format(
                LightSensor.power))


def process_message(message):
    """Parse messages received from the gateway socket."""

    # If status exists in the message, it is an ack from the gateway and can be
    # ignored.
    if 'status' in message:
        return

    # Turns the power of the light sensor on/off
    if 'power' in message:
        state = message['power'].lower()
        if state == 'on' or state == 'off':
            LightSensor.power = state
        else:
            print('Invalid value for key "power". Specify "on" or "off."')

    if 'interval' in message:
        if isinstance(message['interval'], int):
            LightSensor.interval = message['interval']
        else:
            print('Invalid value for key "interval". Specify an int > 0.')

    print_sensor_state()


def main():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    random.seed()

    device_id = sys.argv[1]
    if not device_id:
        sys.exit('The device id must be specified.')

    print(f'Bringing up device {device_id}')

    try:
        run_action(sock, device_id, 'detach')
        run_action(sock, device_id, 'attach')
        run_action(sock, device_id, 'event', 'Light sensor is on')
        run_action(sock, device_id, 'subscribe')

        # Wait a bit for subscribe message to complete before continuing.
        time.sleep(3)

        # Set socket blocking to false so we can handle incoming/outgoing
        # messages asynchronously.
        sock.setblocking(False)

        while True:
            # Try to read message from the socket.
            try:
                data = sock.recv(BUFF_SIZE)
            except OSError as e:
                err = e.args[0]

                # If there is no data from the socket, just report the lux
                # readings
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    # If the light sensor is off, wait a bit before checking
                    # again.
                    if LightSensor.power.lower() == 'off':
                        time.sleep(3)
                        continue

                    detect_light(device_id, sock)
                else:
                    print(e)
                    sys.exit(1)
            else:
                # Received data from the socket, so process the message.
                decode = data.decode("utf-8")
                if decode != '':
                    message = json.loads(decode)
                    if not message:
                        print('invalid json: {}'.format(data.decode("utf-8")))
                        continue
                    process_message(message)
    finally:
        print('Closing socket')
        sock.close()


if __name__ == "__main__":
    main()
