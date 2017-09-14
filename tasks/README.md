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

Queues can not currently be created by the API. To create the queue using the Cloud SDK, use
the provided queue.yaml:

    gcloud app deploy queue.yaml

## Running the Samples

The project ID must be specified either as a command line argument using `--project-id`, or by
editing `DEFAULT_PROJECT_ID` within `task_snippets.py`.

Set the environment variables:

    export API_KEY=your-api-key
    export PROJECT_ID=my-project-id
    export LOCATION_ID=us-central1
    export QUEUE_ID=my-pull-queue # From queue.yaml
    export QUEUE_NAME=projects/$PROJECT_ID/locations/$LOCATION_ID/queues/$QUEUE_ID

View all queues:

     python pull_queue_snippets.py --api_key=$API_KEY list-queues --project_id=$PROJECT_ID --location_id=$LOCATION_ID

Create a task for a queue:

    python pull_queue_snippets.py --api_key=$API_KEY create-task --queue_name=$QUEUE_NAME

Pull and acknowledge a task:

    python pull_queue_snippets.py --api_key=$API_KEY pull-and-ack-task --queue_name=$QUEUE_NAME

Note that usually, there would be a processing step in between pulling a task and acknowledging it.
