import random
import sys

from time import time_ns

from google.cloud import bigquery

from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession

from pyspark.sql.functions import UserDefinedFunction
from pyspark.sql.types import IntegerType, StringType


# Create a SparkSession under the name "setup". Viewable via the Spark UI
spark = SparkSession.builder.appName("setup").getOrCreate()

bucket_name = sys.argv[1]
upload = True  # Whether to upload data to BigQuery

# Check whether or not results should be uploaded
if len(sys.arv) > 1:
    upload = False
    print("Not uploading results to BigQuery")
else:
    print("Results will be uploaded to BigQuery")

table = "bigquery-public-data.new_york_citibike.citibike_trips"

# Check if table exists
try:
    df = spark.read.format('bigquery').option('table', table).load()
except Py4JJavaError:
    print(f"{table} does not exist. ")
    sys.exit(0)

# START MAKING DATA DIRTY


def random_select(items, weights):
    '''Picks an item according to the cumulative weights'''
    return random.choices(items, weights=weights, k=1)[0]


def trip_duration(duration):
    '''Converts trip duration to other units'''
    seconds = str(duration) + " s"
    minutes = str(float(duration) / 60) + " min"
    hours = str(float(duration) / 3600) + " h"
    return random_select([seconds, minutes, hours,
                         str(random.randint(-1000, -1))],
                         [0.3, 0.3, 0.3, 0.1])


def station_name(name):
    '''Replaces '&' with '/' with a 50% chance'''
    return random.choice([name, name.replace("&", "/")])


def user_type(user):
    '''Manipulates the user type string'''
    return random.choice([user, user.upper(), user.lower(),
                          "sub" if user == "Subscriber" else user,
                          "cust" if user == "Customer" else user])


def gender(s):
    '''Manipulates the gender string'''
    return random.choice([s, s.upper(), s.lower(),
                         s[0] if len(s) > 0 else "",
                         s[0].lower() if len(s) > 0 else ""])


def convert_angle(angle):
    '''Converts long and lat to DMS notation'''
    degrees = int(angle)
    minutes = int((angle - degrees) * 60)
    seconds = int((angle - degrees - minutes/60) * 3600)
    new_angle = str(degrees) + u"\u00B0" + \
        str(minutes) + "'" + str(seconds) + '"'
    return random_select([str(angle), new_angle], [0.55, 0.45])


def dirty_data(proc_func, allow_none):
    '''Master function returns a user defined function
    that transforms the column data'''
    def udf(col_value):
        random.seed(hash(col_value) + time_ns())
        if col_value is None:
            return col_value
        elif allow_none:
            return random_select([None, proc_func(col_value)],
                                 [0.05, 0.95])
        else:
            return proc_func(col_value)
    return udf


def id(x):
    return x


# Declare data transformations for each column in dataframe
udfs = [
    (dirty_data(trip_duration, True), StringType()),  # tripduration
    (dirty_data(id, True), StringType()),  # starttime
    (dirty_data(id, True), StringType()),  # stoptime
    (id, IntegerType()),  # start_station_id
    (dirty_data(station_name, False), StringType()),  # start_station_name
    (dirty_data(convert_angle, True), StringType()),  # start_station_latitude
    (dirty_data(convert_angle, True), StringType()),  # start_station_longitude
    (id, IntegerType()),  # end_station_id
    (dirty_data(station_name, False), StringType()),  # end_station_name
    (dirty_data(convert_angle, True), StringType()),  # end_station_latitude
    (dirty_data(convert_angle, True), StringType()),  # end_station_longitude
    (id, IntegerType()),  # bikeid
    (dirty_data(user_type, False), StringType()),  # usertype
    (id, IntegerType()),  # birth_year
    (dirty_data(gender, False), StringType()),  # gender
    (id, StringType()),  # customer_plan
]

# Apply dirty transformations to df
names = df.schema.names
new_df = df.select(*[UserDefinedFunction(*udf)(column).alias(name)
                     for udf, column, name in zip(udfs, df.columns, names)])

# Duplicate about 0.01% of the rows
dup_df = new_df.sample(False, 0.0001, seed=42)

# Create final dirty dataframe
df = new_df.union(dup_df)
df.sample(False, 0.0001, seed=50).show(n=200)
print("Dataframe sample printed")

# Write to BigQuery
if upload:
    # Create BigQuery Dataset
    client = bigquery.Client()
    dataset_id = f'{client.project}.new_york_citibike_trips'
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    dataset = client.create_dataset(dataset)

    # Saving the data to BigQuery
    spark.conf.set('temporaryGcsBucket', bucket_name)

    df.write.format('bigquery') \
        .option('table', dataset_id + ".RAW_DATA") \
        .save()
