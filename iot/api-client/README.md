# Cloud IoT Core Python Samples
This folder contains Python samples that demonstrate an overview of the
Google Cloud IoT Core platform.

## Quickstart
1. Install the gCloud CLI as described in [the device manager guide](https://cloud.google.com/iot/docs/device_manager_guide).
2. Create a PubSub topic:

    gcloud beta pubsub topics create projects/my-iot-project/topics/device-events

3. Add the service account `cloud-iot@system.gserviceaccount.com` to that
PubSub topic from the [Cloud Developer Console](https://console.cloud.google.com)
or by using the helper script in the /scripts folder.

4. Create a registry:

    gcloud alpha iot registries create my-registry \
        --project=my-iot-project \
        --region=us-central1 \
        --pubsub-topic=projects/my-iot-project/topics/device-events

5. Use the `generate_keys.sh` script to generate your signing keys:

    ./generate_keys.sh

6. Register a device:

    gcloud alpha iot devices create my-python-device \
        --project=my-iot-project \
        --region=us-central1 \
        --registry=my-registry \
        --public-key path=rsa_cert.pem,type=rs256

7. Connect a sample device using the sample app in the `mqtt_example` folder.
8. Learn how to manage devices programatically with the sample app in the
`manager` folder.

