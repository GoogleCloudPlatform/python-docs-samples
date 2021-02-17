# Google Cloud Eventarc Python Samples

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=blog/README.md

This directory contains samples for Google Cloud Eventarc.

## Samples

|           Sample                |        Description       |     Deploy    |
| ------------------------------- | ------------------------ | ------------- |
|[Events – Pub/Sub][events_pubsub]  | Event-driven service with Events for Cloud Run for Pub/Sub    |      -        |
|[Anthos Events – Pub/Sub][anthos_events_pubsub]  | Event-driven service with Events for Cloud Run on Anthos for Pub/Sub  |      -        |
|[Events – GCS][events_storage]  | Event-driven service with Events for Cloud Run for GCS    |      -        |
|[Anthos Events – GCS][anthos_events_storage]  | Event-driven service with Events for Cloud Run on Anthos for GCS  |      -        |

For more Cloud Run samples beyond Python, see the main list in the [Cloud Run Samples repository](https://github.com/GoogleCloudPlatform/cloud-run-samples).

## Setup

1. [Set up for Cloud Run development](https://cloud.google.com/run/docs/setup)

2. Clone this repository:

    ```
    git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
    ```

    Note: Some samples in the list above are hosted in other repositories. They are noted with the symbol "&#10149;".

## How to run a sample locally

Install [`pip`][pip] and [`virtualenv`][virtualenv] if you do not already have them.

You may want to refer to the [`Python Development Environment Setup Guide`][setup] for Google Cloud Platform for instructions.   

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

## How to run a sample in a container

1. [Install docker locally](https://docs.docker.com/install/)

2. [Build the sample container](https://cloud.google.com/run/docs/building/containers#building_locally_and_pushing_using_docker):

    ```
    export SAMPLE=<SAMPLE_NAME>
    cd $SAMPLE
    docker build --tag $SAMPLE .
    ```

3. [Run containers locally](https://cloud.google.com/run/docs/testing/local)

    With the built container:

    ```
    PORT=8080 && docker run --rm -p 8080:${PORT} -e PORT=${PORT} $SAMPLE
    ```

    Overriding the built container with local code:

    ```
    PORT=8080 && docker run --rm \
        -p 8080:${PORT} -e PORT=${PORT} \
        -v $PWD:/app $SAMPLE
    ```

    Injecting your service account key for access to GCP services:

    ```
    # Set the name of the service account key within the container
    export SA_KEY_NAME=my-key-name-123

    PORT=8080 && docker run --rm \
        -p 8080:${PORT} \
        -e PORT=${PORT} \
        -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/${SA_KEY_NAME}.json \
        -v $GOOGLE_APPLICATION_CREDENTIALS:/tmp/keys/${SA_KEY_NAME}.json:ro \
        -v $PWD:/app $SAMPLE
    ```

    * Use the --volume (-v) flag to inject the credential file into the container
      (assumes you have already set your `GOOGLE_APPLICATION_CREDENTIALS`
      environment variable on your machine)

    * Use the --environment (-e) flag to set the `GOOGLE_APPLICATION_CREDENTIALS`
      variable inside the container

    Learn more about [testing your container image locally.][testing]

## Deploying a Cloud Run service

1. Set an environment variable with your GCP Project ID
    ```
    export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>
    ```

1. Submit a build using Google Cloud Build
    ```
    gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/${SAMPLE}
    ```

1. Deploy to Cloud Run
    ```
    gcloud run deploy $SAMPLE --image gcr.io/${GOOGLE_CLOUD_PROJECT}/${SAMPLE}
    ```

Choose a particular sample for information about triggering the service with an event.

See [Building containers][run_build] and [Deploying container images][run_deploy]
for more information.

[run_docs]: https://cloud.google.com/run/docs/
[run_build]: https://cloud.google.com/run/docs/building/containers
[run_deploy]: https://cloud.google.com/run/docs/deploying
[events_pubsub]: pubsub/README.md
[anthos_events_pubsub]: pubsub/anthos.md
[events_storage]: audit-storage/README.md
[anthos_events_storage]: audit-storage/anthos.md
[testing]: https://cloud.google.com/run/docs/testing/local#running_locally_using_docker_with_access_to_services
[setup]: https://cloud.google.com/python/setup
[pip]: https://pip.pypa.io/
[virtualenv]: https://virtualenv.pypa.io/
