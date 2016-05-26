# Cloud Logging v2 API Samples

Sample command-line programs for retrieving Google Logging API V2 data.

`logs_api.py` is a simple command-line program to demonstrate writing to a log,
listing its entries to view it, then deleting it via CLI operations.

`export_logs_api.py` demonstrates how to interact with Logging sinks, which can send
logs to Google Cloud Storage, Cloud Pub/Sub, or BigQuery. In this example
we use Google Cloud Storage. It similarly exposes a CLI to run these operations.

## Prerequisites to run locally:


* A Google Cloud Project

Go to the [Google Cloud Console](https://console.cloud.google.com) to create
 a project. Take note of the project ID, which is sometimes but not always
 the same as your given name for a project.

To run `export.py`, you will also need a Google Cloud Storage Bucket. 

    gsutil mb gs://[YOUR_PROJECT_ID]

You must add Cloud Logging as an owner to the bucket. To do so, add cloud-logs@google.com as
an owner to the bucket. See the [exportings logs](https://cloud.google.com/logging/docs/export/configure_export#configuring_log_sinks)
docs for complete details. 

# Set Up Your Local Dev Environment
To install, run the following commands. If you want to use  [virtualenv](https://virtualenv.readthedocs.org/en/latest/)
(recommended), run the commands within a virtualenv.

Create local credentials by running the following command and following the oauth2 flow:

    gcloud beta auth application-default login

To run the list_logs example

    python logs_api.py --project_id=<YOUR-PROJECT-ID> write_entry "hello world"
    python logs_api.py --project_id=<YOUR-PROJECT-ID> list_entries
    python logs_api.py --project_id=<YOUR-PROJECT-ID> delete_logger
    

The `exports_logs_api.py` samples requires a Cloud bucket that has added cloud-logs@google.com 
as an owner. See:

https://cloud.google.com/logging/docs/export/configure_export#setting_product_name_short_permissions_for_writing_exported_logs
    
    python export_logs_api.py --project_id=YOUR_PROJECT_ID create_sink \  
        --destination_bucket=YOUR_BUCKET
        
    python export_logs_api.py --project_id=YOUR_PROJECT_ID update_sink\  
        --destination_bucket=YOUR_BUCKET
                
    python export_logs_api.py --project_id=YOUR_PROJECT_ID list_sinks
              
    python export_logs_api.py --project_id=YOUR_PROJECT_ID delete_sink \  
              --destination_bucket=YOUR_BUCKET


## Running on GCE, GAE, or other environments

See our [Cloud Platform authentication guide](https://cloud.google.com/docs/authentication).

