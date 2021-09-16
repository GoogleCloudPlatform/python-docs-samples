# Copyright 2021 Google LLC
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

import argparse


def spark_streaming_to_pubsublite(
    project_number: int, location: str, topic_id: str
) -> None:
    # [START pubsublite_spark_streaming_to_pubsublite]
    from pyspark.sql import SparkSession
    from pyspark.sql.types import BinaryType, StringType
    import uuid

    # TODO(developer):
    # project_number = 11223344556677
    # location = "us-central1-a"
    # topic_id = "your-topic-id"

    spark = SparkSession.builder.appName("write-app").master("yarn").getOrCreate()

    # Create a RateStreamSource that generates consecutive numbers with timestamps:
    # |-- timestamp: timestamp (nullable = true)
    # |-- value: long (nullable = true)
    sdf = spark.readStream.format("rate").option("rowsPerSecond", 1).load()

    sdf = (
        sdf.withColumn("key", (sdf.value % 5).cast(StringType()).cast(BinaryType()))
        .withColumn("event_timestamp", sdf.timestamp)
        .withColumn("data", sdf.value.cast(StringType()).cast(BinaryType()))
        .drop("value", "timestamp")
    )

    sdf.printSchema()

    query = (
        sdf.writeStream.format("pubsublite")
        .option(
            "pubsublite.topic",
            f"projects/{project_number}/locations/{location}/topics/{topic_id}",
        )
        # Required. Use a unique checkpoint location for each job.
        .option("checkpointLocation", "/tmp/app" + uuid.uuid4().hex)
        .outputMode("append")
        .trigger(processingTime="1 second")
        .start()
    )

    # Wait 60 seconds to terminate the query.
    query.awaitTermination(60)
    query.stop()
    # [END pubsublite_spark_streaming_to_pubsublite]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--project_number", help="Google Cloud Project Number")
    parser.add_argument("--location", help="Your Cloud location, e.g. us-central1-a")
    parser.add_argument("--topic_id", help="Your Pub/Sub Lite topic ID")

    args = parser.parse_args()

    spark_streaming_to_pubsublite(args.project_number, args.location, args.topic_id)
