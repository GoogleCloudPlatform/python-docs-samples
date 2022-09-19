# Dataproc extension for the Data Analytics Example

## Data in this directory
* [`ghcnd-stations.txt`](./ghcnd-stations.txt) is a freely available dataset about weather stations used in [US government climate data](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C00861). A direct download link can be found at that linked site.
* [`ghcn-stations-processed.csv`](./ghcn-stations-processed.csv) is generated from the `ghcnd-stations.txt` text file. To generate this file yourself, run `python data_processing_helper.py` from this directory


## Prerequisites
Go through the tutorial to [Run a data analytics DAG in Google Cloud](https://cloud.google.com/composer/docs/data-analytics-googlecloud) skipping the cleanup steps.

## About this example 

This directory has a DAG similar to the data analytics DAG found in the [Run a data analytics DAG in Google Cloud](https://cloud.google.com/composer/docs/data-analytics-googlecloud) tutorial, but includes a more complicated data processing step with Dataproc. Instead of answering the question, "How warm was it in Chicago on Thanksgiving for the past 25 years?" you will answer the question, "How have the rainfall patterns changed over the past 25 years in the western part of the US and in Phoenix, AZ?" For this example, the western part of the US is defined as the [census defined West region](https://www2.census.gov/geo/pdfs/maps-data/maps/reference/us_regdiv.pdf). Phoenix is used in this example because it is a city that has been affected by climate change in recent years, especially with respect to water.

The Dataproc Serverless job uses [arithmetic mean](https://www.weather.gov/abrfc/map#arithmetic_mean) to calculate precipitation and snowfall in the western states, and uses [distance weighting](https://www.weather.gov/abrfc/map#distance_weighting) to focus on the Phoenix specific area.


The DAG has three steps:

1. Ingest the data about the weather stations from Cloud Storage into BigQuery
2. Use BigQuery to join the weather station data with the data used in the prior tutorial - the [GHCN data](https://console.cloud.google.com/marketplace/details/noaa-public/ghcn-d?_ga=2.256175883.1820196808.1661536029-806997694.1661364277) and write the results to a table
3. Run a Dataproc Serverless job that processes the data by
    1. Removing any data points that are not from weather stations located in the Western US
    2. Removing any data points that are not about snow or other precipitation (data where `ELEMENT` is not `SNOW` or `PRCP`)
    3. Convert the values in the `ELEMENT` column (now equal to `SNOW` or `PRCP`) to be in mm, instead of tenths of a mm. 
    4. Extract the year from the date so the `Date` column is left only with the year
    5. Calculate the [arithmetic mean](https://www.weather.gov/abrfc/map#arithmetic_mean) of precipitation and of snowfall
    6. Calculate the [distance weighting](https://www.weather.gov/abrfc/map#distance_weighting) for Phoenix. 
    7. Write the results to tables in BigQuery

## Running this sample
* Add `data_analytics_dag_expansion.py` to the Composer environment you used in the previous tutorial
* Add `data_analytics_process_expansion.py` and `ghcn-stations-processed.csv` to the Cloud Storage bucket you created in the previous tutorial
* Create an empty BigQuery dataset called `precipitation_changes`

You do not need to add any additional Airflow variables, add any additional permissions, or create any other resources. 