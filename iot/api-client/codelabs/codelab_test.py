# Copyright 2019 Google Inc. All Rights Reserved.
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
from colors import bcolors
import gateway
import ledlight
import lightsensor
import thermostat


# Check colors exist
def test_check_colors(capsys):
    assert bcolors.OKBLUE is not None
    assert bcolors.FAIL is not None
    assert bcolors.CEND is not None


# Check error code returns reasonable justifications
def test_gateway_error_string(capsys):
    print(gateway.error_str(1))
    print(gateway.error_str(2))
    print(gateway.error_str(3))
    print(gateway.error_str(4))
    out, _ = capsys.readouterr()

    assert 'memory' in out
    assert 'network' in out
    assert 'function arguments' in out
    assert 'currently connected' in out


# Check gateway state is init to reasonable defaults
def test_gateway_state(capsys):
    assert (gateway.GatewayState.mqtt_config_topic == '')
    assert (gateway.GatewayState.connected is False)
    assert (gateway.GatewayState.pending_responses == {})
    assert (gateway.GatewayState.pending_subscribes == {})
    assert (gateway.GatewayState.mqtt_bridge_port == 8883 or
            gateway.GatewayState.mqtt_bridge_ == 443)


def test_check_ledlight(capsys):
    print(ledlight.make_message('test', 'action', data='1234'))
    out, _ = capsys.readouterr()

    assert ('{ "device" : "test"' in out)


def test_check_lightsensor(capsys):
    print(lightsensor.print_sensor_state())
    out, _ = capsys.readouterr()

    assert ('Sensor is on, reporting lux every 1 seconds.' in out)


def test_check_thermostat(capsys):
    print(thermostat.make_message('test', 'action', data='1234'))
    out, _ = capsys.readouterr()

    assert ('{ "device" : "test"' in out)
