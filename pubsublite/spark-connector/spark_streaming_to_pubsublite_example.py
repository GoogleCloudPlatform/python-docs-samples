import argparse


def spark_streaming_to_pubsublite(
    project_number: int, location: str, topic_id: str
) -> None:
    # [START pubsublite_spark_streaming_to_pubsublite]
    from pyspark.sql import SparkSession
    from pyspark.sql.types import BinaryType, StringType

    # TODO(developer):
    # project_number = 11223344556677
    # location = "us-central1-a"
    # topic_id = "your-topic-id"

    spark = SparkSession.builder.appName("write-app").master("yarn").getOrCreate()

    # Create a RateStreamSource that generates consecutive numbers with timestamps:
    # |-- timestamp: timestamp (nullable = true)
    # |-- value: long (nullable = true)
    sdf = spark.readStream.format("rate").option("rowsPerSecond", 1).load()

    # divisible_by_two_udf = udf(lambda z: "even" if str(z)[-1] % 2 == 0 else "odd")

    sdf = (
        sdf.withColumn("key", (sdf.value % 5).cast(StringType()).cast(BinaryType()))
        .withColumn("event_timestamp", sdf.timestamp)
        .withColumn(
            "data",
            sdf.value.cast(StringType()).cast(BinaryType())
            # ).withColumn(
            # "attributes", create_map(
            # lit("prop1"), array(divisible_by_two_udf("value").cast(BinaryType()))).cast(MapType(StringType(), ArrayType(BinaryType()), True))
        )
        .drop("value", "timestamp")
    )

    sdf.printSchema()

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
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_number", help="Google Cloud Project Number")
    parser.add_argument("location", help="Your Cloud location, e.g. us-central1-a")
    parser.add_argument("topic_id", help="Your Pub/Sub Lite topic ID")

    args = parser.parse_args()

    spark_streaming_to_pubsublite(args.project_number, args.location, args.topic_id)
