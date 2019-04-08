----------------------------------------

Copyright 2018 Google LLC 

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

----------------------------------------

# 1. Introduction

This guide provides a high-level overview of an energy price forecasting solution, reviewing the significance of the solution and which audiences and use cases it applies to. In this section, we outline the business case for this solution, the problem, the solution, and results. In section 2, we provide the code setup instructions.  

Solution description: Model to forecast hourly energy prices for the next 7 days.

Significance: This is a good complement to standard demand forecasting models that typically predict N periods in the future. This model does a rolling forecast that is vital for operational decisions. It also takes into consideration historical trends, seasonal patterns, and external factors (like weather) to make more accurate forecasts.


## 1.1 Solution scenario

### Challenge

Many companies use forecasting models to predict prices, demand, sales, etc. Many of these forecasting problems have similar characteristics that can be leveraged to produce accurate predictions, like historical trends, seasonal patterns, and external factors.

For example, think about an energy company that needs to accurately forecast the country’s hourly energy prices for the next 5 days (120 predictions) for optimal energy trading.

At forecast time, they have access to historical energy prices as well as weather forecasts for the time period in question.

In this particular scenario, an energy company actually hosted a competition ([http://complatt.smartwatt.net/](http://complatt.smartwatt.net/)) for developers to use the data sets to create a more accurate prediction model. 

### Solution

We solved the energy pricing challenge by preparing a training dataset that encodes historical price trends, seasonal price patterns, and weather forecasts in a single table. We then used that table to train a deep neural network that can make accurate hourly predictions for the next 5 days.

## 1.2 Similar applications

Using the solution that we created for the competition, we can now show how other forecasting problems can also be solved with the same solution.

This type of solution includes any demand forecasting model that predicts N periods in the future and takes advantage of seasonal patterns, historical trends, and external datasets to produce accurate forecasts.

Here are some additional demand forecasting examples:

* Sales forecasting

* Product or service usage forecasting

* Traffic forecasting


# 2. Setting up the solution in a Google Cloud Platform project

## 2.1 Create GCP project and download raw data

Learn how to create a GCP project and prepare it for running the solution following these steps:

1. Create a project in GCP ([article](https://cloud.google.com/resource-manager/docs/creating-managing-projects) on how to create and manage GCP projects).

2. Raw data for this problem:

>[MarketPricePT](http://complatt.smartwatt.net/assets/files/historicalRealData/RealMarketPriceDataPT.csv) - Historical hourly energy prices.
>![alt text](https://storage.googleapis.com/images_public/price_schema.png)
>![alt text](https://storage.googleapis.com/images_public/price_data.png)

>[historical_weather](http://complatt.smartwatt.net/assets/files/weatherHistoricalData/WeatherHistoricalData.zip) - Historical hourly weather forecasts.
>![alt text](https://storage.googleapis.com/images_public/weather_schema.png)
>![alt text](https://storage.googleapis.com/images_public/loc_portugal.png)
>![alt text](https://storage.googleapis.com/images_public/weather_data.png)

*Disclaimer: The data for both tables comes from [http://complatt.smartwatt.net/](http://complatt.smartwatt.net/). This website hosts a closed competition meant to solve the energy price forecasting problem. The data was not collected or vetted by Google LLC and hence, we cannot guarantee the veracity or quality of it.


## 2.2 Execute script for data preparation

Prepare the data that is going to be used by the forecaster model by following these instructions:

1. Clone the solution code from here: [https://github.com/GoogleCloudPlatform/professional-services/tree/master/examples/cloudml-energy-price-forecasting](https://github.com/GoogleCloudPlatform/professional-services/tree/master/examples/cloudml-energy-price-forecasting). In the solution code, navigate to the "data_preparation" folder.

2. Run script "data_preparation.data_prep" to generate training, validation, and testing data as well as the constant files needed for normalization.

3. Export training, validation, and testing tables as CSVs (into Google Cloud Storage bucket gs://energyforecast/data/csv).

4. Read the "README.md" file for more information.

5. Understand which parameters can be passed to the script (to override defaults).

Training data schema:
![alt text](https://storage.googleapis.com/images_public/training_schema.png)

## 2.3 Execute notebook in this folder

Train the forecasting model in AutoML tables by running all cells in the notebook in this folder!

## 2.4 AutoML Tables Results

The following results are from our solution to this problem.

* MAE (Mean Absolute Error) = 0.0416
* RMSE (Root Mean Squared Error) = 0.0524

![alt text](https://storage.googleapis.com/images_public/automl_test.png)

Feature importance:
![alt text](https://storage.googleapis.com/images_public/feature_importance.png)

