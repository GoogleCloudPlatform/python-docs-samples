import random
import sys

from google.cloud import bigquery
from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, UserDefinedFunction, when
from pyspark.sql.types import StringType


BUCKET_NAME = sys.argv[1]
TABLE = "bigquery-public-data.new_york_citibike.citibike_trips"
RAW_DATASET_NAME = "new_york_citibike_trips"
RAW_TABLE_NAME = "RAW_DATA"


# START MAKING DATA DIRTY
def trip_duration(duration):
    '''Converts trip duration to other units'''
    if duration is None:
        return None
    seconds = str(duration) + " s"
    minutes = str(float(duration) / 60) + " min"
    hours = str(float(duration) / 3600) + " h"
    return random.choices([seconds, minutes, hours,
                          str(random.randint(-1000, -1))],
                          weights=[0.3, 0.3, 0.3, 0.1])[0]


def station_name(name):
    '''Replaces '&' with '/' with a 50% chance'''
    if name is None:
        return None
    return random.choice([name, name.replace("&", "/")])


def user_type(user):
    '''Manipulates the user type string'''
    if user is None:
        return None
    return random.choice([user, user.upper(), user.lower(),
                          "sub" if user == "Subscriber" else user,
                          "cust" if user == "Customer" else user])


def gender(s):
    '''Manipulates the gender string'''
    if s is None:
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


def write_to_bigquery(df):
    '''Write a dataframe to BigQuery'''

    # Create BigQuery Dataset
    client = bigquery.Client()
    dataset_id = f'{client.project}.{RAW_DATASET_NAME}'
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    dataset = client.create_dataset(dataset)

    # Saving the data to BigQuery
    df.write.format('bigquery') \
        .option('table', f"{dataset_id}.{RAW_TABLE_NAME}") \
        .option("temporaryGcsBucket", BUCKET_NAME) \
        .save()

    print("Table successfully written to BigQuery")


def main():
    # Create a SparkSession under the name "setup". Viewable via the Spark UI
    spark = SparkSession.builder.appName("setup").getOrCreate()

    upload = True  # Whether to upload data to BigQuery

    # Check whether or not results should be uploaded
    if len(sys.argv) > 2:
        upload = False
        print("Not uploading results to BigQuery")
    else:
        print("Results will be uploaded to BigQuery")

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

    if upload:
        write_to_bigquery(df)
    else:
        df.sample(True, 0.0001).show(n=500, truncate=False)


if __name__ == '__main__':
    main()
