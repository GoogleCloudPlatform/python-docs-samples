# Google Cloud Run for Anthos Python Samples

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=anthos/run/README.md

This directory contains samples for [Cloud Run for Anthos](https://cloud.google.com/anthos/run).
[Cloud Run for Anthos][runanthos_docs] runs stateless [containers](https://cloud.google.com/containers/)
in your own GKE cluster.

## Samples

|           Sample                |        Description       |     Open in Cloud Shell    |
| ------------------------------- | ------------------------ | ------------- |
|[Hello World][helloworld] | Quickstart | [![Open in Cloud Shell][shell_img]][openinshell_button_helloworld] |
|[Local Troubleshooting][hello_broken] | Troubleshoot broken CRfA services | [![Open in Cloud Shell][shell_img]][openinshell_button_hello_broken] |
|[Pub/Sub][pubsub] | Use Google Cloud Pub/Sub with CRfA services | [![Open in Cloud Shell][shell_img]][openinshell_button_pubsub] |
|[Image Processing][image_processing] | Process images with CRfA services | [![Open in Cloud Shell][shell_img]][openinshell_image_processing] |
|[System Package][system_package] | Use system packages in CRfA services | [![Open in Cloud Shell][shell_img]][openinshell_system_package] |
|[Logging][logging_manual] | Write logs in CRfA services | [![Open in Cloud Shell][shell_img]][openinshell_logging_manual] |


## Setup

1. [Set up Cloud Run for Anthos](https://cloud.google.com/anthos/run/docs/setup)

2. Clone this repository:

    ```
    git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
    ```


## Run a sample locally

1. [Install docker locally](https://docs.docker.com/install/)

2. Build the sample container:

    ```sh
    export SAMPLE=<SAMPLE_NAME>
    cd $SAMPLE
    docker build --tag $SAMPLE .
    ```

3.  Run containers locally

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

    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # on your local machine
    export GOOGLE_APPLICATION_CREDENTIALS=PATH-TO-CREDENTIAL

    PORT=8080 && docker run --rm \
        -p 8080:${PORT} \
        -e PORT=${PORT} \
        -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/${SA_KEY_NAME}.json \
        -v $GOOGLE_APPLICATION_CREDENTIALS:/tmp/keys/${SA_KEY_NAME}.json:ro \
        -v $PWD:/app $SAMPLE
    ```

    * The --volume (-v) flag injects the credential file into the container

    * The --environment (-e) flag sets the environment variable inside the container

See [Local Testing][runanthos_local_testing] for more information.

## Deploying

1. Set an environment variable with your GCP Project ID

    ```sh
    export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>
    ```

1. [Set up `gcloud` defaults](https://cloud.google.com/anthos/run/docs/setup#configuring_default_settings_for_gcloud).

1. Submit a build using Google Cloud Build

    ```
    gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/${SAMPLE}
    ```

1. Deploy to Cloud Run for Anthos

    ```
    gcloud run deploy ${SAMPLE} \
        --platform=managed \
        --image gcr.io/${GOOGLE_CLOUD_PROJECT}/${SAMPLE}
    ```

See [Building containers][runanthos_build] and [Deploying container images][runanthos_deploy]
for more information.

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[runanthos_docs]: https://cloud.google.com/anthos/run/docs/
[runanthos_build]: https://cloud.google.com/anthos/run/docs/building/containers
[runanthos_deploy]: https://cloud.google.com/anthos/run/docs/deploying
[runanthos_local_testing]: https://cloud.devsite.corp.google.com/anthos/run/docs/testing/local

[helloworld]: helloworld/
[hello_broken]: hello-broken/
[pubsub]: pubsub/
[image_processing]: image-processing/
[system_package]: system-package/
[logging_manual]: logging-manual/

[openinshell_button_helloworld]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=anthos/run/helloworld/README.md
[openinshell_button_hello_broken]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=anthos/run/hello-broken/README.md
[openinshell_button_pubsub]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=anthos/run/pubsub/README.md
[openinshell_image_processing]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=anthos/run/image-processing/README.md
[openinshell_system_package]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=anthos/run/system-package/README.md
[openinshell_logging_manual]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=anthos/run/logging-manual/README.md
