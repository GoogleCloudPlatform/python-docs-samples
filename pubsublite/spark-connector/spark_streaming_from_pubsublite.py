import argparse


def spark_streaming_from_pubsublite(
    project_number: int, location: str, subscription_id: str
):
    # [START pubsublite_spark_streaming_to_pubsublite]
    from pyspark.sql import SparkSession

    # TODO(developer):
    # project_number = 11223344556677
    # location = "us-central1-a"
    # subscription_id = "your-subscription-id"

    spark = SparkSession.builder.appName("poc").master("yarn").getOrCreate()

    sdf = (
        spark.readStream.format("pubsublite")
        .option(
            "pubsublite.subscription",
            f"projects/{project_number}/locations/{location}/subscriptions/{subscription_id}",
        )
        .load()
    )

    # Expand data field
    sdf = (
        sdf
        .withColumn("", sdf.data)
        .withColumn("data", )
    )

    query = (
        sdf.writeStream.format("console")
        .outputMode("append")
        .trigger(processingTime="1 second")
        .start()
    )



    query.awaitTermination(300)
    query.stop()
    # [END pubsublite_spark_streaming_to_pubsublite]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_number", help="Google Cloud Project Number")
    parser.add_argument("location", help="Your Cloud location, e.g. us-central1-a")
    parser.add_argument("subscription_id", help="Your Pub/Sub Lite subscription ID")

    args = parser.parse_args()

    spark_streaming_from_pubsublite(
        args.project_number, args.location, args.subscription_id
    )
