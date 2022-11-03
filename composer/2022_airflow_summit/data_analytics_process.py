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

# [START composer_dataanalyticstutorial_dataprocjob]
import sys


from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
from pyspark.sql.functions import col


if __name__ == "__main__":
    BUCKET_NAME = sys.argv[1]
    READ_TABLE = sys.argv[2]
    WRITE_TABLE = sys.argv[3]

    # Create a SparkSession, viewable via the Spark UI
    spark = SparkSession.builder.appName("data_processing").getOrCreate()

    # Load data into dataframe if READ_TABLE exists
    try:
        df = spark.read.format("bigquery").load(READ_TABLE)
    except Py4JJavaError as e:
        raise Exception(f"Error reading {READ_TABLE}") from e

    # Convert temperature from tenths of a degree in celsius to degrees celsius
    df = df.withColumn("value", col("value") / 10)
    # Display sample of rows
    df.show(n=20)

    # Write results to GCS
    if "--dry-run" in sys.argv:
        print("Data will not be uploaded to BigQuery")
    else:
        # Set GCS temp location
        temp_path = BUCKET_NAME

        # Saving the data to BigQuery using the "indirect path" method and the spark-bigquery connector
        # Uses the "overwrite" SaveMode to ensure DAG doesn't fail when being re-run
        # See https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html#save-modes
        # for other save mode options
        df.write.format("bigquery").option("temporaryGcsBucket", temp_path).mode(
            "overwrite"
        ).save(WRITE_TABLE)
        print("Data written to BigQuery")
# [END composer_dataanalyticstutorial_dataprocjob]
