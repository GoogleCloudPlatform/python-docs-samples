# Cloud IoT Core Python HTTP example

This sample app publishes data to Cloud Pub/Sub using the HTTP bridge provided
as part of Google Cloud IoT Core. For detailed running instructions see the
[HTTP code samples
guide](https://cloud.google.com/iot/docs/protocol_bridge_guide).

# Setup

1.  Use virtualenv to create a local Python environment.

```
virtualenv env && source env/bin/activate
```

1.  Install the dependencies

```
pip install -r requirements.txt
```

# Running the Sample

The following snippet summarizes usage:

```
cloudiot_http_example.py [-h]
    --project_id PROJECT_ID
    --registry_id REGISTRY_ID
    --device_id DEVICE_ID
    --private_key_file PRIVATE_KEY_FILE
    --algorithm {RS256,ES256}
    --message_type={event,state}
    [--cloud_region CLOUD_REGION]
    [--ca_certs CA_CERTS]
    [--num_messages NUM_MESSAGES]
```

For example, if your project ID is `blue-jet-123`, the following example shows
how you would execute using the configuration from the HTTP code samples guide:

```
python cloudiot_http_example.py \
    --registry_id=my-registry \
    --project_id=blue-jet-123 \
    --device_id=my-python-device \
    --message_type=event \
    --algorithm=RS256 \
    --private_key_file=../rsa_private.pem
```
