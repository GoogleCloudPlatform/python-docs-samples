<img src="https://avatars2.githubusercontent.com/u/2810941?v=3&s=96" alt="Google
Cloud Platform logo" title="Google Cloud Platform" align="right" height="96"
width="96"/>

# Google Cloud Container Analysis Samples


Container Analysis scans container images stored in Container Registry for vulnerabilities.
Continuous automated analysis of containers keep you informed about known vulnerabilities so 
that you can review and address issues before deployment.

Additionally, third-party metadata providers can use Container Analysis to store and 
retrieve additional metadata for their customers' images, such as packages installed in an image.


## Description

These samples show how to use the [Google Cloud Container Analysis Client Library](https://cloud.google.com/container-registry/docs/reference/libraries).

## Build and Run
1.  **Enable APIs** 
    - [Enable the Container Analysis API](https://console.cloud.google.com/flows/enableapi?apiid=containeranalysis.googleapis.com)
    and create a new project or select an existing project.
1.  **Install and Initialize Cloud SDK**
    - Follow instructions from the available [quickstarts](https://cloud.google.com/sdk/docs/quickstarts)
1. **Authenticate with GCP**
    - Typically, you should authenticate using a [service account key](https://cloud.google.com/docs/authentication/getting-started)
1.  **Clone the repo** and cd into this directory

    ```
    git clone https://github.com/GoogleCloudPlatform/python-docs-samples
    cd python-docs-samples
    ```

1. **Set Environment Variables**

    ```
    export GCLOUD_PROJECT="YOUR_PROJECT_ID"
    ```

1. **Run Tests**

    ```
    nox -s "py36(sample='./containeranalysis')"
    ```

## Contributing changes

* See [CONTRIBUTING.md](../../CONTRIBUTING.md)

## Licensing

* See [LICENSE](../../LICENSE)

