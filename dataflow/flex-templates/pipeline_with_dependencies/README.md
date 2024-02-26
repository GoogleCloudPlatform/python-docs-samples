
# Dataflow flex template: a pipeline with dependencies and a custom container image.

This project is created to illustrate the following setup of a Dataflow Python pipeline:
- The pipeline is a package that consists of [multiple files](https://beam.apache.org/documentation/sdks/python-pipeline-dependencies/#multiple-file-dependencies).
- The pipeline has at least one depenendency that is not provided in the default Dataflow runtime environment.
- The workflow uses a [custom container image](https://cloud.google.com/dataflow/docs/guides/using-custom-containers) to preinstall dependencies and define the pipeline runtime environment.
- The workflow uses a [Dataflow Flex template](https://cloud.google.com/dataflow/docs/concepts/dataflow-templates) to control the pipeline submission environment.
- The runtime and submission environment use same set of Python dependencies and can be created in a reproducible manner.

To illustrate this setup, we will use a pipepline that finds a longest word in an input file, crates a [FIGLet text banner](https://en.wikipedia.org/wiki/FIGlet) from of it using [pyfiglet](https://pypi.org/project/pyfiglet/), and outputs it in another file.


## The structure of the example

The `my_package` directory together with `setup.py` comprise the pipeline package. The package defines the pipeline, its dependenicies and input parameters. It is possible to define multiple pipelines in the same package. The `my_package.launcher` is used to submit the pipeline to a runner.

The `main.py` file provides a top-level entrypoint to trigger the pipeline launcher from a
launch environment.

The `Dockerfile` defines the runtime environment for our pipeline, and also configures the Flex Template, so that we can reuse runtime image for building our Flex Template.

The`Dockerfile.flex_template` and `flex_template_cloudbuild.yaml` files provide the remaining instructions to build the Flex template.

The `requirements.txt` defines all Python packages in the dependency chain of our pipeline package. We use it to create reproducible Python environments in our Docker images.

## Before you begin

Make sure you have followed the
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

## Build a Docker image for pipeline runtime environment

Using a [custom SDK container image](https://cloud.google.com/dataflow/docs/guides/using-custom-containers)
allows flexible customizations of the runtime environment.

We use the custom container image to preinstall all dependencies of our pipeline ahead of job submission and to have a reproducible runtime environment.

To illustrate customizations, we use a [custom base base image](https://cloud.google.com/dataflow/docs/guides/build-container-image#use_a_custom_base_image) to build the SDK container image.

```sh
# Use a unique tag to version artifacts we build.
export TAG=`date +%Y%m%d-%H%M%S`
export SDK_CONTAINER_IMAGE="$REGION-docker.pkg.dev/$PROJECT/$REPOSITORY/my_base_image:$TAG"

gcloud builds submit .  --tag $SDK_CONTAINER_IMAGE --project $PROJECT
```

You must rebuild the base image when your pipeline dependencies change.

## Build the Flex template

We will use the [runtime image as the base image](https://cloud.google.com/dataflow/docs/guides/templates/configuring-flex-templates#use_custom_container_images)
 when building our Flex templates.
This allows us to reduce the number of Docker images to maintain and
it ensures that the pipeline  uses the same dependencies at submission and at runtime.

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

Note: Older versions of gcloud might not support AR and require using GCR registry images in the `--flex-template-base-image` option.

If you prefer to have a separate file, such as `Dockefile.flex_template` to configure and build the Flex template image (included in the example), you can build the Flex template as follows:

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

After the pipeline finishes, you can inspect the output via:
```
gsutil cat gs://$BUCKET/output*
```

## (Optional) Update the dependencies in requirements.txt and rebuild the Docker images

The top level dependencies of the pipeline are defined in the `install_requires` stanza of `setup.py`.

The `requirements.txt` file pins all Python dependenciences, including transitive dependencies, that must be installed in Docker base images to have reproducible set of dependencies every time the image is built.
The requirements.txt should be version-controlled together with the rest of pipeline code.

When the dependencies of your pipeline has change or you  want to use the latest available versions of packages in the pipeline's dependency chain,  you can regenerate the `requirements.txt` as follows:

```
    python3.11 -m pip install pip-tools   # Use consistent minor version of Python thorughout the project.
    pip-compile ./setup.py
```

To reduce the image size and prefer the versions already installed in Apache Beam base image, use a constraints file:

```
   wget https://raw.githubusercontent.com/apache/beam/release-2.54.0/sdks/python/container/py311/base_image_requirements.txt
   pip-compile --constraint=base_image_requirements.txt ./setup.py
```

Alternatively, you can use an empty requirements.txt file,  build the SDK container Docker image from the Dockerfile,
collect the output of `pip freeze` at the last stage of Docker build, and seed `requirements.txt` with that content.

For more information, see Apache Beam documentation on [reporoducible environments](https://beam.apache.org/documentation/sdks/python-pipeline-dependencies/#create-reproducible-environments).


## What's next?

For more information about building and running flex templates, see
📝 [Use Flex Templates](https://cloud.google.com/dataflow/docs/guides/templates/using-flex-templates).

For more information about building and using custom containers, see
📝 [Use Custom Containers](https://cloud.google.com/dataflow/docs/guides/using-custom-containers).

To reduce Docker image build time, see:
📝 [Using Kaniko Cache](https://cloud.google.com/build/docs/optimize-builds/kaniko-cache).