# Copyright 2022 Google LLC
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



import sys
import time
import uuid

from google.cloud import storage
from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
from pyspark.sql.functions import UserDefinedFunction
from pyspark.sql.types import FloatType, IntegerType, StringType


def temperature_celsius_udf(temperature_tenths):
    """Convert temperature from tenths of a degree in celsius to degrees celsius"""
    if temperature_tenths:
        return temperature_tenths / 10




# [START datascienceonramp_sparksession]
if __name__ == "__main__":
    BUCKET_NAME = sys.argv[1]
    TABLE = sys.argv[2]

    # Create a SparkSession, viewable via the Spark UI
    spark = SparkSession.builder.appName("data_processing").getOrCreate()

    # Load data into dataframe if table exists
    try:
        df = spark.read.format("bigquery").option("table", TABLE).load()
    except Py4JJavaError as e:
        raise Exception(f"Error reading {TABLE}") from e


    # [START datascienceonramp_sparksingleudfs]
    # Single-parameter udfs
    udfs = {
        "value_celsius": UserDefinedFunction(temperature_celsius_udf, FloatType()),

    }

    for name, udf in udfs.items():
        df = df.withColumn(name, udf(name))
    # [END datascienceonramp_sparksingleudfs]
    # [START datascienceonramp_sparkmultiudfs]
    # [END datascienceonramp_sparkmultiudfs]
    # [START datascienceonramp_displaysamplerows]
    # Display sample of rows
    df.show(n=20)
    # [END datascienceonramp_displaysamplerows]

 
    # # [START datascienceonramp_writetogcs]
    # Write results to GCS
    if "--dry-run" in sys.argv:
        print("Data will not be uploaded to GCS")
    else:
        # Set GCS temp location
        #temp_path = "gs://" + BUCKET_NAME
        temp_path = BUCKET_NAME

        print("temp_path", temp_path)
            # Saving the data to BigQuery using the "indirect path" method and the spark-bigquery connector
        df.write.format('bigquery') \
            .option("temporaryGcsBucket", temp_path) \
            .save('holiday_weather.holidays_weather_normalized_temperature')
        print("Data written to BigQuery")


    #     # Write dataframe to temp location to preserve the data in final location
    #     # This takes time, so final location should not be overwritten with partial data
    #     print("Uploading data to GCS...")
    #     (
    #         df.write
    #         # gzip the output file
    #         .options(codec="org.apache.hadoop.io.compress.GzipCodec")
    #         # write as csv
    #         .csv(temp_path)
    #     )

    #     # Get GCS bucket
    #     storage_client = storage.Client()
    #     source_bucket = storage_client.get_bucket(BUCKET_NAME)

    #     # Get all files in temp location
    #     blobs = list(source_bucket.list_blobs(prefix=path))

    #     # Copy files from temp location to the final location
    #     # This is much quicker than the original write to the temp location
    #     final_path = "clean_data/"
    #     for blob in blobs:
    #         file_match = re.match(path + r"/(part-\d*)[0-9a-zA-Z\-]*.csv.gz", blob.name)
    #         if file_match:
    #             new_blob = final_path + file_match[1] + ".csv.gz"
    #             source_bucket.copy_blob(blob, source_bucket, new_blob)

    #     # Delete the temp location
    #     for blob in blobs:
    #         blob.delete()

    #     print(
    #         "Data successfully uploaded to " + "gs://" + BUCKET_NAME + "/" + final_path
    #     )
# [END datascienceonramp_writetogcs]
