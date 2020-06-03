from google.cloud import storage
from pyspark.sql.types import StructField, StructType, StringType, LongType
from pyspark.sql.utils import AnalysisException
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("testing setup").getOrCreate()

fields = [StructField("tripduration", StringType(), True),
        StructField("starttime", StringType(), True)]
schema = StructType(fields)

data = spark.createDataFrame([], schema)

gs_uri = "gs://citi-bike/dirty_data5/.csv.gz/part-00000-ffc51f06-7af7-46e0-9265-9dc414ee9d7b-c000.csv.gz"
try:
    data = (
        spark.read.format('csv')
        .options(codec="org.apache.hadoop.io.compress.GzipCodec")
        .load(gs_uri, schema=schema)
        .union(data)
    )
except AnalysisException:
    print("Exception occurred")

data.show(n=50)
