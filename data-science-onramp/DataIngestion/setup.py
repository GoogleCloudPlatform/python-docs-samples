import sys

from pyspark.sql import SparkSession
from py4j.protocol import Py4JJavaError

from pyspark.sql.functions import UserDefinedFunction
from pyspark.sql.types import StringType, IntegerType, FloatType

from random import randint, choice, choices, seed
from time import time_ns

# Create a SparkSession under the name "reddit". Viewable via the Spark UI
spark = SparkSession.builder.appName("setup").getOrCreate()

# bucket_name = sys.argv[1]

table = "bigquery-public-data.new_york_citibike.citibike_trips"

# If the table doesn't exist simply continue
try:
    df = spark.read.format('bigquery').option('table', table).load()
except Py4JJavaError:
    print(f"{table} does not exist. ")

# path = "/".join(["gs:/", bucket_name, "dirty_data", ".csv.gz"])

''' START MAKING DATA DIRTY '''
def random_select(items, cum_weights):
    return choices(items, cum_weights=cum_weights, k=1)[0]

def tripduration(duration):
    seed(time_ns())
    seconds = str(duration) + " s"
    minutes = str(float(duration) / 60) + " min"
    hours = str(float(duration) / 3600) + " h"
    return random_select([seconds, minutes, hours, None, str(randint(-1000,-1))], 
        cum_weights=[0.3, 0.6, 0.9, 0.95, 1])

def station_name(name):
    seed(time_ns()+1)
    return choice([name, name.replace("&", "/")])

def starttime(t):
    seed(time_ns()+2)
    return random_select([t, None], cum_weights=[0.95, 1])

def stoptime(t):
    seed(time_ns()+3)
    return random_select([t, None], cum_weights=[0.95, 1])

def remove_data(offset):
    def user_defined_function(s):
        seed(time_ns() + offset)
        return random_select([s, None], cum_weights=[0.95, 1])
    return user_defined_function

def usertype(user):
    seed(time_ns()+4)
    return choice([user, user.upper(), user.lower(), 
        "sub" if user == "Subscriber" else user, 
        "cust" if user == "Customer" else user])

def gender(s):
    seed(time_ns()+4)
    return choice([s, s.upper(), s.lower(), 
        s[0] if len(s) > 0 else "", s[0].lower() if len(s) > 0 else ""])

id = lambda x: x

udfs = [
    UserDefinedFunction(tripduration, StringType()), # tripduration
    UserDefinedFunction(starttime, StringType()), # starttime
    UserDefinedFunction(stoptime, StringType()), # stoptime
    UserDefinedFunction(id, IntegerType()), # start_station_id
    UserDefinedFunction(station_name, StringType()), # start_station_name
    UserDefinedFunction(remove_data(42), FloatType()), # start_station_latitude
    UserDefinedFunction(remove_data(24), FloatType()), # start_station_longitude
    UserDefinedFunction(id, IntegerType()), # end_station_id
    UserDefinedFunction(station_name, StringType()), # end_station_name
    UserDefinedFunction(remove_data(100), FloatType()), # end_station_latitude
    UserDefinedFunction(remove_data(200), FloatType()), # end_station_longitude
    UserDefinedFunction(id, IntegerType()), # bikeid
    UserDefinedFunction(usertype, StringType()), # usertype
    UserDefinedFunction(id, IntegerType()), # birth_year
    UserDefinedFunction(gender, StringType()), # gender
    UserDefinedFunction(id, StringType()), # customer_plan
]

names = df.schema.names

new_df = df.select(*[udf(column).alias(name) for udf, column, name in zip(udfs, df.columns, names)])
new_df.show(100, False)

'''BACKFILLING'''
# Save to GCS bucket
# (
#     df
#     .coalesce(1)
#     .write
#     .options(codec="org.apache.hadoop.io.compress.GzipCodec")
#     .csv(path)
# )
