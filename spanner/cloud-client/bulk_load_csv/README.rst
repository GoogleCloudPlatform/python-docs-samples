Google Cloud Spanner: Bulk Loading From CSV Python Sample
===============

``Google Cloud Spanner`` is a highly scalable, transactional, managed, NewSQL database service.
  Cloud Spanner solves the need for a horizontally-scaling database with consistent global transactions and SQL semantics.

This application demonstrates how to load data from a csv file into a Cloud
Spanner database.

Pre-requisuite
-----------------------
Create a database in your cloud spanner instance using the schema in the folder.

To run sample
-----------------------

 $ python import.py instance_id database_id

positional arguments:
  instance_id           Your Cloud Spanner instance ID.
  database_id           Your Cloud Spanner database ID.

{is_bool_null,divide_chunks,insert_data}
is_bool_null    This function convertes the boolean values in the dataset from strings
                to boolean data types.
                It also converts the string Null to a None data type indicating an empty
                cell.
divide_chunks   This function divides the csv file into chunks so that the mutations will commit
                every 500 rows.
insert_data     This function iterates over the list of files belonging to the dataset and,
                writes each line into cloud spanner using the batch mutation function.