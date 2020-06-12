import os
import sys
import re

from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
from pyspark.sql.functions import UserDefinedFunction, lit
from pyspark.sql.types import StringType, IntegerType, FloatType


PROJECT_ID = sys.argv[1]
#BUCKET_NAME = sys.argv[2]
TABLE = f'{PROJECT_ID}.new_york_citibike_trips.RAW_DATA'

def trip_duration(duration):
    '''Convert trip duration to seconds.'''
    if duration:
        number = re.match('\d*.\d', duration)
        if number:
            number = float(number[0])
        else:
            return None

        if 's' in duration:
            return int(number)
        elif 'm' in duration:
            return int(number * 60)
        elif 'h' in duration:
            return int(number * 60 * 60)
        else:
            if number < 0:
                return None
            else:
                return int(number)

def station_name(name):
    '''Replaces '/' with '&'.'''
    if name:
        return name.replace('/', '&')

def user_type(user):
    '''Converts user type to 'Subscriber' or 'Customer'.'''
    if user:
        if user.lower().startswith('sub'):
            return 'Subscriber'
        elif user.lower().startswith('cust'):
            return 'Customer'
        else:
            return None

def gender(s):
    '''Converts gender to 'Male' or 'Female' or '''
    if s:
        if s.lower().startswith('m'):
            return 'Male'
        elif s.lower().startswith('f'):
            return 'Female'
        else:
            return None

def angle(a):
    '''Converts DMS notation to angles.'''
    if a:
        dms = re.match('(-?\d*).(-?\d*)\'(-?\d*)"', a) #todo change . with unicode symbol for degree
        if dms:
            return int(dms[1]) + int(dms[2])/60 + int(dms[3])/(60 * 60)
        else:
            try:
                return float(a)
            except ValueError:
                return 100
        

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
        'start_station_name': (station_name, StringType()),
        'end_station_name': (station_name, StringType()),
        'tripduration': (trip_duration, IntegerType()),
        'usertype': (user_type, StringType()),
        'gender': (gender, StringType()),
        'start_station_latitude': (angle, FloatType()),
        'start_station_longitude': (angle, FloatType()),
        'end_station_latitude': (angle, FloatType()),
        'end_station_longitude': (angle, FloatType())
    }

    for name, udf in udf_map.items():
        df = df.withColumn(name, UserDefinedFunction(*udf)(name).alias(name))

    df.show(n=100)

if __name__ == '__main__':
    main()