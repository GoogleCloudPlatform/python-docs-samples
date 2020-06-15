import os
import sys
import re
import datetime

from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
from pyspark.sql.functions import UserDefinedFunction, lit
from pyspark.sql.types import StringType, IntegerType, FloatType


PROJECT_ID = sys.argv[1]
BUCKET_NAME = sys.argv[2]
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
        dms = re.match('(-?\d*).(-?\d*)\'(-?\d*)"', a)
        if dms:
            return int(dms[1]) + int(dms[2])/60 + int(dms[3])/(60 * 60)
        else:
            try:
                return float(a)
            except ValueError:
                return None

def compute_time(duration, start, end):
    '''Calculates duration, start time, and end time from each other if one value is null.'''
    time_format = '%Y-%m-%dT%H:%M:%S'

    # Convert to datetime/timedelta
    if start:
        if '.' in start:
            start = start[:start.index('.')]
        start = datetime.datetime.strptime(start, time_format)
    if end:
        if '.' in end:
            end = end[:end.index('.')]
        end = datetime.datetime.strptime(end, time_format)
    if duration:
        duration = datetime.timedelta(seconds=duration)

    # Compute null value
    if start and end and not duration:
        duration = end - start
    elif duration and end and not start:
        start = end - duration
    elif duration and start and not end:
        end = start + duration

    # Convert from datetime/timedelta
    if duration:
        duration = int(duration.total_seconds())
    if start:
        start = start.strftime(time_format)
    if end:
        end = end.strftime(time_format)

    return (duration, start, end)
        
def compute_duration(duration, start, end):
    '''Calculates duration from start and end time if null.'''
    return compute_time(duration, start, end)[0]

def compute_start(duration, start, end):
    '''Calculates start time from duration and end time if null.'''
    return compute_time(duration, start, end)[1]

def compute_end(duration, start, end):
    '''Calculates end time from duration and start time if null.'''
    return compute_time(duration, start, end)[2]

def backfill(df):
    path = 'gs://' + BUCKET_NAME + '/clean_citibike_data' + '.csv.gz'
    df.write.options(codec='org.apache.hadoop.io.compress.GzipCodec').csv(path)

def main():
    # Create a SparkSession under the name 'clean'. Viewable via the Spark UI
    spark = SparkSession.builder.appName('clean').getOrCreate()

    # Whether to backfill data to GCS bucket
    upload = True

    # Check if table exists
    try:
        df = spark.read.format('bigquery').option('table', TABLE).load()
    except Py4JJavaError:
        print(f'{TABLE} does not exist. ')
        return

    # Single-parameter column transformations
    udfs = {
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

    for name, udf in udfs.items():
        df = df.withColumn(name, UserDefinedFunction(*udf)(name))

    # Multiple-parameter column transformations
    multi_udfs = {
        'tripduration': {
            'udf': (compute_duration, IntegerType()),
            'params': ('tripduration', 'starttime', 'stoptime')
        },
        'starttime': {
            'udf': (compute_start, StringType()),
            'params': ('tripduration', 'starttime', 'stoptime')
        },
        'stoptime': {
            'udf': (compute_end, StringType()),
            'params': ('tripduration', 'starttime', 'stoptime')
        }
    }

    for name, obj in multi_udfs.items():
        df = df.withColumn(name, UserDefinedFunction(*obj['udf'])(*obj['params']))

    if upload:
        backfill(df)
    else:
        df.show(n=100)

if __name__ == '__main__':
    main()