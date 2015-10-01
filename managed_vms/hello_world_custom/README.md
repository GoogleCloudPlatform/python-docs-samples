## Google App Engine Managed VMs Python Custom Runtime Hello World

This sample demonstrates using [Python on Google App Engine Managed VMs](https://cloud.google.com/appengine/docs/python/managed-vms/hello-world) with a custom runtime.

This sample does not use the standard App Engine python runtime, but instead uses
a custom runtime. The custom runtime ensures that any requirements defined
in `requirements.txt` are automatically installed.

### Running & deploying the sample

To run the sample locally, use a virtualenv:

    $ virtualenv env
    $ source env/bin/activate.sh
    $ pip install -r requirements.txt
    $ python main.py

To deploy the sample, use the [Google Cloud SDK](https://cloud.google.com/sdk)

    $ gcloud preview app deploy app.yaml
