import datetime
import re
import sys
import time

from google.cloud import storage
from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
from pyspark.sql.functions import UserDefinedFunction
from pyspark.sql.types import FloatType, IntegerType, StringType


def trip_duration_udf(duration):
    """Convert trip duration to seconds. Return None if negative."""
    if not duration:
        return None

    time = re.match(r"\d*.\d*", duration)

    if not time:
        return None

    time = float(time[0])

    if time < 0:
        return None

    if "m" in duration:
        time *= 60
    elif "h" in duration:
        time *= 60 * 60

    return int(time)


def station_name_udf(name):
    """Replaces '/' with '&'."""
    return name.replace("/", "&") if name else None


def user_type_udf(user):
    """Converts user type to 'Subscriber' or 'Customer'."""
    if not user:
        return None

    if user.lower().startswith("sub"):
        return "Subscriber"
    elif user.lower().startswith("cust"):
        return "Customer"


def gender_udf(gender):
    """Converts gender to 'Male' or 'Female'."""
    if not gender:
        return None

    if gender.lower().startswith("m"):
        return "Male"
    elif gender.lower().startswith("f"):
        return "Female"


def angle_udf(angle):
    """Converts DMS notation to degrees. Return None if not in DMS or degrees notation."""
    if not angle:
        return None

    dms = re.match(r'(-?\d*).(-?\d*)\'(-?\d*)"', angle)
    if dms:
        return int(dms[1]) + int(dms[2]) / 60 + int(dms[3]) / (60 * 60)

    degrees = re.match(r"\d*.\d*", angle)
    if degrees:
        return float(degrees[0])


def compute_time(duration, start, end):
    """Calculates duration, start time, and end time from each other if one value is null."""
    time_format = "%Y-%m-%dT%H:%M:%S"

    # Transform to datetime objects
    if start:
        # Round to nearest second
        if "." in start:
            start = start[: start.index(".")]
        # Convert to datetime
        start = datetime.datetime.strptime(start, time_format)
    if end:
        # Round to nearest second
        if "." in end:
            end = end[: end.index(".")]
        # Convert to datetime
        end = datetime.datetime.strptime(end, time_format)
    if duration:
        # Convert to timedelta
        duration = datetime.timedelta(seconds=duration)

    # Calculate missing value
    if start and end and not duration:
        duration = end - start
    elif duration and end and not start:
        start = end - duration
    elif duration and start and not end:
        end = start + duration

    # Transform to primitive types
    if duration:
        duration = int(duration.total_seconds())
    if start:
        start = start.strftime(time_format)
    if end:
        end = end.strftime(time_format)

    return (duration, start, end)


def compute_duration_udf(duration, start, end):
    """Calculates duration from start and end time if null."""
    return compute_time(duration, start, end)[0]


def compute_start_udf(duration, start, end):
    """Calculates start time from duration and end time if null."""
    return compute_time(duration, start, end)[1]


def compute_end_udf(duration, start, end):
    """Calculates end time from duration and start time if null."""
    return compute_time(duration, start, end)[2]


if __name__ == "__main__":
    TABLE = sys.argv[1]
    BUCKET_NAME = sys.argv[2]

    # Create a SparkSession, viewable via the Spark UI
    spark = SparkSession.builder.appName("data_cleaning").getOrCreate()

    # Load data into dataframe if table exists
    try:
        df = spark.read.format("bigquery").option("table", TABLE).load()
    except Py4JJavaError as e:
        raise Exception(f"Error reading {TABLE}") from e

    # Single-parameter udfs
    udfs = {
        "start_station_name": UserDefinedFunction(station_name_udf, StringType()),
        "end_station_name": UserDefinedFunction(station_name_udf, StringType()),
        "tripduration": UserDefinedFunction(trip_duration_udf, IntegerType()),
        "usertype": UserDefinedFunction(user_type_udf, StringType()),
        "gender": UserDefinedFunction(gender_udf, StringType()),
        "start_station_latitude": UserDefinedFunction(angle_udf, FloatType()),
        "start_station_longitude": UserDefinedFunction(angle_udf, FloatType()),
        "end_station_latitude": UserDefinedFunction(angle_udf, FloatType()),
        "end_station_longitude": UserDefinedFunction(angle_udf, FloatType()),
    }

    for name, udf in udfs.items():
        df = df.withColumn(name, udf(name))

    # Multi-parameter udfs
    multi_udfs = {
        "tripduration": {
            "udf": UserDefinedFunction(compute_duration_udf, IntegerType()),
            "params": ("tripduration", "starttime", "stoptime"),
        },
        "starttime": {
            "udf": UserDefinedFunction(compute_start_udf, StringType()),
            "params": ("tripduration", "starttime", "stoptime"),
        },
        "stoptime": {
            "udf": UserDefinedFunction(compute_end_udf, StringType()),
            "params": ("tripduration", "starttime", "stoptime"),
        },
    }

    for name, obj in multi_udfs.items():
        df = df.withColumn(name, obj["udf"](*obj["params"]))

    # Display sample of rows
    df.show(n=20)

    # Write results to GCS
    if "--dry-run" in sys.argv:
        print("Data will not be uploaded to GCS")
    else:
        # Set GCS temp location
        path = str(time.time())
        temp_path = "gs://" + BUCKET_NAME + "/" + path

        # Write dataframe to temp location to preserve the data in final location
        # This takes time, so final location should not be overwritten with partial data
        print("Uploading data to GCS...")
        (
            df.write
            # gzip the output file
            .options(codec="org.apache.hadoop.io.compress.GzipCodec")
            # write as csv
            .csv(temp_path)
        )

        # Get GCS bucket
        storage_client = storage.Client()
        source_bucket = storage_client.get_bucket(BUCKET_NAME)

        # Get all files in temp location
        blobs = list(source_bucket.list_blobs(prefix=path))

        # Copy files from temp location to the final location
        # This is much quicker than the original write to the temp location
        final_path = "clean_data/"
        for blob in blobs:
            file_match = re.match(path + r"/(part-\d*)[0-9a-zA-Z\-]*.csv.gz", blob.name)
            if file_match:
                new_blob = final_path + file_match[1] + ".csv.gz"
                source_bucket.copy_blob(blob, source_bucket, new_blob)

        # Delete the temp location
        for blob in blobs:
            blob.delete()

        print(
            "Data successfully uploaded to " + "gs://" + BUCKET_NAME + "/" + final_path
        )
