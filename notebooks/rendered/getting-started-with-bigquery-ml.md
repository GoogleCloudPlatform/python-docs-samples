
# Getting Started with BigQuery ML

BigQuery ML (BQML) enables users to create and execute machine learning models in BigQuery using SQL queries. The goal is to democratise machine learning by enabling SQL practitioners to build models using their existing tools and to increase development speed by eliminating the need for data movement.

In this tutorial, you'll use the [sample Analytics 360 dataset](https://support.google.com/analytics/answer/3437719) to create a model that predicts whether a visitor will make a transaction.

## Create a dataset


```python
from google.cloud import bigquery

client = bigquery.Client(location="US")
dataset = client.create_dataset("bqml_tutorial")
```

## Create a Model

### Logistic regression for Analytics 360
Now, let's move on to our task. Here is how you would create a model to predict whether a visitor will make a transaction.


```python
%%bigquery
CREATE OR REPLACE MODEL `bqml_tutorial.sample_model` 
OPTIONS(model_type='logistic_reg') AS
SELECT
  IF(totals.transactions IS NULL, 0, 1) AS label,
  IFNULL(device.operatingSystem, "") AS os,
  device.isMobile AS is_mobile,
  IFNULL(geoNetwork.country, "") AS country,
  IFNULL(totals.pageviews, 0) AS pageviews
FROM
  `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE
  _TABLE_SUFFIX BETWEEN '20160801' AND '20170631'
LIMIT 100000;
```




<div>

<table>
<thead>
<tr>
<th></th>
</tr>
</thead>
<tbody>
</tbody>
</table>
</div>



Here, we use the visitor's device's operating system, whether said device is a mobile device, the visitor's country and the number of page views as the criteria for whether a transaction has been made.

In this case, "bqml_tutorial" is the name of the dataset and "sample_model" is the name of our model. The model type specified is binary logistic regression. In this case, `label` is what we're trying to fit to. Note that if you're only interested in 1 column, this is an alternative way to setting `input_label_cols`. We're also limiting our training data to those collected from 1 August 2016 to 31 June 2017. We're doing this to save the last month of data for "prediction". Furthermore, we're limiting to 100,000 data points to save us some time. Feel free to remove the last line if you're not in a rush.

Running the CREATE MODEL command creates a Query Job that will run asynchronously so you can, for example, close or refresh the browser.

When the job is complete, you will see an empty DataFrame returned below the cell (it may be rendered as a small box or line, depending upon your settings). This is expected because there are no query results returned from creating a model.

## Evaluate the Model


```python
%%bigquery
SELECT
  *
FROM
  ml.EVALUATE(MODEL `bqml_tutorial.sample_model`, (
SELECT
  IF(totals.transactions IS NULL, 0, 1) AS label,
  IFNULL(device.operatingSystem, "") AS os,
  device.isMobile AS is_mobile,
  IFNULL(geoNetwork.country, "") AS country,
  IFNULL(totals.pageviews, 0) AS pageviews
FROM
  `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE
  _TABLE_SUFFIX BETWEEN '20170701' AND '20170801'));
```




<div>

<table>
<thead>
<tr>
<th></th>
<th>precision</th>
<th>recall</th>
<th>accuracy</th>
<th>f1_score</th>
<th>log_loss</th>
<th>roc_auc</th>
</tr>
</thead>
<tbody>
<tr>
<th>0</th>
<td>0.461832</td>
<td>0.112663</td>
<td>0.985289</td>
<td>0.181138</td>
<td>0.046062</td>
<td>0.98184</td>
</tr>
</tbody>
</table>
</div>



If used with a linear regression model, the above query returns the following columns: `mean_absolute_error`, `mean_squared_error`, `mean_squared_log_error`, `median_absolute_error`, `r2_score`, `explained_variance`. If used with a logistic regression model, the above query returns the following columns: `precision`, `recall`, `accuracy`, `f1_score`, `log_loss`, `roc_auc`. Please consult the machine learning glossary or run a Google search to understand how each of these metrics are calculated and what they mean.

Concretely, you'll recognize the `SELECT` and `FROM` portions of the query are identical to that used during training. The `WHERE` portion reflects the change in time frame and the `FROM` portion shows that we're calling `ml.EVALUATE`. You should see a table similar to this:


<table>
<tr>
<th></th>
<th>precision</th>
<th>recall</th>
<th>accuracy</th>
<th>f1_score</th>
<th>log_loss</th>
<th>roc_auc</th>
</tr>
<tr>
<td>1</td>
<td>0.437838</td>
<td>0.075419</td>
<td>0.985249</td>
<td>0.128674</td>
<td>0.047682</td>
<td>0.982956</td>
</tr>
</table>

## Use the Model

### Predict purchases per country

Here we try to predict the number of transactions made by visitors of each country, sort the results and select the top 10 countries by purchases.


```python
%%bigquery
SELECT
  country,
  SUM(predicted_label) as total_predicted_purchases
FROM
  ml.PREDICT(MODEL `bqml_tutorial.sample_model`, (
SELECT
  IFNULL(device.operatingSystem, "") AS os,
  device.isMobile AS is_mobile,
  IFNULL(totals.pageviews, 0) AS pageviews,
  IFNULL(geoNetwork.country, "") AS country
FROM
  `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE
  _TABLE_SUFFIX BETWEEN '20170701' AND '20170801'))
GROUP BY country
ORDER BY total_predicted_purchases DESC
LIMIT 10;
```




<div>

<table>
<thead>
<tr>
<th></th>
<th>country</th>
<th>total_predicted_purchases</th>
</tr>
</thead>
<tbody>
<tr>
<th>0</th>
<td>United States</td>
<td>228</td>
</tr>
<tr>
<th>1</th>
<td>Canada</td>
<td>7</td>
</tr>
<tr>
<th>2</th>
<td>Taiwan</td>
<td>6</td>
</tr>
<tr>
<th>3</th>
<td>India</td>
<td>3</td>
</tr>
<tr>
<th>4</th>
<td>Turkey</td>
<td>2</td>
</tr>
<tr>
<th>5</th>
<td>Japan</td>
<td>2</td>
</tr>
<tr>
<th>6</th>
<td>United Kingdom</td>
<td>1</td>
</tr>
<tr>
<th>7</th>
<td>Vietnam</td>
<td>1</td>
</tr>
<tr>
<th>8</th>
<td>El Salvador</td>
<td>1</td>
</tr>
<tr>
<th>9</th>
<td>Serbia</td>
<td>1</td>
</tr>
</tbody>
</table>
</div>



Notice this query is very similar to the evaluation query we demonstrated in the previous section. Instead of `ml.EVALUATE`, we use `ml.PREDICT` here and we wrap the BQML portion of the query with standard SQL commands. Concretely, we're interested in the country and the sum of purchases for each country, so that's what we `SELECT`, `GROUP BY` and `ORDER BY`. `LIMIT` is used here to ensure we only get the top 10 results. You should see a table similar to this:

<table>
<tr><th></th><th>country</th><th>total_predicted_purchases</th></tr>
<tr><td>0</td><td>UnitedStates</td><td>467</td></tr>
<tr><td>1</td><td>Canada</td><td>8</td></tr>
<tr><td>2</td><td>Taiwan</td><td>6</td></tr>
<tr><td>3</td><td>India</td><td>5</td></tr>
<tr><td>4</td><td>UnitedKingdom</td><td>3</td></tr>
<tr><td>5</td><td>Turkey</td><td>3</td></tr>
<tr><td>6</td><td>Japan</td><td>2</td></tr>
<tr><td>7</td><td>Germany</td><td>2</td></tr>
<tr><td>8</td><td>HongKong</td><td>2</td></tr>
<tr><td>9</td><td>Singapore</td><td>2</td></tr>
</table>

### Predict purchases per user

Here is another example. This time we try to predict the number of transactions each visitor makes, sort the results and select the top 10 visitors by transactions.


```python
%%bigquery
SELECT
  fullVisitorId,
  SUM(predicted_label) as total_predicted_purchases
FROM
  ml.PREDICT(MODEL `bqml_tutorial.sample_model`, (
SELECT
  IFNULL(device.operatingSystem, "") AS os,
  device.isMobile AS is_mobile,
  IFNULL(totals.pageviews, 0) AS pageviews,
  IFNULL(geoNetwork.country, "") AS country,
  fullVisitorId
FROM
  `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE
  _TABLE_SUFFIX BETWEEN '20170701' AND '20170801'))
GROUP BY fullVisitorId
ORDER BY total_predicted_purchases DESC
LIMIT 10;
```




<div>

<table>
<thead>
<tr>
<th></th>
<th>fullVisitorId</th>
<th>total_predicted_purchases</th>
</tr>
</thead>
<tbody>
<tr>
<th>0</th>
<td>9417857471295131045</td>
<td>4</td>
</tr>
<tr>
<th>1</th>
<td>2969418676126258798</td>
<td>2</td>
</tr>
<tr>
<th>2</th>
<td>1280993661204347450</td>
<td>2</td>
</tr>
<tr>
<th>3</th>
<td>0376394056092189113</td>
<td>2</td>
</tr>
<tr>
<th>4</th>
<td>806992249032686650</td>
<td>2</td>
</tr>
<tr>
<th>5</th>
<td>1712066703099487652</td>
<td>2</td>
</tr>
<tr>
<th>6</th>
<td>057693500927581077</td>
<td>2</td>
</tr>
<tr>
<th>7</th>
<td>8388931032955052746</td>
<td>2</td>
</tr>
<tr>
<th>8</th>
<td>8064625150033508396</td>
<td>2</td>
</tr>
<tr>
<th>9</th>
<td>112288330928895942</td>
<td>2</td>
</tr>
</tbody>
</table>
</div>



You should see a table similar to this:

<table>
<tr><th></th><th>country</th><th>total_predicted_purchases</th></tr>
<tr><td>0</td><td>9417857471295131045</td><td>3</td></tr>
<tr><td>1</td><td>8388931032955052746</td><td>2</td></tr>
<tr><td>2</td><td>7420300501523012460</td><td>2</td></tr>
<tr><td>3</td><td>806992249032686650</td><td>2</td></tr>
<tr><td>4</td><td>0376394056092189113</td><td>2</td></tr>
<tr><td>5</td><td>2969418676126258798</td><td>2</td></tr>
<tr><td>6</td><td>489038402765684003</td><td>2</td></tr>
<tr><td>7</td><td>057693500927581077</td><td>2</td></tr>
<tr><td>8</td><td>112288330928895942</td><td>2</td></tr>
<tr><td>9</td><td>1280993661204347450</td><td>2</td></tr>
</table>

## Congratulations!

You completed the tutorial. Looking for a challenge? Try making a linear regression model with BQML.

What we've covered:
+ Create a binary logistic regression model
+ Evaluate the model
+ Use model to make predictions

## Cleaning up

To delete the resources created by this tutorial, execute the following code to delete the dataset and its contents:


```python
client.delete_dataset(dataset, delete_contents=True)
```

## Next Steps

For more information about BQML, please refer to the [documentation](https://cloud.google.com/bigquery/docs/bigqueryml-intro).
