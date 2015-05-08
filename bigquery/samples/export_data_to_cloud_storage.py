from samples.utils import get_service, poll_job
import uuid


# [START export_table]
def export_table(service, cloud_storage_path,
                 projectId, datasetId, tableId,
                 num_retries=5):
    # Generate a unique job_id so retries
    # don't accidentally duplicate export
    job_data = {
            'jobReference': {
                    'projectId': projectId,
                    'jobId': str(uuid.uuid4())
                    },
            'configuration': {
                    'extract': {
                            'sourceTable': {
                                    'projectId': projectId,
                                    'datasetId': datasetId,
                                    'tableId': tableId,
                                    },
                            'destinationUris': [cloud_storage_path],
                            }
                    }
            }
    return service.jobs().insert(
        projectId=projectId,
        body=job_data).execute(num_retries=num_retries)
# [END export_table]


# [START run]
def run(cloud_storage_path,
        projectId, datasetId, tableId,
        num_retries, interval):

    bigquery = get_service()
    resource = export_table(bigquery, cloud_storage_path,
                            projectId, datasetId, tableId, num_retries)
    poll_job(bigquery,
             resource['jobReference']['projectId'],
             resource['jobReference']['jobId'],
             interval,
             num_retries)
# [END run]


# [START main]
def main():
    projectId = raw_input("Enter the project ID: ")
    datasetId = raw_input("Enter a dataset ID: ")
    tableId = raw_input("Enter a table name to copy: ")
    cloud_storage_path = raw_input(
            "Enter a Google Cloud Storage URI: ")
    interval = raw_input(
            "Enter how often to poll the job (in seconds): ")
    num_retries = raw_input(
            "Enter the number of retries in case of 500 error: ")

    run(cloud_storage_path,
        projectId, datasetId, tableId,
        num_retries, interval)

    print 'Done exporting!'
# [END main]
