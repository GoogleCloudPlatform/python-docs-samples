----------------------------------------
Copyright 2018 Google LLC 

Licensed under the Apache License, Version 2.0 (the "License");you may not use this file except in compliance with the License.You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, softwaredistributed under the License is distributed on an "AS IS" BASIS,WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.See the License for the specific language governing permissions and limitations under the License.

----------------------------------------

# Retail Product Stockouts Prediction using AutoML Tables

AutoML Tables enables you to build machine learning models based on tables of your own data and host them on Google Cloud for scalability. This solution demonstrates how you can use AutoML Tables to solve a product stockouts problem in the retail industry. This problem is solved using a binary classification approach, which predicts whether a particular product at a certain store will be out-of-stock or not in the next four weeks. Once the solution is built, you can plug this in with your production system and proactively predict stock-outs for your business.
 

Our exercise will 

1. [Walk through the problem of stock-out from a business standpoint](##business-problem)
2. [Explaining the challenges in solving this problem with machine learning](#the-machine-learning-solution)
3. [Demonstrate data preparation for machine learning](#data-preparation)
4. [Step-by-step guide to building the model on AutoML Tables UI](#building-the-model-on-automl-tables-ui)
5. [Step-by-step guide to executing the model through a python script that can be integrated with your production system](#building-the-model-using-automl-tables-python-client-library)
6. [Performance of the model built using AutoML Tables](#evaluation-results-and-business-impact)


## Business Problem

### Problem statement

A stockout, or out-of-stock (OOS) event is an event that causes inventory to be exhausted. While out-of-stocks can occur along the entire supply chain, the most visible kind are retail out-of-stocks in the fast-moving consumer goods industry (e.g., sweets, diapers, fruits). Stockouts are the opposite of overstocks, where too much inventory is retained.

### Impact

According to a study by researchers Thomas Gruen and Daniel Corsten, the global average level of out-of-stocks within retail fast-moving consumer goods sector across developed economies was 8.3% in 2002. This means that shoppers would have a 42% chance of fulfilling a ten-item shopping list without encountering a stockout. Despite the initiatives designed to improve the collaboration of retailers and their suppliers, such as Efficient Consumer Response (ECR), and despite the increasing use of new technologies such as radio-frequency identification (RFID) and point-of-sale data analytics, this situation has improved little over the past decades.

The biggest impacts being
1. Customer dissatisfaction
2. Loss of revenue

### Machine Learning Solution

Using machine learning to solve for stock-outs can help with store operations and thus prevent out-of-stock proactively.

## The Machine Learning Solution

There are three big challenges any retailer would face as they try and solve this problem with machine learning:

1. Data silos: Sales data, supply-chain data, inventory data, etc. may all be in silos. Such disjoint datasets could be a challenge to work with as a machine learning model tries to derive insights from all these data points. 
2. Missing Features: Features such as vendor location, weather conditions, etc. could add a lot of value to a machine learning algorithm to learn from. But such features are not always available and when building machine learning solutions we think for collecting features as an iterative approach to improving the machine learning model.
3. Imbalanced dataset: Datasets for classification problems such as retail stock-out are traditionally very imbalanced with fewer cases for stock-out. Designing machine learning solutions by hand for such problems would be time consuming effort when your team should be focusing on collecting features.

Hence, we recommend using AutoML Tables. With AutoML Tables you only need to work on acquiring all data and features, and AutoML Tables would do the rest. This is a one-click deploy to solving the problem of stock-out with machine learning.


## Data Preparation

### Prerequisite 

To perform this exercise, you need to have a GCP (Google Cloud Platform) account. If you don't have a GCP account, see [Create a GCP project](https://cloud.google.com/resource-manager/docs/creating-managing-projects). 

### Data

In this solution, you will use two datasets: Training/Evaluation data and Batch Prediction inputs. To access the datasets in BigQuery, you need the following information. 

Training/Evaluation dataset: 

`Project ID: product-stockout` \
`Dataset ID: product_stockout` \
`Table ID: stockout`

Batch Prediction inputs: 

`Project ID: product-stockout` \
`Dataset ID: product_stockout` \
`Table ID: batch_prediction_inputs`

### Data Schema

<table>
  <tr>
   <td>Field name
   </td>
   <td>Datatype
   </td>
   <td>Type
   </td>
   <td>Description
   </td>
  </tr>
  <tr>
   <td>Item_Number
   </td>
   <td>STRING
   </td>
   <td>Identifier
   </td>
   <td>This is the product/ item identifier
   </td>
  </tr>
  <tr>
   <td>Category
   </td>
   <td>STRING
   </td>
   <td>Identifier
   </td>
   <td>Several items could belong to one category
   </td>
  </tr>
  <tr>
   <td>Vendor_Number
   </td>
   <td>STRING
   </td>
   <td>Identifier
   </td>
   <td>Product vendor identifier
   </td>
  </tr>
  <tr>
   <td>Store_Number
   </td>
   <td>STRING
   </td>
   <td>Identifier
   </td>
   <td>Store identifier
   </td>
  </tr>
  <tr>
   <td>Item_Description
   </td>
   <td>STRING
   </td>
   <td>Text Features
   </td>
   <td>Item Description
   </td>
  </tr>
  <tr>
   <td>Category_Name
   </td>
   <td>STRING
   </td>
   <td>Text Features
   </td>
   <td>Category Name
   </td>
  </tr>
  <tr>
   <td>Vendor_Name
   </td>
   <td>STRING
   </td>
   <td>Text Features
   </td>
   <td>Vendor Name
   </td>
  </tr>
  <tr>
   <td>Store_Name
   </td>
   <td>STRING
   </td>
   <td>Text Features
   </td>
   <td>Store Name
   </td>
  </tr>
  <tr>
   <td>Address
   </td>
   <td>STRING
   </td>
   <td>Text Features
   </td>
   <td>Address
   </td>
  </tr>
  <tr>
   <td>City
   </td>
   <td>STRING
   </td>
   <td>Categorical Features
   </td>
   <td>City
   </td>
  </tr>
  <tr>
   <td>Zip_Code
   </td>
   <td>STRING
   </td>
   <td>Categorical Features
   </td>
   <td>Zip-code
   </td>
  </tr>
  <tr>
   <td>Store_Location
   </td>
   <td>STRING
   </td>
   <td>Categorical Features
   </td>
   <td>Store Location
   </td>
  </tr>
  <tr>
   <td>County_Number
   </td>
   <td>STRING
   </td>
   <td>Categorical Features
   </td>
   <td>County Number
   </td>
  </tr>
  <tr>
   <td>County
   </td>
   <td>STRING
   </td>
   <td>Categorical Features
   </td>
   <td>County Name
   </td>
  </tr>
  <tr>
   <td>Weekly Sales Quantity 
<p>
<week 1-52>
   </td>
   <td>INTEGER
   </td>
   <td>Time series data
   </td>
   <td>52 columns for weekly sales quantity from week 1 to week 52
   </td>
  </tr>
  <tr>
   <td>Weekly Sales Dollars <week 1-52>
   </td>
   <td>INTEGER
   </td>
   <td>Time series data
   </td>
   <td>52 columns for weekly sales dollars from week 1 to week 52
   </td>
  </tr>
  <tr>
   <td>Inventory
   </td>
   <td>FLOAT
   </td>
   <td>Numeric Feature
   </td>
   <td>This inventory is stocked by the retailer looking at past sales and seasonality of the product to meet demand for future sales.
   </td>
  </tr>
  <tr>
   <td>Stockout
   </td>
   <td>INTEGER
   </td>
   <td>Label 
   </td>
   <td>(1 - Stock-out, 0 - No stock-out)
<p>
When the demand for four weeks future sales is not met by the inventory in stock we say we see a stock-out. This is because an early warning sign would help the retailer re-stock inventory with a lead time for the stock to be replenished.
   </td>
  </tr>
</table>


To use AutoML Tables with BigQuery you do not need to download this dataset. However, if you would like to use AutoML Tables with GCS you may want to download this dataset and upload it into your GCP Project storage bucket. 

Instructions to download dataset: 

Sample Dataset: Download this dataset which contains sales data.

1. [Link to training data](https://console.cloud.google.com/bigquery?folder=&organizationId=&project=product-stockout&p=product-stockout&d=product_stockout&t=stockout&page=table):  \
Dataset URI: <bq://product-stockout.product_stockout.stockout>
2. [Link to data for batch predictions](https://console.cloud.google.com/bigquery?folder=&organizationId=&project=product-stockout&p=product-stockout&d=product_stockout&t=batch_prediction_inputs&page=table):  \
Dataset URI: <bq://product-stockout.product_stockout.batch_prediction_inputs>

Upload this dataset to GCS or BigQuery (optional). 

You could select either [GCS](https://cloud.google.com/storage/) or [BigQuery](https://cloud.google.com/bigquery/) as the location of your choice to store the data for this challenge. 

1. Storing data on GCS: [Creating storage buckets, Uploading data to storage buckets](https://cloud.google.com/storage/docs/creating-buckets)
2. Storing data on BigQuery: [Create and load data to BigQuery](https://cloud.google.com/bigquery/docs/quickstarts/quickstart-web-ui) (optional)


## Building the model on AutoML Tables UI

1. Enable [AutoML Tables](https://cloud.google.com/automl-tables/docs/quickstart#before_you_begin) on GCP. 

2. Visit the [AutoML Tables UI](https://console.cloud.google.com/automl-tables) to begin the process of creating your dataset and training your model. 

![ ](resources/automl_stockout_img/Image%201%202019-03-13%20at%201.02.53%20PM.png)
   
3. Import your dataset or the dataset you downloaded in the last section \
Click <+New Dataset> → Dataset Name <StockOut> → Click Create Dataset 
 
![ ](resources/automl_stockout_img/Image%202%202019-03-13%20at%201.05.17%20PM.png)

4. You can import data from BigQuery or GCS bucket \
    a. For BigQuery enter your GCP project ID, Dataset ID and Table ID \
    After specifying dataset click import dataset 
    
![ ](resources/automl_stockout_img/Image%203%202019-03-13%20at%201.08.44%20PM.png)

    b. For GCS enter the GCS object location by clicking on BROWSE \
    After specifying dataset click import dataset 
    
![ ](resources/automl_stockout_img/Image%204%202019-03-13%20at%201.09.56%20PM.png)

    Depending on the size of the dataset this import can take some time.

5. Once the import is complete you can set the schema of the imported dataset based on your business understanding of the data \
    a. Select Label i.e. Stockout \
    b. Select Variable Type for all features \
    c. Click Continue 
    
![ ](resources/automl_stockout_img/Image%206%202019-03-13%20at%201.20.57%20PM.png)

6. The imported dataset is now analyzed \
This helps you analyze the size of your dataset, dig into missing values if any, calculate correlation, mean and standard deviation. If this data quality looks good to you then we can move on to the next tab i.e. train. 

![ ](resources/automl_stockout_img/Image%20new%201%202019-03-25%20at%2012.43.13%20AM.png)

7. Train \
    a. Select a model name \
    b. Select the training budget \
    c. Select all features you would like to use for training \
    d. Select optimization objectives. Such as: ROC, Log Loss or PR curve \
    (As our data is imbalances we use PR curve as our optimization metric) \
    e. Click TRAIN \
    f. Training the model can take some time 
    
![ ](resources/automl_stockout_img/Image%208%202019-03-13%20at%201.34.08%20PM.png)

![ ](resources/automl_stockout_img/Image%20new%202%202019-03-25%20at%2012.44.18%20AM.png)

8. Once the model is trained you can click on the evaluate tab \
This tab gives you stats for model evaluation  \
         For example our model shows  \
         Area Under Precision Recall Curve: 0.645  \
         Area Under ROC Curve: 0.893 \
         Accuracy: 92.5% \
         Log Loss: 0.217 \
Selecting the threshold lets you set a desired precision and recall on your predictions. 

![ ](resources/automl_stockout_img/Image%20new%203%202019-03-25%20at%2012.49.40%20AM.png)

9. Using the model created let's use batch prediction to predict stock-out \
    a. Batch prediction data inputs could come from BigQuery or your GCS bucket. \
    b. Select the GCS bucket to store the results of your batch prediction \
    c. Click Send Batch Predictions 
    
![ ](resources/automl_stockout_img/Image%2012%202019-03-13%20at%201.56.43%20PM.png)

![ ](resources/automl_stockout_img/Image%2013%202019-03-13%20at%201.59.18%20PM.png)


## Building the model using AutoML Tables Python Client Library

In this notebook, you will learn how to build the same model as you have done on the AutoML Tables UI using its Python Client Library.


## Evaluation results and business impact

![ ](resources/automl_stockout_img/Image%20new%203%202019-03-25%20at%2012.49.40%20AM.png)

Thus the evaluation results tell us that the model we built can: 

1. 92.5% Accuracy: That is about 92.5% times you should be confident that the stock-out or no stock-out prediction is accurate. 
2. 78.2% Precision: Of the sock-outs identified 78.2% results are expected to actually be stock-outs
3. 44.1% Recall: And of all possible stock-outs 44.1% should be identified by this model
4. 1.5% False Positive Rate: Only 1.5% times an item identified as stock-out may not be out-of-stock

Thus, with such a machine learning model your business could definitely expect time savings and revenue gain by predicting stock-outs.

Note: You can always improve this model iteratively by adding business relevant features.
