# Cloud IoT Core Python Samples

## DEPRECATION NOTICE

Please see the [release notes](https://cloud.google.com/iot/docs/release-notes) for information on the upcoming deprecation of IoT Core

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=iot/api-client/README.md
This folder contains Python samples that demonstrate an overview of the
Google Cloud IoT Core platform.

## Quickstart
1. Install the gCloud CLI as described in [the Cloud IoT Core documentation](https://cloud.google.com/iot/docs/how-tos/getting-started#set_up_the_google_cloud_sdk_and_gcloud).
2. Create a PubSub topic:

    gcloud beta pubsub topics create projects/my-iot-project/topics/device-events

3. Add the service account `cloud-iot@system.gserviceaccount.com` with the role `Publisher` to that
PubSub topic from the [Cloud Developer Console](https://console.cloud.google.com)
or by using the helper script in the /scripts folder.

4. Create a registry:

    gcloud beta iot registries create my-registry \
        --project=my-iot-project \
        --region=us-central1 \
        --event-pubsub-topic=projects/my-iot-project/topics/device-events

5. Use the `generate_keys.sh` script to generate your signing keys:

    ./generate_keys.sh

6. Register a device:

    gcloud beta iot devices create my-python-device \
        --project=my-iot-project \
        --region=us-central1 \
        --registry=my-registry \
        --public-key path=rsa_cert.pem,type=rs256

7. Connect a sample device using the sample app in the `mqtt_example` folder.
8. Learn how to manage devices programmatically with the sample app in the
`manager` folder.

