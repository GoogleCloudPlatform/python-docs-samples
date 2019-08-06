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
 
Setup
------------------------
 
Authentication
++++++++++++++
 
This sample requires you to have authentication setup. Refer to the
`Authentication Getting Started Guide`_ for instructions on setting up
credentials for applications.
 
.. _Authentication Getting Started Guide:
    https://cloud.google.com/docs/authentication/getting-started
 
Install Dependencies
++++++++++++++++++++
 
#. Install `pip`_ and `virtualenv`_ if you do not already have them. You may want to refer to the `Python Development Environment Setup Guide`_ for Google Cloud Platform for instructions.
 
   .. _Python Development Environment Setup Guide:
       https://cloud.google.com/python/setup
 
#. Create a virtualenv. Samples are compatible with Python 2.7 and 3.4+.
 
    MACOS/LINUX
    
    .. code-block:: bash
 
        $ virtualenv env
        $ source env/bin/activate
        
    WINDOWS
    
    .. code-block:: bash
 
        > virtualenv env
        > .\env\Scripts\activate
 
#. Install the dependencies needed to run the samples.
 
    .. code-block:: bash
 
        $ pip install -r requirements.txt
 
.. _pip: https://pip.pypa.io/
.. _virtualenv: https://virtualenv.pypa.io/
 
 
To run sample
-----------------------
 
 $ python batch_import.py instance_id database_id
 
positional arguments:
  instance_id:           Your Cloud Spanner instance ID.
  
  database_id :          Your Cloud Spanner database ID.
