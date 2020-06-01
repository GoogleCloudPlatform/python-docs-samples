import sys

from pyspark.sql import SparkSession
from py4j.protocol import Py4JJavaError

# Create a SparkSession under the name "reddit". Viewable via the Spark UI
spark = SparkSession.builder.appName("setup").getOrCreate()

bucket_name = sys.argv[1]

table = "bigquery-public-data.new_york_citibike.citibike_trips"

# If the table doesn't exist simply continue
try:
    df = spark.read.format('bigquery').option('table', table).load()
except Py4JJavaError:
    print(f"{table} does not exist. ")

path = "/".join(["gs:/", bucket_name, "citi_bike", ".csv.gz"])

(
    df
    .coalesce(1)
    .write
    .options(codec="org.apache.hadoop.io.compress.GzipCodec")
    .csv(path)
)
