import argparse


def spark_streaming_to_pubsublite(project_number: int, location: str, topic_id: str):
    # [START pubsublite_spark_streaming_to_pubsublite]
    from pyspark.sql import SparkSession
    from pyspark.sql.types import BinaryType, StringType

    # TODO(developer):
    # project_number = 11223344556677
    # location = "us-central1-a"
    # topic_id = "your-topic-id"

    spark = SparkSession.builder.appName("poc").master("yarn").getOrCreate()

    # RateStreamSource is a streaming source that generates consecutive
    # numbers with timestamp that can be useful for testing and PoCs.
    # DataFrame[timestamp: timestamp, value: bigint]
    sdf = spark.readStream.format("rate").option("rowsPerSecond", 1).load()

    sdf = sdf.withColumn(
        "timestamp", sdf.timestamp.cast(StringType()).cast(BinaryType())
    ).withColumn("value", sdf.value.cast(StringType()).cast(BinaryType()))

    query = (
        sdf.writeStream.format("pubsublite")
        .option(
            "pubsublite.topic",
            f"projects/{project_number}/locations/{location}/topics/{topic_id}",
        )
        .option("checkpointLocation", "/tmp/app")
        .outputMode("append")
        .trigger(processingTime="1 second")
        .start()
    )

    query.awaitTermination(60)
    query.stop()
    # [END pubsublite_spark_streaming_to_pubsublite]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_number", help="Google Cloud Project Number")
    parser.add_argument("location", help="Your Cloud location, e.g. us-central1-a")
    parser.add_argument("topic_id", help="Your Pub/Sub Lite topic ID")

    args = parser.parse_args()

    spark_streaming_to_pubsublite(args.project_number, args.location, args.topic_id)
