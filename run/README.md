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
|[Cloud SQL (MySQL)][mysql]        | Use MySQL with Cloud Run    |      -        |
|[Cloud SQL (Postgres)][postgres]  | Use Postgres with Cloud Run |      -        |
|[Django][django]                  | Deploy Django on Cloud Run  |      -        |
|[Identity Platform][idp-sql]      | Authenticate users and connect to a Cloud SQL postgreSQL databases | [<img src="https://storage.googleapis.com/cloudrun/button.svg" alt="Run on Google Cloud" height="30">][run_button_idpsql] |

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

## Deploying

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

See [Building containers][run_build] and [Deploying container images][run_deploy]
for more information.

[run_docs]: https://cloud.google.com/run/docs/
[run_build]: https://cloud.google.com/run/docs/building/containers
[run_deploy]: https://cloud.google.com/run/docs/deploying
[helloworld]: helloworld/
[pubsub]: pubsub/
[mysql]: ../cloud-sql/mysql/sqlalchemy
[postgres]: ../cloud-sql/postgres/sqlalchemy
[django]: django/
[idp-sql]: idp-sql/
[run_button_helloworld]: https://deploy.cloud.run/?git_repo=https://github.com/knative/docs&dir=docs/serving/samples/hello-world/helloworld-python
[run_button_pubsub]: https://deploy.cloud.run/?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&dir=run/pubsub
[run_button_idpsql]: https://deploy.cloud.run/?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&dir=run/idp-sql
[testing]: https://cloud.google.com/run/docs/testing/local#running_locally_using_docker_with_access_to_services
