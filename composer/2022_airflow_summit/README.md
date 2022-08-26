# Airflow Summit 2022 Sample DAGs

DAGs in this directory are part of the curriculum for the
[Cloud Composer Workshop](https://airflowsummit.org/sessions/2022/cloud-composer-workshop/)
at the 2022 Airflow summit. Be sure to
[register](https://ti.to/airflowsummit/2022-workshops) and join us there!  

## parallel_work

Running a number of tasks in parallel showcases autoscaling in a Cloud Composer environment.

## data_analytics_dag

Runs a basic Data Analytics workflow using BigQuery, Cloud Storage, and Dataproc Serverless. More detailed documentation can be found for this DAG [in the Composer documentation](https://cloud.google.com/composer/docs/data-analytics-googlecloud)

### dataproc_expansion

This directory has a DAG similar to the data analytics DAG but includes a more complicated data processing step with Dataproc.

## retries

Showcasing how retries can be used when API calls fail.

## bigquery_permissions

Demo showing error message when there are missing permissions to query a BigQuery dataset.
