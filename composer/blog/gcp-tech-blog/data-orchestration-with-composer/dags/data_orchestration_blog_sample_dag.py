from airflow.utils import dates
from airflow import models
from airflow.hooks.base_hook import BaseHook
from airflow.utils.state import State
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.google.cloud.operators.dataflow import DataflowTemplatedJobStartOperator
from airflow.providers.google.cloud.operators.gcs import GCSDeleteBucketOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator

BUCKET_NAME = models.Variable.get("bucket_name")
FILE_NAME = models.Variable.get("file_name")
BQ_SQL_STRING = models.Variable.get("bq_sql_string")

def on_failure_callback(context):
    ti = context.get('task_instance')
    slack_msg = """
            :red_circle: Task Failed. 
            *Task*: {task}  
            *Dag*: {dag} 
            *Execution Time*: {exec_date}  
            *Log Url*: {log_url} 
            """.format(
            task=ti.task_id,
            dag=ti.dag_id,
            log_url=ti.log_url,
            exec_date=context.get('execution_date'),
        )
    slack_webhook_token = BaseHook.get_connection('slack_connection').password
    slack_error = SlackWebhookOperator(
        task_id='post_slack_error',
        http_conn_id='slack_connection',
        channel='#airflow-alerts',
        webhook_token=slack_webhook_token,
        message=slack_msg)
    slack_error.execute(context)

with models.DAG(
    'transform-crm-workload',
    schedule_interval=None,
    start_date=dates.days_ago(0),    
    default_args={ 'on_failure_callback': on_failure_callback}
) as crm_workflow_dag:

    validate_file_exists = GCSObjectExistenceSensor(
        task_id="validate_file_exists",
        bucket=BUCKET_NAME,
        object=FILE_NAME
    )

    start_dataflow_job = DataflowTemplatedJobStartOperator(
        task_id="start-dataflow-template-job",
        job_name='crm_wordcount',
        template='gs://dataflow-templates/latest/Word_Count',
        parameters={
            'inputFile': "gs://{bucket}/{filename}".format(bucket=BUCKET_NAME, filename=FILE_NAME),
            'output': "gs://{bucket}/output".format(bucket=BUCKET_NAME)}
    )

    execute_bigquery_sql = BigQueryCheckOperator(
        task_id='execute_bigquery_sql',
        sql=BQ_SQL_STRING,
        use_legacy_sql=False
    )

    delete_bucket = GCSDeleteBucketOperator(
        task_id="delete_bucket",
        bucket_name=BUCKET_NAME
    ) 

    validate_file_exists >> start_dataflow_job >> execute_bigquery_sql >> delete_bucket

if __name__ == "__main__":
    crm_workflow_dag.clear(dag_run_state=State.NONE)
    crm_workflow_dag.run()
