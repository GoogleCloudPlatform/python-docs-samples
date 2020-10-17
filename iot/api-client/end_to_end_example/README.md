Google Cloud IoT Core Python Samples
====================================

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=/README.rst)

This directory contains samples for Google Cloud IoT Core. [Google Cloud
IoT Core](https://cloud.google.com/iot/docs) allows developers to easily
integrate Publish and Subscribe functionality with devices and
programmatically manage device authorization. Before you run the sample,
you must retrieve the Google root certificate. For example,
`wget https://pki.goog/roots.pem` or
`curl https://pki.goog/roots.pem > roots.pem`.

Setup
-----

### Authentication

This sample requires you to have authentication setup. Refer to the
[Authentication Getting Started
Guide](https://cloud.google.com/docs/authentication/getting-started) for
instructions on setting up credentials for applications.

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

### Server

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=/cloudiot_pubsub_example_server.py,/README.rst)

To run this sample:

``` {.bash}
$ python cloudiot_pubsub_example_server.py

usage: cloudiot_pubsub_example_server.py [-h] --project_id PROJECT_ID
                                         --pubsub_subscription
                                         PUBSUB_SUBSCRIPTION
                                         [--service_account_json SERVICE_ACCOUNT_JSON]

Example of Google Cloud IoT registry and device management.

optional arguments:
  -h, --help            show this help message and exit
  --project_id PROJECT_ID
                        GCP cloud project name.
  --pubsub_subscription PUBSUB_SUBSCRIPTION
                        Google Cloud Pub/Sub subscription name.
  --service_account_json SERVICE_ACCOUNT_JSON
                        Path to service account json file.
```

### Device

[![image](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=/cloudiot_pubsub_example_mqtt_device.py,/README.rst)

To run this sample:

``` {.bash}
$ python cloudiot_pubsub_example_mqtt_device.py

usage: cloudiot_pubsub_example_mqtt_device.py [-h] --project_id PROJECT_ID
                                              --registry_id REGISTRY_ID
                                              --device_id DEVICE_ID
                                              --private_key_file
                                              PRIVATE_KEY_FILE --algorithm
                                              {RS256,ES256}
                                              [--cloud_region CLOUD_REGION]
                                              [--ca_certs CA_CERTS]
                                              [--num_messages NUM_MESSAGES]
                                              [--mqtt_bridge_hostname MQTT_BRIDGE_HOSTNAME]
                                              [--mqtt_bridge_port MQTT_BRIDGE_PORT]
                                              [--message_type {event,state}]

Example Google Cloud IoT MQTT device connection code.

optional arguments:
  -h, --help            show this help message and exit
  --project_id PROJECT_ID
                        GCP cloud project name.
  --registry_id REGISTRY_ID
                        Cloud IoT registry id
  --device_id DEVICE_ID
                        Cloud IoT device id
  --private_key_file PRIVATE_KEY_FILE
                        Path to private key file.
  --algorithm {RS256,ES256}
                        Which encryption algorithm to use to generate the JWT.
  --cloud_region CLOUD_REGION
                        GCP cloud region
  --ca_certs CA_CERTS   CA root certificate. Get from
                        https://pki.google.com/roots.pem
  --num_messages NUM_MESSAGES
                        Number of messages to publish.
  --mqtt_bridge_hostname MQTT_BRIDGE_HOSTNAME
                        MQTT bridge hostname.
  --mqtt_bridge_port MQTT_BRIDGE_PORT
                        MQTT bridge port.
  --message_type {event,state}
                        Indicates whether the message to be published is a
                        telemetry event or a device state message.
```
