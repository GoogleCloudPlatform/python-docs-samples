# Google Cloud Run Python Samples

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=blog/README.md

This directory contains samples for [Google Cloud Run](https://cloud.run). [Cloud Run][run_docs] runs stateless [containers](https://cloud.google.com/containers/) on a fully managed environment or in your own GKE cluster.

## Samples

|           Sample                |        Description       |     Deploy    |
| ------------------------------- | ------------------------ | ------------- |
|[Hello World][helloworld]&nbsp;&#10149; | Quickstart | [<img src="https://storage.googleapis.com/cloudrun/button.svg" alt="Run on Google Cloud" height="30">][run_button_helloworld] |
|[Cloud Pub/Sub][pubsub] | Handling Pub/Sub push messages | [<img src="https://storage.googleapis.com/cloudrun/button.svg" alt="Run on Google Cloud" height="30">][run_button_pubsub] |

For more Cloud Run samples beyond Python, see the main list in the [Cloud Run Samples repository](https://github.com/GoogleCloudPlatform/cloud-run-samples).

## Setup

1. [Set up for Cloud Run development](https://cloud.google.com/run/docs/setup)

2. Clone this repository:

    ```
    git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
    ```

    Note: Some samples in the list above are hosted in other repositories. They are noted with the symbol "&#10149;".


## How to run a sample locally

1. [Install docker locally](https://docs.docker.com/install/)

2. [Build the sample container](https://cloud.google.com/run/docs/building/containers#building_locally_and_pushing_using_docker):

    ```
    export SAMPLE=$sample
    cd $SAMPLE
    docker build --tag $sample .
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

    Injecting your service account key:

    ```
    export SA_KEY_NAME=my-key-name-123
    PORT=8080 && docker run --rm \
        -p 8080:${PORT} -e PORT=${PORT} \
        -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/${SA_KEY_NAME}.json \
        -v $GOOGLE_APPLICATION_CREDENTIALS:/tmp/keys/${SA_KEY_NAME}.json:ro \
        -v $PWD:/app $SAMPLE
    ```

## Deploying

```
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/${SAMPLE}
gcloud beta run deploy $SAMPLE \
  # Needed for Manual Logging sample.
  --set-env-var GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}
  --image gcr.io/${GOOGLE_CLOUD_PROJECT}/${SAMPLE}
```

See [Building containers][run_build] and [Deploying container images][run_deploy]
for more information.

[run_docs]: https://cloud.google.com/run/docs/
[run_build]: https://cloud.google.com/run/docs/building/containers
[run_deploy]: https://cloud.google.com/run/docs/deploying
[helloworld]: https://github.com/knative/docs/tree/master/docs/serving/samples/hello-world/helloworld-python
[pubsub]: pubsub/
[run_button_helloworld]: https://console.cloud.google.com/cloudshell/editor?shellonly=true&cloudshell_image=gcr.io/cloudrun/button&cloudshell_git_repo=https://github.com/knative/docs&cloudshell_working_dir=docs/serving/samples/hello-world/helloworld-python
[run_button_pubsub]: https://console.cloud.google.com/cloudshell/editor?shellonly=true&cloudshell_image=gcr.io/cloudrun/button&cloudshell_git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&cloudshell_working_dir=run/pubsub
