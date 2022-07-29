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

import sys
import logging
from datetime import datetime

from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, udf, lit, when, sum, year, avg
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType

import math

BQ_DESTINATION_DATASET_NAME = "expansion_project"
BQ_DESTINATION_TABLE_NAME = "ghcnd_stations_joined"
# name subject to change
BQ_NORMALIZED_TABLE_NAME = "ghcnd_stations_normalized"


if __name__ == "__main__":
    # BUCKET_NAME = sys.argv[1]
    # READ_TABLE = sys.argv[2]
    # WRITE_TABLE = sys.argv[3]


    BUCKET_NAME = "workshop_example_bucket"
    READ_TABLE = f"{BQ_DESTINATION_DATASET_NAME}.{BQ_DESTINATION_TABLE_NAME}"
    # name subject to change
    WRITE_TABLE = f"{BQ_DESTINATION_DATASET_NAME}.{BQ_NORMALIZED_TABLE_NAME}"


    # LOADING DATASET
    # Create a SparkSession, viewable via the Spark UI
    spark = SparkSession.builder.appName("data_processing").getOrCreate()
    # Load data into dataframe if READ_TABLE exists
    try:
        df = spark.read.format("bigquery").load(READ_TABLE)
    except Py4JJavaError as e:
        raise Exception(f"Error reading {READ_TABLE}") from e

    # for testing purposes
    data = df.sample(withReplacement=False, seed=1, fraction=0.0000008).collect()
    columns = ['ID', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'STATE', 'DATE', 'ELEMENT', 'VALUE']
    df = spark.createDataFrame(data, columns)
    df.show()

    # filter out non-west states of the US
    df = df.where((df.STATE == 'WA') | (df.STATE == 'OR') | (df.STATE == 'ID') 
                  | (df.STATE == 'MT') | (df.STATE == 'WY') | (df.STATE == 'CO') 
                  | (df.STATE == 'NM') | (df.STATE == 'AZ') | (df.STATE == 'UT') 
                  | (df.STATE == 'NV') | (df.STATE == 'CA'))
    df.show(n=10)
    print("After state filtering, # of rows remaining is:", df.count())
    
    # filter out rows whose element value does not equal to PRCP or SNOW 
    df = df.where((df.ELEMENT == 'PRCP') | (df.ELEMENT == 'SNOW'))
    df.show(n=10)
    print("After elemet filtering, # of rows remaining is:", df.count())
    
    # convert precipitation and snowfall from "tenths of a mm" to "mm"
    # @udf(returnType=IntegerType())
    # def converter(val) -> int:
    #     return val / 10
    # df = df.withColumn("VALUE", converter(df.VALUE))
    # df.show()

    # return the year of each date
    @udf(returnType=IntegerType())
    def date_to_year(val) -> int:
        return val.year
    
    df = df.withColumn("DATE", date_to_year(df.DATE)).withColumnRenamed('DATE', 'YEAR')
    
    prcp_mean_df = (
        df.where(df.ELEMENT == 'PRCP')
        .groupBy("YEAR")
        .agg(avg("VALUE").alias("ANNUAL_PRCP_MEAN"))
        .sort("YEAR")
    )
    print("prcp mean table")
    prcp_mean_df.show(n=50)
    
    snow_mean_df = (
        df.where(df.ELEMENT == 'SNOW')
        .groupBy("YEAR")
        .agg(avg("VALUE").alias("ANNUAL_SNOW_MEAN"))
        .sort("YEAR")
    )
    print("snow mean table")
    snow_mean_df.show(n=50)



    # CALCULATE THE DISTANCE WEIGHTING PRICIPATION IN PHOENIX OVER THE PAST 25 YEARS
    # STATES USED HERE ARE CA, NV, UT, CO, AZ, and NM ------------------------------------------------------------


    phx_location = [33.4484, -112.0740]
    def phx_dw_prcp(input_list) -> float: 
        # this list contains 1 / d^2 of each station
        factor_list = []
        # this is the total sum of 1 / d^2 of all the stations
        factor_sum = 0.0 
        for row in input_list:
            latitude = row[1]
            longitude = row[2]
            # calculate the distance from each station to Phoenix
            distance_to_phx = math.sqrt((phx_location[0] - latitude) ** 2 + (phx_location[1] - longitude) ** 2)
            # calculate the distance factor of each station
            distance_factor = 1.0 / (distance_to_phx ** 2)
            factor_list.append(distance_factor)
            factor_sum += distance_factor

        print("factor list", factor_list)
     
        # this list contains the weights of each station
        weights_list = []
        for val in factor_list:
            weights_list.append(val / factor_sum)
        print("weight list", weights_list)
        
        phx_annual_prcp = 0.0
        index = 0
        for row in input_list:
            # this is the annual prcipitation of each station
            annual_prcp = row[0]
            print(annual_prcp)
            # weight of each station
            weight = weights_list[index]
            phx_annual_prcp += weight * annual_prcp
            index += 1

        print("return result", phx_annual_prcp)
        print("factor sum", factor_sum)
        
        return phx_annual_prcp
    
    phx_annual_prcp_df = spark.createDataFrame([[]], StructType([]))
    
    annual_df = df.where(((df.STATE == 'CA') | (df.STATE == 'NV') | (df.STATE == 'UT') | (df.STATE == 'CO') 
                | (df.STATE == 'AZ') | (df.STATE == 'NM')))
    
    for year in range(1997, 2022):
        prcp_year = (
            annual_df.where((annual_df.ELEMENT == 'PRCP') & (annual_df.YEAR == year))
            .groupBy("ID", "LATITUDE", "LONGITUDE", "YEAR")
            .agg(sum("VALUE").alias("ANNUAL_PRCP")).collect()
        )
        snow_year = (
            annual_df.where((annual_df.ELEMENT == 'SNOW') & (annual_df.YEAR == year))
            .groupBy("ID", "LATITUDE", "LONGITUDE", "YEAR")
            .agg(sum("VALUE").alias("ANNUAL_SNOW")).collect()
        )
        

        phx_annual_prcp_df = (
            phx_annual_prcp_df.withColumn(f"PHX_PRCP_{year}", lit(phx_dw_prcp(prcp_year)))
        )
        phx_annual_snow_df = (
            phx_annual_snow_df.withColumn(f"PHX_SNOW_{year}", lit(phx_dw_prcp(snow_year)))
        )
    
    # this table has only two rows (the first row contains the columns)
    phx_annual_prcp_df.show()
    phx_annual_snow_df.show()
    





    # # Write results to GCS
    # if "--dry-run" in sys.argv:
    #     print("Data will not be uploaded to BigQuery")
    # else:
    #     # Set GCS temp location
    #     temp_path = BUCKET_NAME

    #     # Saving the data to BigQuery using the "indirect path" method and the spark-bigquery connector
    #     # Uses the "overwrite" SaveMode to ensure DAG doesn't fail when being re-run
    #     # See https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html#save-modes
    #     # for other save mode options
    #     df.write.format("bigquery").option("temporaryGcsBucket", temp_path).mode(
    #         "overwrite"
    #     ).save(WRITE_TABLE)
    #     print("Data written to BigQuery")
    

    
    
