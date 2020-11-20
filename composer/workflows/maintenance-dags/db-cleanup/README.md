# Airflow DB Cleanup

A maintenance workflow that you can deploy into Airflow to periodically clean out the DagRun, TaskInstance, Log, XCom, Job DB and SlaMiss entries to avoid having too much data in your Airflow MetaStore.

## Authors

The DAG is a fork of [teamclairvoyant repository.](https://github.com/teamclairvoyant/airflow-maintenance-dags/tree/master/db-cleanup)

## Usage

1. Update the global variables (SCHEDULE_INTERVAL, DAG_OWNER_NAME, ALERT_EMAIL_ADDRESSES and ENABLE_DELETE) in the DAG with the desired values

2. Modify the DATABASE_OBJECTS list to add/remove objects as needed. Each dictionary in the list features the following parameters:
    - airflow_db_model: Model imported from airflow.models corresponding to a table in the airflow metadata database
    - age_check_column: Column in the model/table to use for calculating max date of data deletion
    - keep_last: Boolean to specify whether to preserve last run instance
        - keep_last_filters: List of filters to preserve data from deleting during clean-up, such as DAG runs where the external trigger is set to 0.
        - keep_last_group_by: Option to specify column by which to group the database entries and perform aggregate functions.

3. Create and Set the following Variables in the Airflow Web Server (Admin -> Variables)

    - airflow_db_cleanup__max_db_entry_age_in_days - integer - Length to retain the log files if not already provided in the conf. If this is set to 30, the job will remove those files that are 30 days old or older.

4. Put the DAG in your gcs bucket.
