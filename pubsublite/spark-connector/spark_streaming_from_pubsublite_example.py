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


def spark_streaming_from_pubsublite(
    project_number: int, location: str, subscription_id: str
) -> None:
    # [START pubsublite_spark_streaming_from_pubsublite]
    from pyspark.sql import SparkSession
    from pyspark.sql.types import StringType

    # TODO(developer):
    # project_number = 11223344556677
    # location = "us-central1-a"
    # subscription_id = "your-subscription-id"

    spark = SparkSession.builder.appName("read-app").master("yarn").getOrCreate()

    sdf = (
        spark.readStream.format("pubsublite")
        .option(
            "pubsublite.subscription",
            f"projects/{project_number}/locations/{location}/subscriptions/{subscription_id}",
        )
        .load()
    )

    sdf = sdf.withColumn("data", sdf.data.cast(StringType()))

    query = (
        sdf.writeStream.format("console")
        .outputMode("append")
        .trigger(processingTime="1 second")
        .start()
    )

    # Wait 120 seconds (must be >= 60 seconds) to start receiving messages.
    query.awaitTermination(120)
    query.stop()
    # [END pubsublite_spark_streaming_from_pubsublite]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--project_number", help="Google Cloud Project Number")
    parser.add_argument("--location", help="Your Cloud location, e.g. us-central1-a")
    parser.add_argument("--subscription_id", help="Your Pub/Sub Lite subscription ID")

    args = parser.parse_args()

    spark_streaming_from_pubsublite(
        args.project_number, args.location, args.subscription_id
    )
