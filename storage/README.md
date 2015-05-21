## Python Samples for Google Cloud Storage

Two samples:

1. ``list_objects.py`` lists objects in a bucket.
2. ``compose_objects.py`` composes objects together to create another.

See the docstring for each sample for usage, or run the sample for the help text.

### Setup

Before running the samples, you'll need the Google Cloud SDK in order to setup authentication.

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/), including the [gcloud tool](https://cloud.google.com/sdk/gcloud/), and [gcloud app component](https://cloud.google.com/sdk/gcloud-app).
2. Setup the gcloud tool.

   ```
   gcloud components update app
   gcloud auth login
   gcloud config set project <your-app-id>
   ```

You will also need to install the dependencies using [pip](https://pypi.python.org/pypi/pip):

```
pip install -r requirements.txt
```
