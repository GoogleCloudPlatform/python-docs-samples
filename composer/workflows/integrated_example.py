"""An example Composer workflow integrating BigQuery, Dataflow, and GCS.
   This workflow runs a Dataflow job on a CSV file, stores the output dataset in
   a BigQuery table, performs a query on the dataset, and writes the query results
   back to a GCS bucket.

   Before starting, configure the `gcp_project` and `gcs_bucket` environment
   variables. The `gcs_ubkcet` value can be the same Composer bucket in which
   you upload this DAG.

   gcloud composer environments run composer-exercise variables -- \
       --set gcp_project [your project id]

   gcloud composer environments run composer-exercise variables -- \
       --set gcs_bucket [your gcs bucket]

   Also, be sure that you've enabled the Dataflow API for your project.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.operators.bigquery_to_gcs import BigQueryToCloudStorageOperator
from airflow.contrib.operators.dataflow_operator import DataFlowPythonOperator
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator

YESTERDAY = datetime.combine(datetime.today() - timedelta(days=1),
                             datetime.min.time())

BUCKET = Variable.get('gcs_bucket')
BQ_DATASET_NAME = 'example_dataset'
BQ_RESULT_TABLE = '{0}.{1}'.format(BQ_DATASET_NAME, 'results')

DEFAULT_ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': YESTERDAY,
    # If you'd like to test out enabling e-mail notifications on DAG
    # retries/failure, configure your environment to support email by
    # setting the SENDGRID variables and modifying the email fields below.
    'email': ['email@foobar.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'dataflow_default_options': {
        'project': Variable.get('gcp_project'),
        'stagingLocation': '{0}/{1}'.format(BUCKET, 'staging/'),
        'tempLocation': '{0}/{1}'.format(BUCKET, 'temp/'),
    }
}

with DAG('integrated_example', default_args=DEFAULT_ARGS) as dag:
  # We need to create a BigQuery dataset to store the output from Dataflow.
  # There's currently no BigQuery dataset creation operator to do this, so
  # we use a `BashOperator` catch-all operator. Notice that the
  # `create_bq_dataset_if_not_exist` command is implemented using the
  # same command that we'd use in the BigQuery command line tools.
  #
  # After this completes, a BigQuery dataset with the `BQ_DATASET_NAME`
  # should be viewable from your BigQuery dashboard.
  create_bq_dataset_if_not_exist = """
    bq ls {0}
    if [ $? -ne 0 ]; then
      bq mk {0}
    fi
  """.format(BQ_DATASET_NAME)
  CREATE_BIGQUERY_DATASET = BashOperator(
      task_id='create-bq-dataset',
      bash_command=create_bq_dataset_if_not_exist,
      dag=dag)

  # This DataFlow operator runs a Python pipeline from Apache Beam,
  # `hourly_team_score.py`, that calculates the scores of teams in batch and
  # sends the results to our BigQuery dataset.
  #
  # Optional: We use this Apache pipeline file directly by setting the py_file as
  # follows; however, if you'd like to see how the Dataflow oeprator uses local
  # Python pipeline files, copy the pipeline file (https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/complete/game/hourly_team_score.py)
  # to a directory in your bucket (we use `pipelines/`):
  #   gsutil hourly_team_score.py gs://{composer-bucket}/pipelines
  # Then, modify the `py_file` argument in the given DAG to point to the local
  # file location:
  #   py_file=`/home/airflow/gcs/pipelines/hourly_team_score`
  #
  # Notice how we feed in the data file `game_data-condensed.csv` (located in a
  # public bucket `gs://example-datasets) and point the pipeline to our BigQuery
  # dataset. As this runs (should take 3-5 minutes), you should be able to track
  # the progress in your Dataflow dashboard as a job with the prefix
  # `run-dataflow-python`.
  RUN_DATAFLOW_PYTHON = DataFlowPythonOperator(
      task_id='run-dataflow-python',
      py_file='apache_beam.examples.complete.game.hourly_team_score',
      py_options=['-m'],
      options={
          'input': 'gs://example-datasets/game_data_condensed.csv',
          'dataset': BQ_DATASET_NAME
      }
  )

  # After the Dataflow process completes, you should see an `hourly-team-score`
  # table within the `example-dataset`. We now want to filter the entries by
  # running a query on this table using the BigQuery operator below. This query
  # chooses all the teams with `total_score > 20000` from the table we just
  # generated, `example_dataset.hourly_team_score`. We write the result of this
  # query (`destination_dataset_table`) to a new table,
  # `example_dataset.results`, and set `write_disposition="WRITE_TRUNCATE" (so
  # our results will overwrite any results already existing in this table).
  # Run a query on this dataset
  RUN_BQ_QUERY = BigQueryOperator(
      task_id='bq-team-query',
      bql="""
        SELECT
          team, total_score
        FROM
          [{0}.hourly_team_score]
        WHERE
          total_score > 20000
        ORDER BY total_score
      """.format(BQ_DATASET_NAME),
      destination_dataset_table=BQ_RESULT_TABLE,
      write_disposition='WRITE_TRUNCATE'   # Overwrites existing table
  )

  # Finally, we export the result table back to a GCS bucket in a .csv file
  # format, using the `BigQueryToCloudStorageOperator`.
  BQ_TO_GCS = BigQueryToCloudStorageOperator(
      task_id='bq-to-gcs',
      source_project_dataset_table=BQ_RESULT_TABLE,
      # Destination is of format 'bucket/output/dataset_result.csv'
      destination_cloud_storage_uris=['{0}/{1}{2}{3}'.format(
          BUCKET, 'output/', BQ_RESULT_TABLE, '.csv')],
      export_format='CSV'
  )

  # This chaining lets Airflow know about the order of execution.
  CREATE_BIGQUERY_DATASET >> RUN_DATAFLOW_PYTHON >> RUN_BQ_QUERY >> BQ_TO_GCS

  # After this DAG completes, the result should be uploaded in CSV format to the
  # output/directory of your GCS bucket.
