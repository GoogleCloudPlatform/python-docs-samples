# Eventarc Python Samples

This directory contains python samples for Eventarc.

## Samples

- [Pub/Sub][events_pubsub]
- [Audit Logs – Cloud Storage][events_audit_storage]
- [Generic][events_generic]

## Setup

1. [Set up for Cloud Run development](https://cloud.google.com/run/docs/setup)

1. Install [`pip`][pip] and [`virtualenv`][virtualenv] if you do not already have them.

    - You may want to refer to the [`Python Development Environment Setup Guide`][setup] for Google Cloud Platform for instructions.   

1. Create a virtualenv. Samples are compatible with Python 2.7 and 3.4+.

    ```sh
    virtualenv env
    source env/bin/activate
    ```

1. Install the dependencies needed to run the samples.

    ```sh
    pip install -r requirements.txt
    ```

1. Start the application

    ```sh
    python main.py
    ```

[events_pubsub]: pubsub/
[events_audit_storage]: audit-storage/
[events_generic]: generic/
[setup]: https://cloud.google.com/python/setup
[pip]: https://pip.pypa.io/
[virtualenv]: https://virtualenv.pypa.io/
