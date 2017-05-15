# Cloud IoT Core Device Manager Python Sample

This sample application shows you how to manage devices programmatically using
Python.


# Setup

1. Use virtualenv to create a local Python environment.

    virtualenv env && source env/bin/activate

2. Install the dependencies

    pip install -r requirements.txt


# Running the sample

The following snippet summarizes usage for the device manager sample:

    usage: cloudiot_device_manager_example.py [-h] \
        --project_id PROJECT_ID \
        --pubsub_topic PUBSUB_TOPIC \
        --api_key API_KEY \
        [--ec_public_key_file EC_PUBLIC_KEY_FILE] \
        [--rsa_certificate_file RSA_CERTIFICATE_FILE] \
        [--cloud_region CLOUD_REGION] \
        [--service_account_json SERVICE_ACCOUNT_JSON] \
        [--registry_id REGISTRY_ID]


For example, if your project-id is `blue-jet-123` and your service account
credentials are stored in `creds.json` in your home folder, the following
command would run the sample:

    python cloudiot_device_manager_example.py \
      --project_id blue-jet-123 \
      --pubsub_topic projects/blue-jet-123/topics/device-events \
      --ec_public_key ../ec_public.pem \
      --rsa_certificate_file ../rsa_cert.pem \
      --api_key YOUR_API_KEY \
      --service_account_json $HOME/creds.json
