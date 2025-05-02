<img src="https://avatars2.githubusercontent.com/u/2810941?v=3&s=96" alt="Google Cloud logo" title="Google Cloud" align="right" height="96" width="96"/>

# Cloud Workflows Quickstart – Python

This sample shows how to execute Cloud Workflows and wait for the result
of a workflow execution using the Python client libraries.

## Setup

1. Deploy the workflow, `myFirstWorkflow`:

    1. Copy the YAML from this file: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/workflows/cloud-client/myFirstWorkflow.workflows.yaml
    1. Paste the YAML into a file called `myFirstWorkflow.workflows.yaml`.
    1. Run the command: `gcloud workflows deploy myFirstWorkflow --source myFirstWorkflow.workflows.yaml`

## Run the Quickstart

Install [`pip`][pip] and [`virtualenv`][virtualenv] if you do not already have them.

For more information, refer to the
[Python Development Environment Setup Guide][setup] for Google Cloud.

1. Create a virtualenv. Samples are compatible with Python 3.9+.

    ```sh
    virtualenv env
    source env/bin/activate
    ```

1. Install the dependencies needed to run the samples.

    ```sh
    pip install -r requirements.txt
    ```

1. Start the application, setting your project name in an environment variable, `GOOGLE_CLOUD_PROJECT`:

    ```sh
    export GOOGLE_CLOUD_PROJECT=your-project-id
    python main.py
    ```

1. Observe the results:

    In `stdout`, you should see a JSON response from your workflow like the following,
    depending on the current weekday in Amsterdam.

    ```json
    ["Wednesday","Wednesday Night Wars","Wednesday 13","Wednesday Addams","Wednesday Campanella","Wednesdayite","Wednesday Martin","Wednesday Campanella discography","Wednesday Night Hockey (American TV program)","Wednesday Morning, 3 A.M."]
    ```

[prereq]: ../README.md#prerequisites
[setup]: https://cloud.google.com/python/setup
[pip]: https://pip.pypa.io/
[virtualenv]: https://virtualenv.pypa.io/
