# Cloud IoT Core Python Samples
This folder contains Python samples that demonstrate an overview of the
commands beta feature.

## Quickstart
1. Install the Cloud SDK as described in [the device manager guide](https://cloud.google.com/iot/docs/device_manager_guide).
2. Create a PubSub topic:

    gcloud beta pubsub topics create projects/my-iot-project/topics/device-events

3. Create a registry:

    gcloud iot registries create my-registry \
        --project=my-iot-project \
        --region=us-central1 \
        --event-notification-config=topic=projects/intense-wavelet-343/topics/device-events

4. Use the `generate_keys.sh` script to generate your signing keys:

    <path-to>/python-docs-samples/iot/api-client/generate_keys.sh

5. Register a device:

    gcloud iot devices create my-python-device \
        --project=my-iot-project \
        --region=us-central1 \
        --registry=my-registry \
        --public-key path=rsa_cert.pem,type=rs256

6. Connect a virtual device using the sample app in the `receive` folder.
7. While the virtual device is connected, send a commmand using the sample app in the `send` folder.
