## NDB Overview Sample

This is a sample app for Google App Engine that exercises the [NDB Python API](https://cloud.google.com/appengine/docs/python/ndb/).

See our other [Google Cloud Platform github
repos](https://github.com/GoogleCloudPlatform) for sample applications and
scaffolding for other python frameworks and use cases.

## Run Locally
1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/), including the [gcloud tool](https://cloud.google.com/sdk/gcloud/), and [gcloud app component](https://cloud.google.com/sdk/gcloud-app).
2. Setup the gcloud tool.

   ```
   gcloud components update app
   gcloud auth login
   gcloud config set project <your-app-id>
   ```
   You don't need a valid app-id to run locally, but will need a valid id to deploy below.

1. Clone this repo.

   ```
   git clone https://github.com/GoogleCloudPlatform/datastore-pthon-samples.git
   cd datastore-python-samples/ndb-overview
   ```
1. Run this project locally from the command line.

   ```
   gcloud preview app run ./
   ```

1. Visit the application at [http://localhost:8080](http://localhost:8080).

## Deploying

1. Use the [Cloud Developer Console](https://console.developer.google.com)  to create a project/app id. (App id and project id are identical)
2. Configure gcloud with your app id.

   ```
   gcloud config set project <your-app-id>
   ```
1. Use the [Admin Console](https://appengine.google.com) to view data, queues, and other App Engine specific administration tasks.
1. Use gcloud to deploy your app.

   ```
   gcloud preview app deploy ./
   ```

1. Congratulations!  Your application is now live at your-app-id.appspot.com

## Contributing changes

* See [CONTRIBUTING.md](../../CONTRIBUTING.md)

## Licensing

* See [LICENSE](../../LICENSE)
