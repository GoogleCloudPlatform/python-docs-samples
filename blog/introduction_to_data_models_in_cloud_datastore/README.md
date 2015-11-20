# Introduction to data models in Cloud Datastore

This sample code is used in [this blog post](http://googlecloudplatform.blogspot.com/2015/08/Introduction-to-data-models-in-Cloud-Datastore.html). It demonstrates two data models
using [Google Cloud Datastore](https://cloud.google.com/datastore).

## Prerequisites

1. Create project with billing enabled on the [Google Developers Console](https://console.developers.google.com)

2. [Enable the Datastore API](https://console.developers.google.com/project/_/apiui/apiview/datastore/overview).

3. Install the [Google Cloud SDK](https://cloud.google.com/sdk) and be sure to run ``gcloud init``.


## Running the samples

Install dependencies from `requirements.txt`:

    pip install -r requirements.txt

And run the samples:

    python blog.py your-project-id
    python wiki.py your-project-id
