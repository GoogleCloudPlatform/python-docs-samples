import sys
import re
import datetime

from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
from pyspark.sql.functions import UserDefinedFunction
from pyspark.sql.types import StringType, IntegerType, FloatType


PROJECT_ID = sys.argv[1]
BUCKET_NAME = sys.argv[2]
TABLE = f'{PROJECT_ID}.new_york_citibike_trips.RAW_DATA'

def trip_duration(duration):
    '''Convert trip duration to seconds.'''
    if not duration:
        return None
    
    time = re.match('\d*.\d', duration)

    if not time:
        return None

    time = float(time[0])

    if time < 0:
        return None

    if 'm' in duration:
        time *= 60
    elif 'h' in duration:
        time *= 60 * 60
    
    return int(time)

def station_name(name):
    '''Replaces '/' with '&'.'''
    return name.replace('/', '&') if name else None

def user_type(user):
    '''Converts user type to 'Subscriber' or 'Customer'.'''
    if not user:
        return None
    
    if user.lower().startswith('sub'):
        return 'Subscriber'
    elif user.lower().startswith('cust'):
        return 'Customer'
    else:
        return None

def gender(g):
    '''Converts gender to 'Male' or 'Female' or '''
    if not g:
        return None
    
    if g.lower().startswith('m'):
        return 'Male'
    elif g.lower().startswith('f'):
        return 'Female'
    else:
        return None

def angle(a):
    '''Converts DMS notation to angles.'''
    if not a:
        return None
    
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
    '''Writes a dataframe to a GCP bucket.'''
    path = 'gs://' + BUCKET_NAME + '/clean_citibike_data' + '.csv.gz'
    df.write.options(codec='org.apache.hadoop.io.compress.GzipCodec').csv(path)
    return path

def main():
    # Create a SparkSession under the name 'data_cleaning'. Viewable via the Spark UI
    spark = SparkSession.builder.appName('data_cleaning').getOrCreate()

    # Whether to backfill data to GCS bucket
    upload = True
    if '--test' in sys.argv:
        upload = False
        print('Results will not be backfilled into GCS bucket')

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
        gcs_path = backfill(df)
    
    df.sample(False, 0.0001).show(n=100)

if __name__ == '__main__':
    main()
    