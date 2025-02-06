# Google Cloud Platform Python Samples

Python samples for [Google Cloud Platform products][cloud].

[![Build Status][py-2.7-shield]][py-2.7-link] [![Build Status][py-3.9-shield]][py-3.9-link] [![Build Status][py-3.10-shield]][py-3.10-link] [![Build Status][py-3.11-shield]][py-3.11-link] [![Build Status][py-3.12-shield]][py-3.12-link] [![Build Status][py-3.13-shield]][py-3.13-link]

## Google Cloud Samples

Check out some of the samples found on this repository on the [Google Cloud Samples](https://cloud.google.com/docs/samples?l=python) page.

## Setup

1. Install [`pip` and `virtualenv`][cloud_python_setup] if you do not already have them.

1. Clone this repository:

    ```
    git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
    ```

1. Obtain authentication credentials.

    Create local credentials by running the following command and following the
    oauth2 flow (read more about the command [here][auth_command]):

    ```
    gcloud auth application-default login
    ```

    Read more about [Google Cloud Platform Authentication][gcp_auth].

## How to run a sample

1. Change directory to one of the sample folders, e.g. `logging/cloud-client`:

    ```
    cd logging/cloud-client/
    ```

1. Create a virtualenv. Samples are compatible with Python 3.6+.

    ```
    python3 -m venv env
    source env/bin/activate
    ```

1. Install the dependencies needed to run the samples.

    ```
    pip install -r requirements.txt
    ```

1. Run the sample:

    ```
    python snippets.py
    ```

## Contributing

Contributions welcome! See the [Contributing Guide](CONTRIBUTING.md).

[slack_badge]: https://img.shields.io/badge/slack-Google%20Cloud%20Platform-E01563.svg	
[slack_link]: https://googlecloud-community.slack.com/
[cloud]: https://cloud.google.com/
[cloud_python_setup]: https://cloud.google.com/python/setup
[auth_command]: https://cloud.google.com/sdk/gcloud/reference/beta/auth/application-default/login
[gcp_auth]: https://cloud.google.com/docs/authentication#projects_and_resources

[py-2.7-shield]: https://storage.googleapis.com/cloud-devrel-public/python-docs-samples/badges/py-2.7.svg
[py-2.7-link]: https://storage.googleapis.com/cloud-devrel-public/python-docs-samples/badges/py-2.7.html
[py-3.9-shield]: https://storage.googleapis.com/cloud-devrel-public/python-docs-samples/badges/py-3.9.svg
[py-3.9-link]: https://storage.googleapis.com/cloud-devrel-public/python-docs-samples/badges/py-3.9.html
[py-3.10-shield]: https://storage.googleapis.com/cloud-devrel-public/python-docs-samples/badges/py-310.svg
[py-3.10-link]: https://storage.googleapis.com/cloud-devrel-public/python-docs-samples/badges/py-3.10.html
[py-3.11-shield]: https://storage.googleapis.com/cloud-devrel-public/python-docs-samples/badges/py-311.svg
[py-3.11-link]: https://storage.googleapis.com/cloud-devrel-public/python-docs-samples/badges/py-3.11.html
[py-3.12-shield]: https://storage.googleapis.com/cloud-devrel-public/python-docs-samples/badges/py-3.12.svg
[py-3.12-link]: https://storage.googleapis.com/cloud-devrel-public/python-docs-samples/badges/py-3.12.html
[py-3.13-shield]: https://storage.googleapis.com/cloud-devrel-public/python-docs-samples/badges/py-3.13.svg
[py-3.13-link]: https://storage.googleapis.com/cloud-devrel-public/python-docs-samples/badges/py-3.13.html
