import sys

from pyspark.sql import SparkSession
from py4j.protocol import Py4JJavaError

from pyspark.sql.functions import UserDefinedFunction
from pyspark.sql.types import StringType, IntegerType, FloatType

from random import randint, choice, choices, seed
from time import time_ns

# Create a SparkSession under the name "reddit". Viewable via the Spark UI
spark = SparkSession.builder.appName("setup").getOrCreate()

bucket_name = sys.argv[1]

table = "bigquery-public-data.new_york_citibike.citibike_trips"

# If the table doesn't exist simply continue
try:
    df = spark.read.format('bigquery').option('table', table).load()
except Py4JJavaError:
    print(f"{table} does not exist. ")

''' START MAKING DATA DIRTY '''

def random_select(items, cum_weights):
    return choices(items, cum_weights=cum_weights, k=1)[0]

# Converts trip duration to other units
def tripduration(duration):
    seconds = str(duration) + " s"
    minutes = str(float(duration) / 60) + " min"
    hours = str(float(duration) / 3600) + " h"
    return random_select([seconds, minutes, hours, str(randint(-1000,-1))], 
        cum_weights=[0.3, 0.6, 0.9, 1])

def station_name(name):
    return choice([name, name.replace("&", "/")])

def usertype(user):
    return choice([user, user.upper(), user.lower(), 
        "sub" if user == "Subscriber" else user, 
        "cust" if user == "Customer" else user])

def gender(s):
    return choice([s, s.upper(), s.lower(), 
        s[0] if len(s) > 0 else "", s[0].lower() if len(s) > 0 else ""])

# Converts long and lat to DMS notation
def convertAngle(angle):
    degrees = int(angle)
    minutes = int((angle - degrees) * 60) 
    seconds = int((angle - degrees - minutes/60) * 3600)
    new_angle = str(degrees) + u"\u00B0" + str(minutes) + "'" + str(seconds) + '"'
    return random_select([str(angle), new_angle], cum_weights=[0.55, 1])

# Master function that calls the appopriate function per column 
def dirty_data(proc_func, allow_none):
    def udf(col_value):
        seed(hash(col_value) + time_ns())
        if allow_none:
            return random_select([None, proc_func(col_value)], cum_weights=[0.05, 1])
        else:
            return proc_func(col_value)
    return udf

id = lambda x: x

# Declare data transformations for each column in dataframe
udfs = [
    (dirty_data(tripduration, True), StringType()), # tripduration
    (dirty_data(id, True), StringType()), # starttime
    (dirty_data(id, True), StringType()), # stoptime
    (id, IntegerType()), # start_station_id
    (dirty_data(station_name, False), StringType()), # start_station_name
    (dirty_data(convertAngle, True), StringType()), # start_station_latitude
    (dirty_data(convertAngle, True), StringType()), # start_station_longitude
    (id, IntegerType()), # end_station_id
    (dirty_data(station_name, False), StringType()), # end_station_name
    (dirty_data(convertAngle, True), StringType()), # end_station_latitude
    (dirty_data(convertAngle, True), StringType()), # end_station_longitude
    (id, IntegerType()), # bikeid
    (dirty_data(usertype, False), StringType()), # usertype
    (id, IntegerType()), # birth_year
    (dirty_data(gender, False), StringType()), # gender
    (id, StringType()), # customer_plan
]

# Apply dirty transformations to df
names = df.schema.names
new_df = df.select(*[UserDefinedFunction(*udf)(column).alias(name) 
    for udf, column, name in zip(udfs, df.columns, names)])

# Duplicate about 5% of the rows
dup_df = df.where("rand() > 0.05")

# Create final dirty dataframe
df = new_df.union(dup_df)
df.show(n=200)

'''BACKFILLING'''

# Save to GCS bucket
path = "/".join(["gs:/", bucket_name, "dirty_data", ".csv.gz"])

(
    df
    .coalesce(1)
    .write
    .options(codec="org.apache.hadoop.io.compress.GzipCodec")
    .csv(path)
)
