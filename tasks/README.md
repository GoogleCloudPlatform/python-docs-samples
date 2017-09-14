# Google Cloud Tasks Pull Queue Samples

Sample command-line program for interacting with the Google Cloud Tasks API
using pull queues.

Pull queues let you add tasks to a queue, then programatically remove and
interact with them. Tasks can be added or processed in any environment,
such as on Google App Engine or Google Compute Engine.

`pull_queue_snippets.py` is a simple command-line program to demonstrate listing queues,
 creating tasks, and pulling and acknowledging tasks.

## Prerequisites to run locally:

Please refer to [Setting Up a Python Development Environment](https://cloud.google.com/python/setup).

## Authentication

To set up authentication, please refer to our
[authentication getting started guide](https://cloud.google.com/docs/authentication/getting-started).

## Creating a queue

To create a queue using the Cloud SDK, use the following gcloud command:

    gcloud alpha tasks queues create-pull-queue my-pull-queue

## Running the Samples

Set the environment variables:

Set environment variables:

First, your project ID:

    export PROJECT_ID=my-project-id

Then the queue ID, as specified at queue creation time. Queue IDs already
created can be listed with `gcloud alpha tasks queues list`.

    export QUEUE_ID=my-pull-queue

And finally the location ID, which can be discovered with
`gcloud alpha tasks queues describe $QUEUE_ID`, with the location embedded in
the "name" value (for instance, if the name is
"projects/my-project/locations/us-central1/queues/my-pull-queue", then the
location is "us-central1").

    export LOCATION_ID=us-central1

Create a task for a queue:

    python pull_queue_snippets.py create-task --project=$PROJECT_ID --queue=$QUEUE_ID --location=$LOCATION_ID

Pull and acknowledge a task:

    python pull_queue_snippets.py pull-and-ack-task --project=$PROJECT_ID --queue=$QUEUE_ID --location=$LOCATION_ID

Note that usually, there would be a processing step in between pulling a task and acknowledging it.
