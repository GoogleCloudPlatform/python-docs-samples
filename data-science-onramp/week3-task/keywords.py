import sys

from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, \
    StringType, LongType

from sparknlp.annotator import Stemmer, Tokenizer, Normalizer
from sparknlp.base import DocumentAssembler, Finisher

from pyspark.ml import Pipeline
from pyspark.ml.feature import StopWordsRemover, CountVectorizer
from pyspark.sql.functions import col, lit, concat
from pyspark.sql.utils import AnalysisException

# Assign bucket where the data lives
try:
    bucket = sys.argv[1]
except IndexError:
    print("Please provide a bucket name")
    sys.exit(1)

# Create a SparkSession under the name "reddit". Viewable via the Spark UI
spark = SparkSession.builder.appName("reddit_keywords").getOrCreate()

# Create a three column schema consisting of two strings and a long integer
fields = [StructField("title", StringType(), True),
          StructField("body", StringType(), True),
          StructField("created_at", LongType(), True)]
schema = StructType(fields)

# We'll attempt to process every month combination below.
year = '2017'
months = ['01', '02', '03', '04', '05', '06',
          '07', '08', '09', '10', '11', '12']

subreddit = "AskReddit"

# Create a base dataframe
reddit_data = spark.createDataFrame([], schema)

# Keep a running list of all files that will be processed
files_read = []

# Iterate through each month and create one data frame with all the text
for month in months:
    gs_uri = f"gs://{bucket}/reddit_posts/{year}/{month}/{subreddit}.csv.gz"

    try:
        reddit_data = (
            spark.read.format('csv')
            .options(codec="org.apache.hadoop.io.compress.GzipCodec")
            .load(gs_uri, schema=schema)
            .union(reddit_data)
        )
        files_read.append(gs_uri)

    except AnalysisException:
        continue

if len(files_read) == 0:
    print('No files read')
    sys.exit(1)

# Replace null values with empty string and combine rows
df_train = (
    reddit_data
    .fillna("")
    .select(
        concat(
            col("title"),
            lit(" "),
            col("body")
        ).alias("text")
    )
)

# Convert raw text to a document
document_assembler = DocumentAssembler().setInputCol("text") \
    .setOutputCol("document")

# Tokenize document into individual words
tokenizer = Tokenizer().setInputCols(["document"]).setOutputCol("token")

# Group words with similar meanings together
normalizer = Normalizer().setInputCols(["token"]).setOutputCol("normalizer")

# Converts word to root meaning
stemmer = Stemmer().setInputCols(["normalizer"]).setOutputCol("stem")

# Allow access to data other than spark-nlp
finisher = Finisher().setInputCols(["stem"]).setOutputCols(["to_spark"]) \
    .setValueSplitSymbol(" ")

# Remove common words
stopword_remover = StopWordsRemover(inputCol="to_spark", outputCol="filtered")

# Create matrix to count frequency of words appearing in text
tf = CountVectorizer(inputCol="filtered", outputCol="raw_features")

# Create pipeline object with transformers
pipeline = Pipeline(
    stages=[
        document_assembler,
        tokenizer,
        normalizer,
        stemmer,
        finisher,
        stopword_remover,
        tf
    ]
)

# We fit the data to the model
model = pipeline.fit(df_train)
df_trans = model.transform(df_train).show()

# Gather counts and create dictionary with words
vocab = model.stages[-1].vocabulary
counts = model.transform(df_train).select("raw_features").collect()

# Merge dictionaries per row into a master dictionary
master_dict = {}
for i in range(len(counts)):
    word_counts = dict(zip(vocab, counts[i]["raw_features"].values))
    master_dict = dict(master_dict, **word_counts)

# Sort word count by value in descending order to get top keywords
sorted_dict = sorted(master_dict, key=master_dict.get, reverse=True)
for i in range(10):
    print(sorted_dict[i])
