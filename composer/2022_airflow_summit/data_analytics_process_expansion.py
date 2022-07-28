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
from pyspark.sql.functions import col, count, udf, lit, when, sum, year
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

    # FILTER OUT NON-WEST STATES (US) IN THE DATASET
    
    # !!!!! need to also specify US here !!!!!!!
    df = df.where((df.STATE == 'WA') | (df.STATE == 'OR') | (df.STATE == 'ID') 
                  | (df.STATE == 'MT') | (df.STATE == 'WY') | (df.STATE == 'CO') 
                  | (df.STATE == 'NM') | (df.STATE == 'AZ') | (df.STATE == 'UT') 
                  | (df.STATE == 'NV') | (df.STATE == 'CA'))
    df.show(n=10)
    print("After state filtering, # of rows remaining is:", df.count())
    
    # FILTER OUT ROWS WHOSE ELEMENT VALUE DO NOT EQUAL TO PRCP NOR SNOW THE DATASET
    df = df.where((df.ELEMENT == 'PRCP') | (df.ELEMENT == 'SNOW'))
    df.show(n=10)
    print("After elemet filtering, # of rows remaining is:", df.count())
    
    # CONVERT PRECIPITATION AND SNOW FROM TENTHS OF A MM TO MM
    # @udf(returnType=IntegerType())
    # def converter(val) -> int:
    #     return val / 10
    # df = df.withColumn("VALUE", converter(df.VALUE))
    # df.show()

    # CALCULATE THE ARITHMETIC MEAN OF PRECIPITATION
    # this funcation calcualte the arithmetic mean given a list of floats


    # try to use the built-in functions of PySpark here to calculate the arithmetic mean\
    # also, we can group by the original dataframe to create a new one, and output the dataframe
    # to the BigQuery
    def prcp_arithmetic_mean(col) -> float:
        prcp_sum = 0.0
        for prcp_value in col:
            prcp_sum += prcp_value
        return prcp_sum / len(col) if len(col) != 0 else 0.0
    
    for year in range(1997, 2022):
        # we don't care about states here since we are calculating the arithmetic mean of the entire western us
        prcp_year = (
            df.select('VALUE')
            .where((df.ELEMENT == 'PRCP') & (df.DATE >= f'{year}-01-01') & (df.DATE <= f"{year}-12-31"))
            .rdd.flatMap(lambda x: x).collect()
        )
        if year == 1997: 
            # It will create a new column named YEARLY_PRCP_ARITHMETIC_MEAN
            df = df.withColumn("YEARLY_PRCP_ARITHMETIC_MEAN", 
            when((df.ELEMENT == 'PRCP') & (df.DATE >= f'{year}-01-01') & (df.DATE <= f"{year}-12-31"), 
            prcp_arithmetic_mean(prcp_year)))
        else:
            # It will edit the already existing column named YEARLY_PRCP_ARITHMETIC_MEAN
            df = df.withColumn("YEARLY_PRCP_ARITHMETIC_MEAN", 
            when((df.ELEMENT == 'PRCP') & (df.DATE >= f'{year}-01-01') & (df.DATE <= f"{year}-12-31"), 
            prcp_arithmetic_mean(prcp_year)).otherwise(df.YEARLY_PRCP_ARITHMETIC_MEAN))
    df.show(n=50)

    
    # CALCULATE THE ARITHMETIC MEAN OF SNOWFALL
    # this funcation calcualte the arithmetic mean given a list of floats

    # try to use the built-in functions of PySpark here to calculate the arithmetic mean
    # also, we can group by the original dataframe to create a new one, and output the dataframe
    # to the BigQuery
    def snow_arithmetic_mean(col) -> float:
        snow_sum = 0.0
        for snow_value in col:
            snow_sum += snow_value
        return snow_sum / len(col) if len(col) != 0 else 0.0
    
    for year in range(1997, 2022):
        # we don't care about states here since we are calculating the arithmetic mean of the entire western us
        snow_year = (
            df.select('VALUE')
            .where((df.ELEMENT == 'SNOW') & (df.DATE >= f'{year}-01-01') & (df.DATE <= f"{year}-12-31"))
            .rdd.flatMap(lambda x: x).collect()
        )
        if year == 1997:
            # It will create a new column named YEARLY_SNOW_ARITHMETIC_MEAN
            df = df.withColumn("YEARLY_SNOW_ARITHMETIC_MEAN", 
            when((df.ELEMENT == 'SNOW') & (df.DATE >= f'{year}-01-01') & (df.DATE <= f"{year}-12-31"), 
            snow_arithmetic_mean(snow_year)))
        else:
            # It will edit the already existing column named YEARLY_SNOW_ARITHMETIC_MEAN
            df = df.withColumn("YEARLY_SNOW_ARITHMETIC_MEAN", 
            when((df.ELEMENT == 'SNOW') & (df.DATE >= f'{year}-01-01') & (df.DATE <= f"{year}-12-31"), 
            snow_arithmetic_mean(snow_year)).otherwise(df.YEARLY_SNOW_ARITHMETIC_MEAN))
    df.show(n=50)
    

    # CALCULATE THE DISTANCE WEIGHTING PRICIPATION IN PHOENIX OVER THE PAST 25 YEARS
    # STATES USED HERE ARE CA, NV, UT, CO, AZ, and NM ------------------------------------------------------------

    # drop the rows with "element" = "snow"
    df_snow_drop = df.na.drop(subset="YEARLY_PRCP_ARITHMETIC_MEAN")
    df.show(n=50)
    df_snow_drop.show(n=50)
    
    # return the year of each date
    @udf(returnType=IntegerType())
    def date_to_year(val) -> int:
        return val.year
    
    annual_prcp_table = (
        df_snow_drop.select('ID', 'STATE', 'LATITUDE', 'LONGITUDE', 'VALUE', 'DATE')
        .where(((df.STATE == 'CA') | (df.STATE == 'NV') | (df.STATE == 'UT') | (df.STATE == 'CO') 
                | (df.STATE == 'AZ') | (df.STATE == 'NM')))
        .withColumn("DATE", date_to_year(df.DATE))
    )
    print("original annual_prcp_table:")
    annual_prcp_table.show(n=50)
    
    # this table contains each station's annual pricipation each year
    annual_prcp_table = (
        annual_prcp_table.groupBy("ID", "STATE", "LATITUDE", "LONGITUDE", "DATE")
        .agg(sum("VALUE").alias("ANNUAL_PRCP"))
        .withColumnRenamed('DATE', 'YEAR')
    )
    print("annual_prcp_table after grouby function:")
    annual_prcp_table.show(n=200)
    
    
    # This is good up until this point !!!!!!!!!!!

    phx_location = [33.4484, -112.0740]
    def phx_dw_prcp(col) -> float: 
        # this list contains 1 / d^2 of each station
        factor_list = []
        # this is the total sum of 1 / d^2 of all the stations
        factor_sum = 0.0 
        for index in range(0, len(col) - 2, 3):
            latitude = col[index + 1]
            longitude = col[index + 2]
            # calculate the distance from each station to Phoenix
            distance_to_phx = math.sqrt((phx_location[0] - latitude) ** 2 + (phx_location[1] - longitude) ** 2)
            # calculate the distance factor of each station
            distance_factor = 1.0 / (distance_to_phx ** 2)
            factor_list.append(distance_factor)
            factor_sum += distance_factor
            print("index #1", index)
            # index += 3

        print("factor list", factor_list)
     
        # this list contains the weights of each station
        weights_list = []
        for val in factor_list:
            weights_list.append(val / factor_sum)
        print("weight list", weights_list)
        
        phx_annual_prcp = 0.0
        for index in range(0, len(col) - 2, 3):
            # this is the annual prcipitation of each station
            annual_prcp = col[index]
            # weight of each station
            weight = weights_list[index] if index == 0 else weights_list[int(index / 3)]
            phx_annual_prcp += weight * annual_prcp
            print("index #2", index)
            print("index #3", int(index / 3))
            # index += 3

        print("return result", phx_annual_prcp)
        print("factor sum", factor_sum)
        
        return phx_annual_prcp
    
    # emptyRDD = spark.sparkContext.emptyRDD()
    # schema = StructType([StructField('PHX_PRCP_1997', IntegerType(), False)])
    schema=StructType([])
    # phx_annual_prcp_df = spark.createDataFrame(emptyRDD, StructType([]))
    phx_annual_prcp_df = spark.createDataFrame([[]], schema)
    
     
    
    for year in range(1997, 2022):
        # if I'm only using collect(), the return type would be a list of Row object
        # to select the first object in the first row, simplely use row[0][0]
        prcp_year = (
            annual_prcp_table.select('ANNUAL_PRCP', 'LATITUDE', 'LONGITUDE')
            .where(annual_prcp_table.YEAR == year).collect()
            # .rdd.flatMap(lambda x: [x]).collect()
        )
        print(prcp_year)
        # phx_annual_prcp_df = spark.createDataFrame([[10]], schema)
        phx_annual_prcp_df = (
            phx_annual_prcp_df.withColumn(f"PHX_PRCP_{year}", lit(phx_dw_prcp(prcp_year)))
        )
    
    # this table has only two rows (the first row contains the columns)
    phx_annual_prcp_df.show()
    
    
    # ------------------------------------------------------------------------------------------------------------------------


    # CALCULATE THE DISTANCE WEIGHTING SNOWFALL IN PHOENIX OVER THE PAST 25 YEARS
    # STATES USED HERE ARE CA, NV, UT, CO, AZ, and NM





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
    

    
    
