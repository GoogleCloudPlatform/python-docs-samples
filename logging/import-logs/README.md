# Import Logs from Cloud Storage

This directory contains an opinionated implementation of the Import Logs
solution that imports logs that were previously exported to Cloud Storage back
to Cloud Logging.
<!--
You can find more information about the scenario and instructions to run the
solution in [documentation].

[documentation]: (LINK-TO-REFERENCE-ARCHITECTURE-ARTICLE)-->

All logs will be imported to the project that runs Cloud Run job.
Alternatively you can explicitly configure the project ID where you want logs to be imported.
The logs will be imported with log name `imported_logs`.
It means that the `logName` field of the imported logs will be:

```text
projects/PROJECT_ID/logs/imported_logs
```

where `PROJECT_ID` is the project ID of the project where you import the logs.

The original log name will be stored in the user labels under the key `original_logName` (mind the casing).

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
| PROJECT_ID | (Optional) If you want to explicitly define destination project other than one your import job is deployed |

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

## Importing log entries with timestamps older than 30 days

The incoming log entries that are older than default retention period (i.e. 30 days) are not ingested.
You can see [documentation][retention] for more details. The code takes a safety margin of an extra day
to prevent importing old logs that cannot be ingested.
To import the older logs you have to modified the [current] code by performing the following modifications:

* comment the fencing condition [lines][code1]:

  <https://github.com/GoogleCloudPlatform/python-docs-samples/blob/86f12a752a4171e137adaa855c7247be9d5d39a2/logging/import-logs/main.py#L81-L83>

* uncomment [2 lines][code2] to keep the original timestamp as a user label and to reset the `timestamp` field of the imported log entries.

> [!IMPORTANT]  
>
> 1. To query the imported logs by timestamp you will have to use the label `original_timestamp` instead of the `timestamp` field.
> 1. If the same log entry is imported multiple times, the query response may include more than one line.

After applying the changes, [build](#build) a custom container image and use it when creating an import job.

[retention]: https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry#FIELDS.timestamp
[current]: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/e2709a218072c86ec1a9b9101db45057ebfdbff0/logging/import-logs/main.py
[code1]: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/86f12a752a4171e137adaa855c7247be9d5d39a2/logging/import-logs/main.py#L81-L83
[code2]: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/86f12a752a4171e137adaa855c7247be9d5d39a2/logging/import-logs/main.py#L188-L189
