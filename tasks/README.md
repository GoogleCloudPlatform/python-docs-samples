# Google Cloud Tasks Samples

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=tasks/README.md

This sample demonstrates how to use the
[Cloud Tasks](https://cloud.google.com/tasks/docs/) client library.

`create_http_task.py` is a simple command-line program to create
tasks to be pushed to an URL endpoint.

`create_http_task_with_token.py` is a simple command-line program to create
tasks to be pushed to an URL endpoint with authorization header.

## Prerequisites to run locally:

Please refer to [Setting Up a Python Development Environment](https://cloud.google.com/python/setup).

## Authentication

To set up authentication, please refer to our
[authentication getting started guide](https://cloud.google.com/docs/authentication/getting-started).

## Install Dependencies

To install the dependencies for this sample, use the following command:

```
pip install -r requirements.txt
```

This sample uses the common protos in the [googleapis](https://github.com/googleapis/googleapis)
repository. For more info, see
[Protocol Buffer Basics](https://developers.google.com/protocol-buffers/docs/pythontutorial).

## Creating a queue

To create a queue (named `my-queue`) using the Cloud SDK, use the following
gcloud command:

```
gcloud tasks queues create my-queue
```

## Run the Sample Using the Command Line

Set environment variables:

First, your project ID:

```
export PROJECT_ID=my-project-id
```

Then the queue ID, as specified at queue creation time. Queue IDs already
created can be listed with `gcloud tasks queues list`.

```
export QUEUE_ID=my-queue
```

And finally the location ID, which can be discovered with
`gcloud tasks queues describe my-queue`, with the location embedded in
the "name" value (for instance, if the name is
"projects/my-project/locations/us-central1/queues/my-queue", then the
location is "us-central1").

```
export LOCATION_ID=us-central1
```

### Creating Tasks with HTTP Targets

Set an environment variable for the endpoint to your task handler. This is an
example url:
```
export URL=https://example.com/task_handler
```

Running the sample will create a task and send the task to the specific URL
endpoint, with a payload specified:

```
python create_http_task.py --project=$PROJECT_ID --queue=$QUEUE_ID --location=$LOCATION_ID --url=$URL --payload=hello
```
