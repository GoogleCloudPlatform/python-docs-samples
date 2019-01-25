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
# [START iot_gateway_demo]
import csv
import datetime
import io
import logging
import os
import time

from google.cloud import pubsub

# import manager  # TODO(class) when feature exits beta, remove borrowed defs
import gateway

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.CRITICAL)

cloud_region = 'us-central1'
device_id_template = 'test-device-{}'
gateway_id_template = 'test-gateway-{}'
topic_id = 'test-device-events-{}'.format(int(time.time()))

ca_cert_path = 'resources/roots.pem'
log_path = 'config_log.csv'
rsa_cert_path = 'resources/rsa_cert.pem'
rsa_private_path = 'resources/rsa_private.pem'

if ('GCLOUD_PROJECT' not in os.environ or
        'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ):
    print(
      'You must set GCLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS')
    quit()

project_id = os.environ['GCLOUD_PROJECT']
service_account_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

pubsub_topic = 'projects/{}/topics/{}'.format(project_id, topic_id)
registry_id = 'test-registry-{}'.format(int(time.time()))

base_url = 'https://console.cloud.google.com/iot/locations/{}'.format(
        cloud_region)
edit_template = '{}/registries/{}?project={}'.format(
        base_url, '{}', '{}')

device_url_template = '{}/registries/{}/devices/{}?project={}'.format(
        base_url, '{}', '{}', '{}')

mqtt_bridge_hostname = 'mqtt.googleapis.com'
mqtt_bridge_port = 8883

num_messages = 15
jwt_exp_time = 20
listen_time = 30


def create_iot_topic(project, topic_name):
    """Creates a PubSub Topic and grants access to Cloud IoT Core."""
    pubsub_client = pubsub.PublisherClient()
    topic_path = pubsub_client.topic_path(project, topic_name)

    topic = pubsub_client.create_topic(topic_path)
    policy = pubsub_client.get_iam_policy(topic_path)

    policy.bindings.add(
        role='roles/pubsub.publisher',
        members=['serviceAccount:cloud-iot@system.gserviceaccount.com'])

    pubsub_client.set_iam_policy(topic_path, policy)

    return topic


def create_registry(
        service_account_json, project_id, cloud_region, pubsub_topic,
        registry_id):
    """ Creates a registry and returns the result. Returns an empty result if
    the registry already exists."""
    client = gateway.get_client(service_account_json)
    registry_parent = 'projects/{}/locations/{}'.format(
            project_id,
            cloud_region)
    body = {
        'eventNotificationConfigs': [{
            'pubsubTopicName': pubsub_topic
        }],
        'id': registry_id
    }
    request = client.projects().locations().registries().create(
        parent=registry_parent, body=body)

    response = request.execute()
    print('Created registry')
    return response


def delete_registry(
       service_account_json, project_id, cloud_region, registry_id):
    """Deletes the specified registry."""
    print('Delete registry')
    client = gateway.get_client(service_account_json)
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    registries = client.projects().locations().registries()
    return registries.delete(name=registry_name).execute()


def create_device(
        service_account_json, project_id, cloud_region, registry_id,
        device_id, certificate_file):
    """Create a new device without authentication."""
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    with io.open(certificate_file) as f:
        certificate = f.read()

    client = gateway.get_client(service_account_json)
    device_template = {
        'id': device_id,
        'credentials': [{
            'publicKey': {
                'format': 'RSA_X509_PEM',
                'key': certificate
            }
        }]
    }

    devices = client.projects().locations().registries().devices()
    return devices.create(parent=registry_name, body=device_template).execute()


def delete_device(
        service_account_json, project_id, cloud_region, registry_id,
        device_id):
    """Delete the device with the given id."""
    print('Delete device')
    client = gateway.get_client(service_account_json)
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    device_name = '{}/devices/{}'.format(registry_name, device_id)

    devices = client.projects().locations().registries().devices()
    return devices.delete(name=device_name).execute()


if __name__ == '__main__':
    print("Running demo")

    gateway_id = device_id_template.format('RS256')
    device_id = device_id_template.format('noauthbind')

    # [START iot_gateway_demo_create_registry]
    print('Creating registry: {}'.format(registry_id))
    create_registry(
            service_account_json, project_id, cloud_region, pubsub_topic,
            registry_id)
    # [END iot_gateway_demo_create_registry]

    # [START iot_gateway_demo_create_gateway]
    print('Creating gateway: {}'.format(gateway_id))
    gateway.create_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            None, gateway_id, rsa_cert_path, 'RS256')
    # [END iot_gateway_demo_create_gateway]

    # [START iot_gateway_demo_create_bound_device]
    print('Creating device to bind: {}'.format(device_id))
    gateway.create_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    # [END iot_gateway_demo_create_bound_device]

    # [START iot_gateway_demo_bind_device]
    print('Binding device')
    gateway.bind_device_to_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, gateway_id)
    # [END iot_gateway_demo_bind_device]

    # [START iot_gateway_demo_listen]
    print('Listening for messages for {} seconds'.format(listen_time))
    print('Try setting configuration in: ')
    print('\t{}'.format(edit_template.format(registry_id, project_id)))
    try:
        input("Press enter to continue")
    except SyntaxError:
        pass

    def log_callback(client):
        def log_on_message(unused_client, unused_userdata, message):
            if not os.path.exists(log_path):
                with open(log_path, 'w') as csvfile:
                    logwriter = csv.writer(csvfile, dialect='excel')
                    logwriter.writerow(['time', 'topic', 'data'])

            with open(log_path, 'a') as csvfile:
                logwriter = csv.writer(csvfile, dialect='excel')
                logwriter.writerow([
                        datetime.datetime.now().isoformat(),
                        message.topic,
                        message.payload])

        client.on_message = log_on_message

    gateway.listen_for_config_and_error_messages(
                service_account_json, project_id, cloud_region, registry_id,
                device_id, gateway_id, num_messages, rsa_private_path, 'RS256',
                ca_cert_path, mqtt_bridge_hostname, mqtt_bridge_port,
                jwt_exp_time, listen_time, log_callback)
    # [END iot_gateway_demo_listen]

    # [START iot_gateway_demo_publish]
    print('Publishing messages demo')
    print('Publishing: {} messages'.format(num_messages))
    gateway.send_data_from_bound_device(
                service_account_json, project_id, cloud_region, registry_id,
                device_id, gateway_id, num_messages, rsa_private_path, 'RS256',
                ca_cert_path, mqtt_bridge_hostname, mqtt_bridge_port,
                jwt_exp_time, "Hello from gateway_demo.py")

    print('You can read the state messages for your device at this URL:')
    print('\t{}'.format(device_url_template).format(
            registry_id, device_id, project_id))
    try:
        input('Press enter to continue after reading the messages.')
    except SyntaxError:
        pass
    # [END iot_gateway_demo_publish]

    # [START iot_gateway_demo_cleanup]
    # Clean up
    gateway.unbind_device_from_gateway(
            service_account_json, project_id, cloud_region, registry_id,
            device_id, gateway_id)
    delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            device_id)
    delete_device(
            service_account_json, project_id, cloud_region, registry_id,
            gateway_id)
    delete_registry(
            service_account_json, project_id, cloud_region, registry_id)
    # [END iot_gateway_demo_cleanup]

# [END iot_gateway_demo]
