from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructField, StructType
from pyspark.sql.utils import AnalysisException

# Create a spark session
spark = SparkSession.builder.appName("testing setup").getOrCreate()

# Identify and create the schema
fields = [StructField("tripduration", StringType(), True),
          StructField("starttime", StringType(), True)]
schema = StructType(fields)

# Create an empty dataframe for to load the dataset
data = spark.createDataFrame([], schema)

gs_uri = "gs://citi-bike/dirty_data5/.csv.gz/ \
    part-00000-ffc51f06-7af7-46e0-9265-9dc414ee9d7b-c000.csv.gz"

# Read the files in the GCS bucket into the dataframe
try:
    data = (
        spark.read.format('csv')
        .options(codec="org.apache.hadoop.io.compress.GzipCodec")
        .load(gs_uri, schema=schema)
        .union(data)
    )
except AnalysisException:
    print("Exception occurred")

# Output the first 50 rows of the dataframe
data.show(n=50)
