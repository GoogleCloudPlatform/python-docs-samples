# Google Cloud Tasks Samples

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/flexible/tasks/README.md

Sample command-line programs for interacting with the Cloud Tasks API
.

App Engine queues push tasks to an App Engine HTTP target. This directory
contains both the App Engine app to deploy, as well as the snippets to run
locally to push tasks to it, which could also be called on App Engine.

`create_app_engine_queue_task.py` is a simple command-line program to create
tasks to be pushed to the App Engine app.

`main.py` is the main App Engine app. This app serves as an endpoint to receive
App Engine task attempts.

`app.yaml` configures the App Engine app.


## Prerequisites to run locally:

Please refer to [Setting Up a Python Development Environment](https://cloud.google.com/python/setup).

### Authentication

To set up authentication, please refer to our
[authentication getting started guide](https://cloud.google.com/docs/authentication/getting-started).

### Install Dependencies

To install the dependencies for this sample, use the following command:

```
pip install -r requirements.txt
```

This sample uses the common protos in the [googleapis](https://github.com/googleapis/googleapis)
repository. For more info, see
[Protocol Buffer Basics](https://developers.google.com/protocol-buffers/docs/pythontutorial).

## Creating a queue

To create a queue using the Cloud SDK, use the following gcloud command:

```
gcloud tasks queues create my-appengine-queue
```

Note: A newly created queue will route to the default App Engine service and
version unless configured to do otherwise.

## Deploying the App Engine App

Deploy the App Engine app with gcloud:

* To deploy to the Standard environment:
  ```
  gcloud app deploy app.yaml
  ```
* To deploy to the Flexible environment:
  ```
  gcloud app deploy app.flexible.yaml
  ```

Verify the index page is serving:

```
gcloud app browse
```

The App Engine app serves as a target for the push requests. It has an
endpoint `/example_task_handler` that reads the payload (i.e., the request body)
of the HTTP POST request and logs it. The log output can be viewed with:

```
gcloud app logs read
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
export QUEUE_ID=my-appengine-queue
```

And finally the location ID, which can be discovered with
`gcloud tasks queues describe $QUEUE_ID`, with the location embedded in
the "name" value (for instance, if the name is
"projects/my-project/locations/us-central1/queues/my-appengine-queue", then the
location is "us-central1").

```
export LOCATION_ID=us-central1
```
### Using App Engine Queues
Running the sample will create a task, targeted at the `/example_task_handler`
endpoint, with a payload specified:

```
python create_app_engine_queue_task.py --project=$PROJECT_ID --queue=$QUEUE_ID --location=$LOCATION_ID --payload=hello
```
