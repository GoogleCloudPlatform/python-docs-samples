# Python + Flask + SparkPost Example on Google App Engine Standard

> [SparkPost][sparkpost]—Modern email delivery services built for developers, by developers.
>
> – sparkpost.com

This sample app demonstrates how to send email with Python and [python-sparkpost](https://github.com/SparkPost/python-sparkpost) on the Google App Engine standard environment.

You can also [read the SparkPost documentation here](https://developers.sparkpost.com/).

### Prerequisites

 - a [Google Cloud Platform](https://cloud.google.com/) account
 - the [Google Cloud SDK](https://cloud.google.com/sdk/) installed and configured

### Setup

1. Sign up for a SparkPost account [here](https://app.sparkpost.com/sign-up).

1. Create an API key with *Transmissions: read/write* privilege [here](https://app.sparkpost.com/account/credentials).

1. Add your API key to `app.yaml`.

1. Install the app's dependencies:
    ```sh
    mkdir lib
    pip install -r requirements -t lib
    ```

### Running Locally

1. Run the app using the Google Cloud SDK dev app server:
    ```sh
    $GCLOUD_SDK/bin/dev_appserver.py app.yaml
    ```

1. Visit the app in your browser: [http://localhost:8080/](http://localhost:8080/)

### Deploying To Google App Engine

1. Deploy the app and dependencies to your Google Cloud project:
    ```sh
    gcloud app deploy
    ```

1. Visit the app in your browser: 
    ```sh
    gcloud app browse
    ```

### Running The Tests

```sh
pip install pytest responses flaky
pytest .
```

[sparkpost]: https://www.sparkpost.com/

