## Running locally

Refer to the [top-level README](../README.md) for instructions on running and deploying.

When running locally, you can use the [Google Cloud SDK](https://cloud.google.com/sdk) to provide authentication to use Google Cloud APIs:

    $ gcloud init

Install dependencies, preferably with a virtualenv:

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt

Start your application:

    $ python main.py

## Deploying on App Engine

Deploy using `gcloud`:

    gcloud app deploy

You can now access the application at `https://your-app-id.appspot.com`.
