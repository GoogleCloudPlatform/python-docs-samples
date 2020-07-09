"""Setup Dataproc job for Data Science Onramp Sample Application
This job ingests an external gas prices in NY dataset as well as
takes a New York Citibike dataset available on BigQuery and
"dirties" the dataset before uploading it back to BigQuery
It needs the following arguments
* the name of the Google Cloud Storage bucket to be used
* an optional --test flag to upload a subset of the dataset for testing
"""

import random
import sys
import pandas as pd

from google.cloud import bigquery
from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, UserDefinedFunction, when
from pyspark.sql.types import FloatType, StringType, StructField, StructType


BUCKET_NAME = sys.argv[1]
TABLE = "bigquery-public-data.new_york_citibike.citibike_trips"
DATASET_NAME = "data_science_onramp"
RAW_TABLE_NAME = "new_york_citibike_trips"
EXTERNAL_DATASETS = {
    "gas_prices": {
        "url": "https://data.ny.gov/api/views/wuxr-ni2i/rows.csv",
        "schema": StructType([
            StructField("Date", StringType(), True),
            StructField("New_York_State_Average_USD_per_Gal",
                        FloatType(), True),
            StructField("Albany_Average_USD_per_Gal", FloatType(), True),
            StructField("Blinghamton_Average_USD_per_Gal", FloatType(), True),
            StructField("Buffalo_Average_USD_per_Gal", FloatType(), True),
            StructField("Nassau_Average_USD_per_Gal", FloatType(), True),
            StructField("New_York_City_Average_USD_per_Gal",
                        FloatType(), True),
            StructField("Rochester_Average_USD_per_Gal", FloatType(), True),
            StructField("Syracuse_Average_USD_per_Gal", FloatType(), True),
            StructField("Utica_Average_USD_per_Gal", FloatType(), True),
        ]),
    },
}


# START MAKING DATA DIRTY
def trip_duration(duration):
    '''Converts trip duration to other units'''
    if not duration:
        return None
    seconds = f"{str(duration)} s"
    minutes = f"{str(float(duration) / 60)} min"
    hours = f"{str(float(duration) / 3600)} h"
    return random.choices([seconds, minutes, hours,
                          str(random.randint(-1000, -1))],
                          weights=[0.3, 0.3, 0.3, 0.1])[0]


def station_name(name):
    '''Replaces '&' with '/' with a 50% chance'''
    if not name:
        return None
    return random.choice([name, name.replace("&", "/")])


def user_type(user):
    '''Manipulates the user type string'''
    if not user:
        return None
    return random.choice([user, user.upper(), user.lower(),
                          "sub" if user == "Subscriber" else user,
                          "cust" if user == "Customer" else user])


def gender(s):
    '''Manipulates the gender string'''
    if not s:
        return None
    return random.choice([s.upper(), s.lower(),
                         s[0].upper() if len(s) > 0 else "",
                         s[0].lower() if len(s) > 0 else ""])


def convert_angle(angle):
    '''Converts long and lat to DMS notation'''
    if angle is None:
        return None
    degrees = int(angle)
    minutes = int((angle - degrees) * 60)
    seconds = int((angle - degrees - minutes/60) * 3600)
    new_angle = str(degrees) + "\u00B0" + \
        str(minutes) + "'" + str(seconds) + '"'
    return random.choices([str(angle), new_angle],
                          weights=[0.55, 0.45])[0]


def create_bigquery_dataset():
    # Create BigQuery Dataset
    client = bigquery.Client()
    dataset_id = f'{client.project}.{DATASET_NAME}'
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    dataset = client.create_dataset(dataset)


def write_to_bigquery(df, table_name):
    '''Write a dataframe to BigQuery'''
    client = bigquery.Client()
    dataset_id = f'{client.project}.{DATASET_NAME}'

    # Saving the data to BigQuery
    df.write.format('bigquery') \
        .option('table', f"{dataset_id}.{table_name}") \
        .option("temporaryGcsBucket", BUCKET_NAME) \
        .save()

    print(f"Table {table_name} successfully written to BigQuery")


def main():
    # Create a SparkSession under the name "setup". Viewable via the Spark UI
    spark = SparkSession.builder.appName("setup").getOrCreate()

    test = False  # Whether we are running the job as a test 

    # Check whether or not the job is running as a test
    if '--test' in sys.argv:
        test = True
        print("Subset of whole dataset will be uploaded to BigQuery")
    else:
        create_bigquery_dataset()
        print("Results will be uploaded to BigQuery")

    # Ingest External Datasets

    for table_name, data in EXTERNAL_DATASETS.items():
        print(f'Creating dataframe for {table_name}')
        df = spark.createDataFrame(pd.read_csv(data["url"]),
                                   schema=data["schema"])

        write_to_bigquery(df, table_name)

    # Check if table exists
    try:
        df = spark.read.format('bigquery').option('table', TABLE).load()
    except Py4JJavaError:
        print(f"{TABLE} does not exist. ")
        return

    # Declare dictionary with keys column names and values user defined
    #  functions and return types
    udf_map = {
            'tripduration': (trip_duration, StringType()),
            'start_station_name': (station_name, StringType()),
            'start_station_latitude': (convert_angle, StringType()),
            'start_station_longitude': (convert_angle, StringType()),
            'end_station_name': (station_name, StringType()),
            'end_station_latitude': (convert_angle, StringType()),
            'end_station_longitude': (convert_angle, StringType()),
            'usertype': (user_type, StringType()),
            'gender': (gender, StringType()),
    }

    # Declare which columns to set some values to null randomly
    null_columns = [
            'tripduration',
            'starttime',
            'stoptime',
            'start_station_latitude',
            'start_station_longitude',
            'end_station_latitude',
            'end_station_longitude',
    ]

    # Dirty the columns
    for name, udf in udf_map.items():
        df = df.withColumn(name, UserDefinedFunction(*udf)(name))

    # Randomly set about 5% of the values in some columns to null
    for name in null_columns:
        df = df.withColumn(name, when(expr("rand() < 0.05"), None).otherwise(df[name]))

    # Duplicate about 0.01% of the rows
    dup_df = df.sample(True, 0.0001)

    # Create final dirty dataframe
    df = df.union(dup_df)

    if not test:
        write_to_bigquery(df, RAW_TABLE_NAME)
    else:
        # df.sample(True, 0.0001).show(n=500, truncate=False)
        # Upload 0.001% of the table (about 600 rows)
        write_to_bigquery(df.sample(False, 0.00001))


if __name__ == '__main__':
    main()
