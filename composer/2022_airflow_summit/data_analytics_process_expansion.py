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

# This PySpark program is trying to answer the question: "How has the rainfall
# and snowfall patterns changed in the western US for the past 25 years?"

import sys

import pandas as pd

from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
import pyspark.sql.functions as functions


if __name__ == "__main__":
    # read in the input argument

    # GCS temp location
    BUCKET_NAME = sys.argv[1]
    # Input table
    READ_TABLE = sys.argv[2]
    # Output table after rows filtering and unit normalization
    DF_WRITE_TABLE = sys.argv[3]
    # Output table containing annual arithmetic mean of precipitation over the past 25 years
    PRCP_MEAN_WRITE_TABLE = sys.argv[4]
    # Output table containing annual arithmetic mean of snowfall over the past 25 years
    SNOW_MEAN_WRITE_TABLE = sys.argv[5]
    # Output table containing aunnal precipitation in Phoenix over the past 25 years
    PHX_PRCP_WRITE_TABLE = sys.argv[6]
    # Output table containing annual snowfall in Phoenix over the past 25 years
    PHX_SNOW_WRITE_TABLE = sys.argv[7]

    # Create a SparkSession, viewable via the Spark UI
    spark = SparkSession.builder.appName("data_processing").getOrCreate()
    # Load data into dataframe if READ_TABLE exists
    try:
        # The input dataset contains the information of different weather stations around the world.
        # You can read more about the input dataset in the following link:
        # https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt
        df = spark.read.format("bigquery").load(READ_TABLE)
    except Py4JJavaError:
        raise Exception(f"Error reading {READ_TABLE}")

    # Since the goal is to focus on the western US, you first filter out non-western states of the US.
    # The definition of western US can be found in the following link:
    # https://www2.census.gov/geo/pdfs/maps-data/maps/reference/us_regdiv.pdf
    western_states = ["AZ", "CA", "CO", "ID", "MT", "NM", "NV", "OR", "UT", "WA", "WY"]
    df = df.where(df.STATE.isin(western_states))
    df.show(n=10)
    print("After state filtering, # of rows remaining is:", df.count())

    # The input dataset contains many different weather phenomenons.
    # Based on the goal, you then filter out rows whose element value does not equal to PRCP or SNOW
    # PRCP = precipitation
    # SNOW = snowfall
    df = df.where(df.ELEMENT.isin(["PRCP", "SNOW"]))
    df.show(n=10)
    print("After element filtering, # of rows remaining is:", df.count())

    # Convert the units of precipitation and snowfall from "tenths of a mm" to "mm"
    df = df.withColumn("VALUE", df.VALUE / 10)
    df.show()

    # Extract the year of each date and rename it as YEAR
    # This will allow us to merge the data based on the years they are created instead of date
    df = df.withColumn("DATE", functions.year(df.DATE)).withColumnRenamed("DATE", "YEAR")

    # Each year's arithmetic mean of precipitation
    prcp_mean_df = (
        df.where(df.ELEMENT == "PRCP")
        .groupBy("YEAR")
        .agg(functions.avg("VALUE").alias("ANNUAL_PRCP_MEAN"))
        .sort("YEAR")
    )
    print("PRCP mean table")
    prcp_mean_df.show(n=50)

    # Each year's arithmetic mean of snowfall
    snow_mean_df = (
        df.where(df.ELEMENT == "SNOW")
        .groupBy("YEAR")
        .agg(functions.avg("VALUE").alias("ANNUAL_SNOW_MEAN"))
        .sort("YEAR")
    )
    print("SNOW mean table")
    snow_mean_df.show(n=50)

    # Filter out the states to move on to the distance weighting algorithm (DWA)
    states_near_phx = ["AZ", "CA", "CO", "NM", "NV", "UT"]
    annual_df = df.where(df.STATE.isin(states_near_phx))

    # Inverse Distance Weighting algorithm (DWA)
    @functions.pandas_udf("YEAR integer, VALUE double", functions.PandasUDFType.GROUPED_MAP)
    def phx_dw_compute(year: tuple, df: pd.DataFrame) -> pd.DataFrame:
        # This adjusts the rainfall / snowfall in Phoenix for a given year using Inverse Distance Weighting
        # based on each weather station's distance to Phoenix. The closer a station is to Phoenix, the higher
        # its measurement is weighed.
        #
        # This function combines the distance equation and inverse distance factor since the distance equation is:
        #
        #     d = sqrt((x1-x2)^2 + (y1-y2)^2))
        #
        # and the inverse distance factor is:
        #
        #     idf = 1 / d^2
        #
        # so we negate the square and square root to combine this into:
        #
        #     idf = 1 / ((x1-x2)^2 + (y1-y2)^2))
        #
        # Args:
        #    year: a tuple containing a single 4-digit integer value for this group's year
        #    df: a pandas dataframe
        #
        # Returns:
        #    A new pandas dataframe

        # Latitude and longitude of Phoenix
        PHX_LATITUDE = 33.4484
        PHX_LONGITUDE = -112.0740

        inverse_distance_factors = 1.0 / (
            (PHX_LATITUDE - df.LATITUDE) ** 2 +
            (PHX_LONGITUDE - df.LONGITUDE) ** 2
        )

        # Calculate each station's weight
        weights = inverse_distance_factors / inverse_distance_factors.sum()

        return pd.DataFrame({"YEAR": year, "VALUE": (weights * df.ANNUAL_AMOUNT).sum()})

    # Calculate the distance-weighted precipitation amount
    phx_annual_prcp_df = (
        annual_df.where(annual_df.ELEMENT == "PRCP")
        .groupBy("ID", "LATITUDE", "LONGITUDE", "YEAR")
        .agg(functions.sum("VALUE").alias("ANNUAL_AMOUNT"))
        .groupBy("YEAR")
        .apply(phx_dw_compute)
    )

    # Calculate the distance-weighted snowfall amount
    phx_annual_snow_df = (
        annual_df.where(annual_df.ELEMENT == "SNOW")
        .groupBy("ID", "LATITUDE", "LONGITUDE", "YEAR")
        .agg(functions.sum("VALUE").alias("ANNUAL_AMOUNT"))
        .groupBy("YEAR")
        .apply(phx_dw_compute)
    )

    # Display the tables
    phx_annual_prcp_df.show()
    phx_annual_snow_df.show()

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
        (
            df.write.format("bigquery")
            .option("writeMethod", "direct")
            .mode("overwrite")
            .save(DF_WRITE_TABLE)
        )

        (
            prcp_mean_df.write.format("bigquery")
            .option("writeMethod", "direct")
            .mode("overwrite")
            .save(PRCP_MEAN_WRITE_TABLE)
        )

        # this table write mysteriously fails when using the direct method
        # but works as is using the indirect method
        (
            snow_mean_df.write.format("bigquery")
            .option("temporaryGcsBucket", temp_path)
            .mode("overwrite")
            .save(SNOW_MEAN_WRITE_TABLE)
        )

        (
            phx_annual_prcp_df.write.format("bigquery")
            .option("writeMethod", "direct")
            .mode("overwrite")
            .save(PHX_PRCP_WRITE_TABLE)
        )

        (
            phx_annual_snow_df.write.format("bigquery")
            .option("writeMethod", "direct")
            .mode("overwrite")
            .save(PHX_SNOW_WRITE_TABLE)
        )

        print("Data written to BigQuery")
