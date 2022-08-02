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

import math
import sys

from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, lit, sum, udf, year
from pyspark.sql.types import FloatType, IntegerType, StructType

# BQ_DESTINATION_DATASET_NAME = "expansion_project"
# BQ_DESTINATION_TABLE_NAME = "ghcnd_stations_joined"
# BQ_NORMALIZED_TABLE_NAME = "ghcnd_stations_normalized"
# BQ_PRCP_MEAN_TABLE_NAME = "ghcnd_stations_prcp_mean"
# BQ_SNOW_MEAN_TABLE_NAME = "ghcnd_stations_snow_mean"
# BQ_PHX_PRCP_TABLE_NAME = "phx_annual_prcp"
# BQ_PHX_SNOW_TABLE_NAME = "phx_annual_snow"

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

    # BUCKET_NAME = "workshop_example_bucket"
    # READ_TABLE = f"{BQ_DESTINATION_DATASET_NAME}.{BQ_DESTINATION_TABLE_NAME}"
    # DF_WRITE_TABLE = f"{BQ_DESTINATION_DATASET_NAME}.{BQ_NORMALIZED_TABLE_NAME}"
    # PRCP_MEAN_WRITE_TABLE = f"{BQ_DESTINATION_DATASET_NAME}.{BQ_PRCP_MEAN_TABLE_NAME}"
    # SNOW_MEAN_WRITE_TABLE = f"{BQ_DESTINATION_DATASET_NAME}.{BQ_SNOW_MEAN_TABLE_NAME}"
    # PHX_PRCP_WRITE_TABLE = f"{BQ_DESTINATION_DATASET_NAME}.{BQ_PHX_PRCP_TABLE_NAME}"
    # PHX_SNOW_WRITE_TABLE = f"{BQ_DESTINATION_DATASET_NAME}.{BQ_PHX_SNOW_TABLE_NAME}"

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
    
    # Since our goal is to focus on the western US, we first filter out non-western states of the US.
    # The definition of western US can be found in the following link:
    # https://www2.census.gov/geo/pdfs/maps-data/maps/reference/us_regdiv.pdf
    western_states = ['AZ', 'CA', 'CO', 'ID', 'MT', 'NM', 'NV', 'OR', 'UT', 'WA', 'WY']
    df = df.where(df.STATE.isin(western_states))
    df.show(n=10)
    print("After state filtering, # of rows remaining is:", df.count())

    # The input dataset contains many different weather phenomenons.
    # Based on our goal, we then filter out rows whose element value does not equal to PRCP or SNOW
    # PRCP = precipitation
    # SNOW = snowfall
    df = df.where(df.ELEMENT.isin(['PRCP', 'SNOW']))
    df.show(n=10)
    print("After elemet filtering, # of rows remaining is:", df.count())

    # Convert the units of precipitation and snowfall from "tenths of a mm" to "mm"
    df = df.withColumn("VALUE", df.VALUE / 10)
    df.show()

    # Extract the year of each date and rename it as YEAR
    # This will allow us to merge the data based on the years they are created instead of date
    df = df.withColumn("DATE", year(df.DATE)).withColumnRenamed('DATE', 'YEAR')

    # Each year's arithmetic mean of precipitation
    prcp_mean_df = (
        df.where(df.ELEMENT == 'PRCP')
        .groupBy("YEAR")
        .agg(avg("VALUE").alias("ANNUAL_PRCP_MEAN"))
        .sort("YEAR")
    )
    print("prcp mean table")
    prcp_mean_df.show(n=50)

    # Each year's arithmetic mean of snowfall
    snow_mean_df = (
        df.where(df.ELEMENT == 'SNOW')
        .groupBy("YEAR")
        .agg(avg("VALUE").alias("ANNUAL_SNOW_MEAN"))
        .sort("YEAR")
    )
    print("snow mean table")
    snow_mean_df.show(n=50)

    # Filter out the states to move on to the distance weighting algorithm (DWA)
    states_near_phx = ['AZ', 'CA', 'CO', 'NM', 'NV', 'UT']
    annual_df = df.where(df.STATE.isin(states_near_phx))

    # Latitude and longitude of Phoenix
    phx_location = [33.4484, -112.0740]

    # Create blank tables for storing the results of the distance weighting algorithm (DWA)
    # The tables will have the following format
    # +------------------+-------------------+------------------+
    # |PHX_PRCP/SNOW_1997|...                |PHX_PRCP/SNOW_2021|
    # +------------------+-------------------+------------------+
    # |DWA result (float)|...                |DWA result (float)|
    # +------------------+-------------------+------------------+
    phx_annual_prcp_df = spark.createDataFrame([[]], StructType([]))
    phx_annual_snow_df = spark.createDataFrame([[]], StructType([]))

    # Distance weighting algorithm (DWA)
    def phx_dw_compute(input_list) -> float:
        # Input_list is a list of Row object with format:
        # [
        #    ROW(ID='...', LATITUDE='...', LONGITUDE='...', YEAR='...', ANNUAL_PRCP/ANNUAL_SNOW='...'),
        #    ROW(ID='...', LATITUDE='...', LONGITUDE='...', YEAR='...', ANNUAL_PRCP/ANNUAL_SNOW='...'),
        #    ...
        # ]

        # Contains 1 / d^2 of each station
        factor_list = []
        # The total sum of 1 / d^2 of all the stations
        factor_sum = 0.0
        for row in input_list:
            latitude = row[1]
            longitude = row[2]
            # Calculate the distance from each station to Phoenix
            distance_to_phx = math.sqrt((phx_location[0] - latitude) ** 2 + (phx_location[1] - longitude) ** 2)
            # Calculate the distance factor of each station (1 / d^2)
            distance_factor = 1.0 / (distance_to_phx ** 2)
            factor_list.append(distance_factor)
            factor_sum += distance_factor

        # Contains the weights of each station
        weights_list = []
        for val in factor_list:
            weights_list.append(val / factor_sum)

        dwa_result = 0.0
        for row in input_list:
            # This is the annual prcipitation/snowfall of each station
            annual_value = row[4]
            # Weight of each station
            weight = weights_list[input_list.index(row)]
            dwa_result += weight * annual_value

        # print("weight list", weights_list)
        # print("factor list", factor_list)
        # print("return result", dwa_result)
        # print("factor sum", factor_sum)

        return dwa_result

    for year in range(1997, 2022):
        # Collect() function returns a list of Row object.
        # prcp_year and snow_year will be the input for the distance weighting algorithm
        prcp_year = (
            annual_df.where((annual_df.ELEMENT == 'PRCP') & (annual_df.YEAR == year))
            .groupBy("ID", "LATITUDE", "LONGITUDE", "YEAR")
            .agg(sum("VALUE").alias("ANNUAL_PRCP")).collect()
        )
        # print(prcp_year)
        snow_year = (
            annual_df.where((annual_df.ELEMENT == 'SNOW') & (annual_df.YEAR == year))
            .groupBy("ID", "LATITUDE", "LONGITUDE", "YEAR")
            .agg(sum("VALUE").alias("ANNUAL_SNOW")).collect()
        )

        phx_annual_prcp_df = (
            phx_annual_prcp_df.withColumn(f"PHX_PRCP_{year}", lit(phx_dw_compute(prcp_year)))
        )
        phx_annual_snow_df = (
            phx_annual_snow_df.withColumn(f"PHX_SNOW_{year}", lit(phx_dw_compute(snow_year)))
        )

    # This table has only two rows (the first row contains the columns)
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
            df.write
            .format("bigquery")
            .option("temporaryGcsBucket", temp_path)
            .mode("overwrite")
            .save(DF_WRITE_TABLE)
        )

        (
            prcp_mean_df.write
            .format("bigquery")
            .option("temporaryGcsBucket", temp_path)
            .mode("overwrite")
            .save(PRCP_MEAN_WRITE_TABLE)
        )

        (
            snow_mean_df.write
            .format("bigquery")
            .option("temporaryGcsBucket", temp_path)
            .mode("overwrite")
            .save(SNOW_MEAN_WRITE_TABLE)
        )

        (
            phx_annual_prcp_df.write
            .format("bigquery")
            .option("temporaryGcsBucket", temp_path)
            .mode("overwrite")
            .save(PHX_PRCP_WRITE_TABLE)
        )

        (
            phx_annual_snow_df.write
            .format("bigquery")
            .option("temporaryGcsBucket", temp_path)
            .mode("overwrite")
            .save(PHX_SNOW_WRITE_TABLE)
        )

        print("Data written to BigQuery")
