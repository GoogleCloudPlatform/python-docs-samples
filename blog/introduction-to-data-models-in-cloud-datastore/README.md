# Introduction to data models in Cloud Datastore

This sample code is used in [this blog post](). It demonstrates two data models
using [Google Cloud Datstore](https://cloud.google.com/datastore).

## Prerequisites

1. Create project with billing enabled on the [Google Developers Console](https://console.developers.google.com)
2. [Enable the Datastore API](https://console.developers.google.com/project/_/apiui/apiview/datastore/overview).
3. Install the [Google Cloud SDK](https://cloud.google.com/sdk) and be sure to run ``gcloud auth``.


## Running the samples

Install any dependencies:

    pip install -r requirements.txt

And run the samples:

    python blog.py your-project-id
    python wiki.py your-project-id
