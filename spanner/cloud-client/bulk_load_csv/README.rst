Google Cloud Spanner: Bulk Loading From CSV Python Sample
===============

``Google Cloud Spanner`` is a highly scalable, transactional, managed, NewSQL database service.
  Cloud Spanner solves the need for a horizontally-scaling database with consistent global transactions and SQL semantics.

This application demonstrates how to load data from a csv file into a Cloud
Spanner database.

Pre-requisuite
-----------------------
Create a database in your Cloud Spanner instance using the [schema](schema.ddl) in the folder.

To run sample
-----------------------

 $ python import.py instance_id database_id

positional arguments:
  instance_id:           Your Cloud Spanner instance ID.
  
  database_id :          Your Cloud Spanner database ID.

