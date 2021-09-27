# Cloud Run File System Sample

This sample shows how to create a service that mounts a Filestore
instance as a network file system.

# Tutorial
See our [Using Filestore with Cloud Run tutorial](https://cloud.google.com/run/docs/tutorials/network-filesystems) for instructions for setting up and deploying this sample application.

## Run with [GCS Fuse][fuse]
[`gcsfuse`][git] is a user-space file system for interacting with Google Cloud Storage.

[Create a GCS bucket][create] or reuse an existing. Set as environment variable:
```
export BUCKET=<YOUR_BUCKET>
```

Set project Id as an environment variable:
```
export PROJECT_ID=<YOUR_PROJECT_ID>
```

Build the Docker container specifying the Fuse Dockerfile:
```
docker build -t gcr.io/$PROJECT_ID/gcsfuse -f gcsfuse.Dockerfile .
```

Push to Container Registry (See [Setting up authentication for Docker][auth]):
```
docker push gcr.io/$PROJECT_ID/gcsfuse
```

Deploy to Cloud Run
```
gcloud alpha run deploy gcsfuse \
    --image gcr.io/$PROJECT_ID/gcsfuse \
    --execution-environment gen2 \
    --update-env-vars BUCKET=$BUCKET \
    --allow-unauthenticated
```

[create]: https://cloud.google.com/storage/docs/creating-buckets
[fuse]: https://cloud.google.com/storage/docs/gcs-fuse
[git]: https://github.com/GoogleCloudPlatform/gcsfuse
[auth]: https://cloud.google.com/artifact-registry/docs/docker/authentication