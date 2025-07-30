# Cloud Run Hello World Streamlit Sample

This sample shows how to deploy a Hello World Streamlit application to Cloud Run.

[![Run in Google Cloud][run_img]][run_link]

[run_img]: https://storage.googleapis.com/cloudrun/button.svg
[run_link]: https://console.cloud.google.com/cloudshell/editor?shellonly=true&cloudshell_image=gcr.io/cloudrun/button&cloudshell_git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&cloudshell_working_dir=run/helloworld-streamlit

## Deploy

```sh
# Ensure you have set your Google Cloud Project ID
gcloud config set project <PROJECT_ID>

# Deploy to Cloud Run
gcloud run deploy helloworld-streamlit --source .
```

For more details on how to work with this sample read the [Python Cloud Run Samples README](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/run)
