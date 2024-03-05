
# Dataflow flex template: a pipeline with dependencies and a custom container image.

This project is created to illustrate the following setup of a Dataflow Python pipeline:
- The pipeline is a package that consists of [multiple files](https://beam.apache.org/documentation/sdks/python-pipeline-dependencies/#multiple-file-dependencies).
- The pipeline has at least one dependency that is not provided in the default Dataflow runtime environment.
- The workflow uses a [custom container image](https://cloud.google.com/dataflow/docs/guides/using-custom-containers) to preinstall dependencies and to define the pipeline runtime environment.
- The workflow uses a [Dataflow Flex Template](https://cloud.google.com/dataflow/docs/concepts/dataflow-templates) to control the pipeline submission environment.
- The runtime and submission environment use same set of Python dependencies and can be created in a reproducible manner.

To illustrate this setup, we use a pipeline that does the following:

1. Finds the longest word in an input file
2. Creates a [FIGLet text banner](https://en.wikipedia.org/wiki/FIGlet) from of it using [pyfiglet](https://pypi.org/project/pyfiglet/)
3. Outputs the text banner in another file


## The structure of the example

The pipeline package is comprised of the `my_package` directory and the `setup.py` file. The package defines the pipeline, the pipeline dependencies, and the input parameters. You can define multiple pipelines in the same package. The `my_package.launcher` file is used to submit the pipeline to a runner.

The `main.py` file provides a top-level entrypoint to trigger the pipeline launcher from a
launch environment.

The `Dockerfile` defines the runtime environment for the pipeline. It also configures the Flex Template, which lets you reuse the runtime image to build the Flex Template.

The`Dockerfile.flex_template` and `flex_template_cloudbuild.yaml` files provide the remaining instructions to build the Flex Template.

The `requirements.txt` file defines all Python packages in the dependency chain of the pipeline package. Use it to create reproducible Python environments in the Docker images.

## Before you begin

Follow the
[Dataflow setup instructions](../../README.md).

## Create a Cloud Storage bucket

```sh
export PROJECT="project-id"
export BUCKET="your-bucket"
export REGION="us-central1"
gsutil mb -p $PROJECT gs://$BUCKET
```

## Create an Artifact Registry repository

```sh
export REPOSITORY="your-repository"
gcloud artifacts repositories create $REPOSITORY \
    --repository-format=docker \
    --location=$REGION

gcloud artifacts repositories create $REPOSITORY \
    --repository-format=docker \
    --location=$REGION \
    --project $PROJECT
```

## Build a Docker image for the pipeline runtime environment

Using a [custom SDK container image](https://cloud.google.com/dataflow/docs/guides/using-custom-containers)
allows flexible customizations of the runtime environment.

We use the custom container image both to preinstall all of the pipeline dependencies before job submission and to create a reproducible runtime environment.

To illustrate customizations, we use a [custom base base image](https://cloud.google.com/dataflow/docs/guides/build-container-image#use_a_custom_base_image) to build the SDK container image.

```sh
# Use a unique tag to version artifacts we build.
export TAG=`date +%Y%m%d-%H%M%S`
export SDK_CONTAINER_IMAGE="$REGION-docker.pkg.dev/$PROJECT/$REPOSITORY/my_base_image:$TAG"

gcloud builds submit .  --tag $SDK_CONTAINER_IMAGE --project $PROJECT
```

You must rebuild the base image when your pipeline dependencies change.

## Build the Flex Template

To build the Flex Templates, use the [runtime image as the base image](https://cloud.google.com/dataflow/docs/guides/templates/configuring-flex-templates#use_custom_container_images).
Using the runtime image as the base image allows us to reduce the number of Docker images that need to be maintained.
It also ensures that the pipeline uses the same dependencies at submission and at runtime.

```sh
export TEMPLATE_FILE=gs://$BUCKET/longest-word-$TAG.json
export TEMPLATE_IMAGE=$REGION-docker.pkg.dev/$PROJECT/$REPOSITORY/my_template_image:$TAG
```

```sh
gcloud dataflow flex-template build $TEMPLATE_FILE  \
    --image-gcr-path $TEMPLATE_IMAGE \
    --sdk-language "PYTHON" \
    --flex-template-base-image $SDK_CONTAINER_IMAGE \
    --py-path "."  \
    --env "FLEX_TEMPLATE_PYTHON_PY_FILE=main.py" \
    --env "FLEX_TEMPLATE_PYTHON_SETUP_FILE=setup.py" \
    --project $PROJECT
```

Note: Older versions of `gcloud` might not support Artifact Registry in the `--flex-template-base-image` option. You might need to upgrade `gcloud` or build the Flex Template from a `Dockerfile` using the instructions below.

If you prefer to have a separate file to configure and build the Flex Template image (included in the example), such as a `Dockefile.flex_template` file, you can build the Flex Template as follows:

```sh
gcloud builds submit --config flex_template_cloudbuild.yaml \
    --substitutions="_TEMPLATE_IMAGE=${TEMPLATE_IMAGE},_BASE_IMAGE=${SDK_CONTAINER_IMAGE}" \
    --project $PROJECT

gcloud dataflow flex-template build $TEMPLATE_FILE  \
    --image $TEMPLATE_IMAGE \
    --sdk-language "PYTHON" \
    --project $PROJECT
```

## Run the template

```sh
gcloud dataflow flex-template run "flex-`date +%Y%m%d-%H%M%S`" \
    --template-file-gcs-location $TEMPLATE_FILE \
    --region $REGION \
    --staging-location "gs://$BUCKET/staging" \
    --parameters input="gs://dataflow-samples/shakespeare/hamlet.txt" \
    --parameters output="gs://$BUCKET/output" \
    --parameters sdk_container_image=$SDK_CONTAINER_IMAGE \
    --project $PROJECT
```

After the pipeline finishes, use the following command to inspect the output:
```
gsutil cat gs://$BUCKET/output*
```

## Optional: Update the dependencies in requirements.txt and rebuild the Docker images

The top-level pipeline dependencies are defined in the `install_requires` section of the `setup.py` file.

The `requirements.txt` file pins all Python dependencies, including transitive dependencies, that must be installed in the Docker base images. This step produces a reproducible set of dependencies every time the image is built.
Version control the `requirements.txt` file together with the rest of pipeline code.

When the dependencies of your pipeline change or when you want to use the latest available versions of packages in the pipeline's dependency chain,  regenerate the `requirements.txt` file:

```
    python3.11 -m pip install pip-tools   # Use a consistent minor version of Python throughout the project.
    pip-compile ./setup.py
```

To reduce the image size and to give preference to the versions already installed in the Apache Beam base image, use a constraints file:

```
   wget https://raw.githubusercontent.com/apache/beam/release-2.54.0/sdks/python/container/py311/base_image_requirements.txt
   pip-compile --constraint=base_image_requirements.txt ./setup.py
```

Alternatively, use an empty `requirements.txt` file,  build the SDK container Docker image from the Docker file,
collect the output of `pip freeze` at the last stage of the Docker build, and seed the `requirements.txt` with that content.

For more information, see the Apache Beam [reproducible environments](https://beam.apache.org/documentation/sdks/python-pipeline-dependencies/#create-reproducible-environments) documentation.


## What's next?

For more information about building and running Flex Templates, see
📝 [Use Flex Templates](https://cloud.google.com/dataflow/docs/guides/templates/using-flex-templates).

For more information about building and using custom containers, see
📝 [Use custom containers in Dataflow](https://cloud.google.com/dataflow/docs/guides/using-custom-containers).

To reduce Docker image build time, see:
📝 [Using Kaniko Cache](https://cloud.google.com/build/docs/optimize-builds/kaniko-cache).