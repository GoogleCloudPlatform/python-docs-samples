# Import Logs from Cloud Storage

This directory contains an opinionated implementation of the Import Logs
solution that imports logs that were previously exported to Cloud Storage back
to Cloud Logging.
<!--
You can find more information about the scenario and instructions to run the
solution in [documentation].

[documentation]: (LINK-TO-REFERENCE-ARCHITECTURE-ARTICLE)-->

## Requirements

You have to grant the following permissions to a service account that you will
use with your solution:

* [Storage Object Viewer][r1] permissions to the storage bucket with exported
  logs
* [Log Writer][r2] permissions to write the logs

The service account can be the Compute Engine default [service account][sa] in
the project or it can be a custom service that will be used to run the solution.

[r1]: https://cloud.google.com/iam/docs/understanding-roles#storage.objectViewer
[r2]: https://cloud.google.com/iam/docs/understanding-roles#logging.logWriter
[sa]: https://cloud.google.com/compute/docs/access/service-accounts#default_service_account

## Launch

The solution runs on [Cloud Run][run] as a job. The following parameters are
recommended when importing a low volume of logs:

| Parameter | Value |
|---|---|
| Image URI | `us-docker.pkg.dev/cloud-devrel-public-resources/samples/import-logs-solution` |
| CPUs | `2` |
| Memory | `2Gi` |
| Task timeout | `60m` |
| Number of tasks | `1` (it is default number) |

The input arguments for the solution are set using environment variables that
have to be configured when a new Cloud Run job for the solution is created:

| Environment variable | Value |
|---|---|
| START_DATE | A string in format `MM/DD/YYYY` that defines the first day of the import range |
| END_DATE | A string in format `MM/DD/YYYY` that defines the last day of the import range |
| LOG_ID | A string that identifies the particular log to be imported. See [documentation][logid] for more details. |
| STORAGE_BUCKET_NAME | A name of the storage bucket where the exported logs are stored. |

<!--Read [documentation] for more information about Cloud Run job setup.-->

[run]: https://cloud.google.com/run/
[logid]: <https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry#FIELDS-table>

### Build

The solution uses a pre-built image. Use the following commands to build your custom image:

1. [Install Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
1. Clone the repo:

   ```bash
   git clone https://github.com/GoogleCloudPlatform/python-docs-samples/
   ```

1. Open the directory with this solution

   ```bash
   cd python-docs-samples/logging/import-logs
   ```

1. Build a container image with a name `IMAGE_NAME` and store it in the artifact registry `REGISTRY` (in the US multi-region location)
for the project ID `PROJECT_ID`:

  ```bash
  gcloud builds submit --pack image=us-docker.pkg.dev/PROJECT_ID/REGISTRY/IMAGE_NAME
  ```

  This commands [builds a container image][build] using buildpacks. Not that non-Google artifact registries are not currently supported.

> [!Note]
> Running `gcloud` command may require authentication.

[build]: https://cloud.google.com/docs/buildpacks/build-application

### Run tests with nox

```shell
nox -s lint
nox -s py-3.8
nox -s py-3.11
```
