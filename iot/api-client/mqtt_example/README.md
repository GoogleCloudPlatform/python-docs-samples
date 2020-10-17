Google Cloud IoT Core Python Samples
====================================

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=iot/api-client/mqtt_example/README.rst)

This directory contains samples for Google Cloud IoT Core. [Google Cloud
IoT Core](https://cloud.google.com/iot/docs) allows developers to easily
integrate Publish and Subscribe functionality with devices and
programmatically manage device authorization. Before you run the sample,
you must retrieve the Google root certificate. For example,
`wget https://pki.goog/roots.pem` or
`curl https://pki.goog/roots.pem > roots.pem`. The following example
runs the sample using the project ID `blue-jet-123` and the device name
`my-python-device`:

    python cloudiot_mqtt_example.py \
        --registry_id=my-registry \
        --cloud_region=us-central1 \
        --project_id=blue-jet-123 \
        --device_id=my-python-device \
        --algorithm=RS256 \
        --private_key_file=../rsa_private.pem

Setup
-----

### Install Dependencies

1.  Clone python-docs-samples and change directory to the sample
    directory you want to use.

    > ``` {.bash}
    > $ git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
    > ```

2.  Install [pip](https://pip.pypa.io/) and
    [virtualenv](https://virtualenv.pypa.io/) if you do not already have
    them. You may want to refer to the [Python Development Environment
    Setup Guide]() for Google Cloud Platform for instructions.

    ::: {#Python Development Environment Setup Guide}
    > <https://cloud.google.com/python/setup>
    :::

3.  Create a virtualenv. Samples are compatible with Python 2.7 and
    3.4+.

    > ``` {.bash}
    > $ virtualenv env
    > $ source env/bin/activate
    > ```

4.  Install the dependencies needed to run the samples.

    > ``` {.bash}
    > $ pip install -r requirements.txt
    > ```

Samples
-------

### MQTT Device Client Example

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=iot/api-client/mqtt_example/cloudiot_mqtt_example.py,iot/api-client/mqtt_example/README.rst)

To run this sample:

``` {.bash}
$ python cloudiot_mqtt_example.py

usage: cloudiot_mqtt_example.py [-h] --algorithm {RS256,ES256}
                                [--ca_certs CA_CERTS]
                                [--cloud_region CLOUD_REGION] [--data DATA]
                                --device_id DEVICE_ID
                                [--gateway_id GATEWAY_ID]
                                [--jwt_expires_minutes JWT_EXPIRES_MINUTES]
                                [--listen_dur LISTEN_DUR]
                                [--message_type {event,state}]
                                [--mqtt_bridge_hostname MQTT_BRIDGE_HOSTNAME]
                                [--mqtt_bridge_port {8883,443}]
                                [--num_messages NUM_MESSAGES]
                                --private_key_file PRIVATE_KEY_FILE
                                [--project_id PROJECT_ID] --registry_id
                                REGISTRY_ID
                                [--service_account_json SERVICE_ACCOUNT_JSON]
                                {device_demo,gateway_send,gateway_listen} ...

Example Google Cloud IoT Core MQTT device connection code.

positional arguments:
  {device_demo,gateway_send,gateway_listen}
    device_demo         Connects a device, sends data, and receives data.
    gateway_send        Sends data from a gateway on behalf of a device that
                        is bound to it.
    gateway_listen      Listens for messages sent to the gateway and bound
                        devices.

optional arguments:
  -h, --help            show this help message and exit
  --algorithm {RS256,ES256}
                        Which encryption algorithm to use to generate the JWT.
  --ca_certs CA_CERTS   CA root from https://pki.google.com/roots.pem
  --cloud_region CLOUD_REGION
                        GCP cloud region

  --data DATA           The telemetry data sent on behalf of a device
  --device_id DEVICE_ID
                        Cloud IoT Core device id
  --gateway_id GATEWAY_ID
                        Gateway identifier.
  --jwt_expires_minutes JWT_EXPIRES_MINUTES
                        Expiration time, in minutes, for JWT tokens.
  --listen_dur LISTEN_DUR
                        Duration (seconds) to listen for configuration
                        messages
  --message_type {event,state}
                        Indicates whether the message to be published is a
                        telemetry event or a device state message.
  --mqtt_bridge_hostname MQTT_BRIDGE_HOSTNAME
                        MQTT bridge hostname.
  --mqtt_bridge_port {8883,443}
                        MQTT bridge port.
  --num_messages NUM_MESSAGES
                        Number of messages to publish.
  --private_key_file PRIVATE_KEY_FILE
                        Path to private key file.
  --project_id PROJECT_ID
                        GCP cloud project name
  --registry_id REGISTRY_ID
                        Cloud IoT Core registry id
  --service_account_json SERVICE_ACCOUNT_JSON
                        Path to service account json file.
```

### MQTT Image Example

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=iot/api-client/mqtt_example/cloudiot_mqtt_image.py,iot/api-client/mqtt_example/README.rst)

To run this sample:

``` {.bash}
$ python cloudiot_mqtt_image.py

usage: cloudiot_mqtt_image.py [-h] [--ca_certs CA_CERTS]
                              [--cloud_region CLOUD_REGION]
                              [--image_path IMAGE_PATH] --device_id DEVICE_ID
                              --private_key_file PRIVATE_KEY_FILE
                              [--project_id PROJECT_ID] --registry_id
                              REGISTRY_ID
                              [--service_account_json SERVICE_ACCOUNT_JSON]
                              {send} ...

Google Cloud IoT Core MQTT binary transmission demo.

positional arguments:
  {send}
    send                Send an image to a device registry

optional arguments:
  -h, --help            show this help message and exit
  --ca_certs CA_CERTS   CA root from https://pki.google.com/roots.pem
  --cloud_region CLOUD_REGION
                        GCP cloud region
  --image_path IMAGE_PATH
                        The telemetry data sent on behalf of a device
  --device_id DEVICE_ID
                        Cloud IoT Core device id
  --private_key_file PRIVATE_KEY_FILE
                        Path to private key file.
  --project_id PROJECT_ID
                        GCP cloud project name
  --registry_id REGISTRY_ID
                        Cloud IoT Core registry id
  --service_account_json SERVICE_ACCOUNT_JSON
                        Path to service account json file.
```
