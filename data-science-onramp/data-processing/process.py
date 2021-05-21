# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import datetime
import re
import sys
import time

from google.cloud import storage
from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
from pyspark.sql.functions import UserDefinedFunction
from pyspark.sql.types import FloatType, IntegerType, StringType


# [START datascienceonramp_tripdurationudf]
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


# [END datascienceonramp_tripdurationudf]

# [START datascienceonramp_stationnameudf]
def station_name_udf(name):
    """Replaces '/' with '&'."""
    return name.replace("/", "&") if name else None


# [END datascienceonramp_stationnameudf]

# [START datascienceonramp_usertypeudf]
def user_type_udf(user):
    """Converts user type to 'Subscriber' or 'Customer'."""
    if not user:
        return None

    if user.lower().startswith("sub"):
        return "Subscriber"
    elif user.lower().startswith("cust"):
        return "Customer"


# [END datascienceonramp_usertypeudf]


# [START datascienceonramp_stationlocationudf]
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


# [END datascienceonramp_stationlocationudf]

# [START datascienceonramp_timeconvertudf]
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
    # [END datascienceonramp_timeconvertudf]
    # [START datascienceonramp_timemissingvalueudf]
    # Calculate missing value
    if start and end and not duration:
        duration = end - start
    elif duration and end and not start:
        start = end - duration
    elif duration and start and not end:
        end = start + duration
    # [END datascienceonramp_timemissingvalueudf]
    # [START datascienceonramp_timereturnudf]
    # Transform to primitive types
    if duration:
        duration = int(duration.total_seconds())
    if start:
        start = start.strftime(time_format)
    if end:
        end = end.strftime(time_format)

    return (duration, start, end)


# [END datascienceonramp_timereturnudf]

# [START datascienceonramp_timehelperudf]
def compute_duration_udf(duration, start, end):
    """Calculates duration from start and end time if null."""
    return compute_time(duration, start, end)[0]


def compute_start_udf(duration, start, end):
    """Calculates start time from duration and end time if null."""
    return compute_time(duration, start, end)[1]


def compute_end_udf(duration, start, end):
    """Calculates end time from duration and start time if null."""
    return compute_time(duration, start, end)[2]


# [END datascienceonramp_timehelperudf]

# [START datascienceonramp_sparksession]
if __name__ == "__main__":
    BUCKET_NAME = sys.argv[1]
    TABLE = sys.argv[2]

    # Create a SparkSession, viewable via the Spark UI
    spark = SparkSession.builder.appName("data_cleaning").getOrCreate()

    # Load data into dataframe if table exists
    try:
        df = spark.read.format("bigquery").option("table", TABLE).load()
    except Py4JJavaError as e:
        raise Exception(f"Error reading {TABLE}") from e

# [END datascienceonramp_sparksession]

# [START datascienceonramp_removecolumn]
    # remove unused column
    df = df.drop("gender")
# [END datascienceonramp_removecolumn]

# [START datascienceonramp_sparksingleudfs]
    # Single-parameter udfs
    udfs = {
        "start_station_name": UserDefinedFunction(station_name_udf, StringType()),
        "end_station_name": UserDefinedFunction(station_name_udf, StringType()),
        "tripduration": UserDefinedFunction(trip_duration_udf, IntegerType()),
        "usertype": UserDefinedFunction(user_type_udf, StringType()),
        "start_station_latitude": UserDefinedFunction(angle_udf, FloatType()),
        "start_station_longitude": UserDefinedFunction(angle_udf, FloatType()),
        "end_station_latitude": UserDefinedFunction(angle_udf, FloatType()),
        "end_station_longitude": UserDefinedFunction(angle_udf, FloatType()),
    }

    for name, udf in udfs.items():
        df = df.withColumn(name, udf(name))
    # [END datascienceonramp_sparksingleudfs]
    # [START datascienceonramp_sparkmultiudfs]
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
    # [END datascienceonramp_sparkmultiudfs]
    # [START datascienceonramp_displaysamplerows]
    # Display sample of rows
    df.show(n=20)
    # [END datascienceonramp_displaysamplerows]
    # [START datascienceonramp_writetogcs]
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
# [END datascienceonramp_writetogcs]
