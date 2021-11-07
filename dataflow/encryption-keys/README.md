# Using customer-managed encryption keys

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=dataflow/encryption-keys/README.md)

This sample demonstrate how to use
[cryptographic encryption keys](https://cloud.google.com/kms/)
for the I/O connectors in an
[Apache Beam](https://beam.apache.org) pipeline.
For more information, see the
[Using customer-managed encryption keys](https://cloud.google.com/dataflow/docs/guides/customer-managed-encryption-keys)
docs page.

## Before you begin

Follow the
[Getting started with Google Cloud Dataflow](../README.md)
page, and make sure you have a Google Cloud project with billing enabled
and a *service account JSON key* set up in your `GOOGLE_APPLICATION_CREDENTIALS` environment variable.
Additionally, for this sample you need the following:

1. [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery,cloudkms.googleapis.com):
   BigQuery and Cloud KMS API.

1. Create a Cloud Storage bucket.

   ```sh
   export BUCKET=your-gcs-bucket
   gsutil mb gs://$BUCKET
   ```

1. [Create a symmetric key ring](https://cloud.google.com/kms/docs/creating-keys).
   For best results, use a [regional location](https://cloud.google.com/kms/docs/locations).
   This example uses a `global` key for simplicity.

   ```sh
   export KMS_KEYRING=samples-keyring
   export KMS_KEY=samples-key

   # Create a key ring.
   gcloud kms keyrings create $KMS_KEYRING --location global

   # Create a key.
   gcloud kms keys create $KMS_KEY --location global \
     --keyring $KMS_KEYRING --purpose encryption
   ```

   > *Note:* Although you can destroy the
   > [*key version material*](https://cloud.google.com/kms/docs/destroy-restore),
   > you [cannot delete keys and key rings](https://cloud.google.com/kms/docs/object-hierarchy#lifetime).
   > Key rings and keys do not have billable costs or quota limitations,
   > so their continued existence does not impact costs or production limits.

1. Grant Encrypter/Decrypter permissions to the *Dataflow*, *Compute Engine*, and *BigQuery*
   [service accounts](https://cloud.google.com/iam/docs/service-accounts).
   This grants your Dataflow, Compute Engine and BigQuery service accounts the
   permission to encrypt and decrypt with the CMEK you specify.
   The Dataflow workers use these service accounts when running the pipeline,
   which is different from the *user* service account used to start the pipeline.

   ```sh
   export PROJECT=$(gcloud config get-value project)
   export PROJECT_NUMBER=$(gcloud projects list --filter $PROJECT --format "value(PROJECT_NUMBER)")

   # Grant Encrypter/Decrypter permissions to the Dataflow service account.
   gcloud projects add-iam-policy-binding $PROJECT \
     --member serviceAccount:service-$PROJECT_NUMBER@dataflow-service-producer-prod.iam.gserviceaccount.com \
     --role roles/cloudkms.cryptoKeyEncrypterDecrypter

   # Grant Encrypter/Decrypter permissions to the Compute Engine service account.
   gcloud projects add-iam-policy-binding $PROJECT \
     --member serviceAccount:service-$PROJECT_NUMBER@compute-system.iam.gserviceaccount.com \
     --role roles/cloudkms.cryptoKeyEncrypterDecrypter

   # Grant Encrypter/Decrypter permissions to the BigQuery service account.
   gcloud projects add-iam-policy-binding $PROJECT \
     --member serviceAccount:bq-$PROJECT_NUMBER@bigquery-encryption.iam.gserviceaccount.com \
     --role roles/cloudkms.cryptoKeyEncrypterDecrypter
   ```

1. Clone the `python-docs-samples` repository.

   ```sh
   git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git
   ```

1. Navigate to the sample code directory.

   ```sh
   cd python-docs-samples/dataflow/encryption-keys
   ```

1. Create a virtual environment and activate it.

   ```sh
   virtualenv env
   source env/bin/activate
   ```

   > Once you are done, you can deactivate the virtualenv and go back to your global Python environment by running `deactivate`.

1. Install the sample requirements.

   ```sh
   pip install -U -r requirements.txt
   ```

## BigQuery KMS Key example

* [bigquery_kms_key.py](bigquery_kms_key.py)

The following sample gets some data from the
[NASA wildfires public BigQuery dataset](https://console.cloud.google.com/bigquery?p=bigquery-public-data&d=nasa_wildfire&t=past_week&page=table)
using a customer-managed encryption key, and dump that data into the specified `output_bigquery_table`
using the same customer-managed encryption key.

Make sure you have the following variables set up:

```sh
# Set the project ID, GCS bucket and KMS key.
export PROJECT=$(gcloud config get-value project)
export BUCKET=your-gcs-bucket

# Set the region for the Dataflow job.
# https://cloud.google.com/compute/docs/regions-zones/
export REGION=us-central1

# Set the KMS key ID.
export KMS_KEYRING=samples-keyring
export KMS_KEY=samples-key
export KMS_KEY_ID=$(gcloud kms keys list --location global --keyring $KMS_KEYRING --filter $KMS_KEY --format "value(NAME)")

# Output BigQuery dataset and table name.
export DATASET=samples
export TABLE=dataflow_kms
```

Create the BigQuery dataset where the output table resides.

```sh
# Create the BigQuery dataset.
bq mk --dataset $PROJECT:$DATASET
```

To run the sample using the Dataflow runner.

```sh
python bigquery_kms_key.py \
  --output_bigquery_table $PROJECT:$DATASET.$TABLE \
  --kms_key $KMS_KEY_ID \
  --project $PROJECT \
  --runner DataflowRunner \
  --temp_location gs://$BUCKET/samples/dataflow/kms/tmp \
  --region $REGION
```

> *Note:* To run locally you can omit the `--runner` command line argument and it defaults to the `DirectRunner`.

You can check your submitted Cloud Dataflow jobs in the
[GCP Console Dataflow page](https://console.cloud.google.com/dataflow) or by using `gcloud`.

```sh
gcloud dataflow jobs list
```

Finally, check the contents of the BigQuery table.

```sh
bq query --use_legacy_sql=false "SELECT * FROM `$PROJECT.$DATASET.$TABLE`"
```

## Cleanup

To avoid incurring charges to your GCP account for the resources used:

```sh
# Remove only the files created by this sample.
gsutil -m rm -rf "gs://$BUCKET/samples/dataflow/kms"

# [optional] Remove the Cloud Storage bucket.
gsutil rb gs://$BUCKET

# Remove the BigQuery table.
bq rm -f -t $PROJECT:$DATASET.$TABLE

# [optional] Remove the BigQuery dataset and all its tables.
bq rm -rf -d $PROJECT:$DATASET

# Revoke Encrypter/Decrypter permissions to the Dataflow service account.
gcloud projects remove-iam-policy-binding $PROJECT \
  --member serviceAccount:service-$PROJECT_NUMBER@dataflow-service-producer-prod.iam.gserviceaccount.com \
  --role roles/cloudkms.cryptoKeyEncrypterDecrypter

# Revoke Encrypter/Decrypter permissions to the Compute Engine service account.
gcloud projects remove-iam-policy-binding $PROJECT \
  --member serviceAccount:service-$PROJECT_NUMBER@compute-system.iam.gserviceaccount.com \
  --role roles/cloudkms.cryptoKeyEncrypterDecrypter

# Revoke Encrypter/Decrypter permissions to the BigQuery service account.
gcloud projects remove-iam-policy-binding $PROJECT \
  --member serviceAccount:bq-$PROJECT_NUMBER@bigquery-encryption.iam.gserviceaccount.com \
  --role roles/cloudkms.cryptoKeyEncrypterDecrypter
```
