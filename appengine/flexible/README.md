## Google App Engine Flexible Environment Python Samples

These are samples for using Python on Google App Engine Flexible Environment. These samples are typically referenced from the [docs](https://cloud.google.com/appengine/docs).

See our other [Google Cloud Platform github repos](https://github.com/GoogleCloudPlatform) for sample applications and
scaffolding for other frameworks and use cases.

## Run Locally

Some samples have specific instructions. If there is a README in the sample folder, pleaese refer to it for any additional steps required to run the sample.

In general, the samples typically require:

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/), including the [gcloud tool](https://cloud.google.com/sdk/gcloud/), and [gcloud app component](https://cloud.google.com/sdk/gcloud-app).

2. Setup the gcloud tool. This provides authentication to Google Cloud APIs and services.

   ```
   gcloud init
   ```

3. Clone this repo.

   ```
   git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
   cd python-docs-samples/appengine/flexible
   ```

4. Open a sample folder, create a virtualenv, install dependencies, and run the sample:

   ```
   cd hello-world
   virtualenv env
   source env/bin/activate
   pip install -r requirements.txt
   python main.py
   ```

5. Visit the application at [http://localhost:8080](http://localhost:8080).


## Deploying

Some samples in this repositories may have special deployment instructions. Refer to the readme in the sample directory.

1. Use the [Google Developers Console](https://console.developer.google.com)  to create a project/app id. (App id and project id are identical)

2. Setup the gcloud tool, if you haven't already.

   ```
   gcloud init
   ```

3. Use gcloud to deploy your app.

   ```
   gcloud app deploy
   ```

4. Congratulations!  Your application is now live at `your-app-id.appspot.com`

## Contributing changes

* See [CONTRIBUTING.md](../CONTRIBUTING.md)

## Licensing

* See [LICENSE](../LICENSE)
