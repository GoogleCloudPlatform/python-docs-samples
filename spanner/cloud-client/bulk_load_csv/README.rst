Google Cloud Spanner: Bulk Loading From CSV Python Sample
===============
 
``Google Cloud Spanner`` is a highly scalable, transactional, managed, NewSQL database service.
  Cloud Spanner solves the need for a horizontally-scaling database with consistent global transactions and SQL semantics.
 
This application demonstrates how to load data from a csv file into a Cloud
Spanner database.
 
The data contained in the csv files is sourced from the "Hacker News - Y Combinator" Bigquery `public dataset`_.
 
.. _public dataset :
    https://cloud.google.com/bigquery/public-data/
 
Pre-requisuite
-----------------------
Create a database in your Cloud Spanner instance using the `schema`_ in the folder.
 
.. _schema:
    schema.ddl
 
To run sample
-----------------------
 
 $ python import.py instance_id database_id
 
positional arguments:
  instance_id:           Your Cloud Spanner instance ID.
  
  database_id :          Your Cloud Spanner database ID.
