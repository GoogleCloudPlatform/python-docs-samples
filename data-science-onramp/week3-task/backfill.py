import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace, col

from py4j.protocol import Py4JJavaError

# Create a SparkSession under the name "reddit". Viewable via the Spark UI
spark = SparkSession.builder.appName("reddit").getOrCreate()

# Establish a set of years and months to iterate over
year = sys.argv[1]
month = sys.argv[2]
bucket_name = sys.argv[3]

# Establish a subreddit to process
top_subreddits = [
    "AskReddit",
    "AutoNewspaper",
    "RocketLeagueExchange",
    "The_Donald",
    "GlobalOffensiveTrade"
]

# Keep track of all tables accessed via the job
tables_read = []

# In the form of <project-id>.<dataset>.<table>
table = f"fh-bigquery.reddit_posts.{year}_{month}"

# If the table doesn't exist simply continue
try:
    df = spark.read.format('bigquery').option('table', table).load()
except Py4JJavaError:
    print(f"{table} does not exist. ")

print(f"Processing {table}.")

# Iterate through the subreddits and save posts to the GCS bucket
for subreddit in top_subreddits:
    subreddit_timestamps = (
        df
        .select(
            regexp_replace(col("title"), "\n", " "),
            regexp_replace(col("selftext"), "\n", " "),
            "created_utc"
        )
        .where(df.subreddit == subreddit)
    )

    path = "/".join(["gs:/", bucket_name, "reddit_posts", year, month,
                    subreddit + ".csv.gz"])

    (
        subreddit_timestamps
        .coalesce(1)
        .write
        .options(codec="org.apache.hadoop.io.compress.GzipCodec")
        .csv(path)
    )
