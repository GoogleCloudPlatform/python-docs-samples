import os
import sys

from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
from pyspark.sql.functions import UserDefinedFunction, lit
from pyspark.sql.types import IntegerType, StringType


PROJECT_ID = sys.argv[1]
BUCKET_NAME = sys.argv[2]
TABLE = f'{PROJECT_ID}.new_york_citibike_trips.RAW_DATA'

def station_name(name):
    if name:
        return name.replace('/', '&')
    else:
        return ''

def main():
    '''...'''
    # Create a SparkSession under the name 'clean'. Viewable via the Spark UI
    spark = SparkSession.builder.appName('clean').getOrCreate()

    # Check if table exists
    
    try:
        df = spark.read.format('bigquery').option('table', TABLE).load()
    except Py4JJavaError:
        print(f"{TABLE} does not exist. ")
        return

    udf_map = {
        'start_station_name': (station_name, StringType())
    }

    for name, (func, col_type) in udf_map.items():
        df = df.withColumn(name, UserDefinedFunction(func, col_type)(name).alias(name))
    
    df = spark.createDataframe
    df.show(n=100)

if __name__ == '__main__':
    main()