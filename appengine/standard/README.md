# Google App Engine Samples

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/standard/README.md

This section contains samples for [Google App Engine](https://cloud.google.com/appengine). Most of these samples have associated documentation that is linked
within the docstring of the sample itself.

## Running the samples locally

1. Download the [Google App Engine Python SDK](https://cloud.google.com/appengine/downloads) for your platform.
2. Many samples require extra libraries to be installed. If there is a `requirements.txt`, you will need to install the dependencies with [`pip`](pip.readthedocs.org).

        pip install -t lib -r requirements.txt

3. Use `dev_appserver.py` to run the sample:

        dev_appserver.py app.yaml

4. Visit `http://localhost:8080` to view your application.

Some samples may require additional setup. Refer to individual sample READMEs.

## Deploying the samples

1. Download the [Google App Engine Python SDK](https://cloud.google.com/appengine/downloads) for your platform.
2. Many samples require extra libraries to be installed. If there is a `requirements.txt`, you will need to install the dependencies with [`pip`](pip.readthedocs.org).

        pip install -t lib -r requirements.txt

3. Use `gcloud` to deploy the sample, you will need to specify your Project ID and a version number:

        gcloud app deploy --project your-app-id -v your-version

4. Visit `https://your-app-id.appspot.com` to view your application.

## Additional resources

For more information on App Engine:

> https://cloud.google.com/appengine

For more information on Python on App Engine:

> https://cloud.google.com/appengine/docs/python
