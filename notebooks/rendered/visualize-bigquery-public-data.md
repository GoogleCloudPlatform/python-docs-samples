
# Vizualizing BigQuery Data in a Jupyter Notebook

[BigQuery](https://cloud.google.com/bigquery/docs/) is a petabyte-scale analytics data warehouse that you can use to run SQL queries over vast amounts of data in near realtime.

Data visualization tools can help you make sense of your BigQuery data and help you analyze the data interactively. You can use visualization tools to help you identify trends, respond to them, and make predictions using your data. In this tutorial, you use the BigQuery Python client library and pandas in a Jupyter notebook to visualize data in the BigQuery natality sample table.

## Using Jupyter Magics to Query BigQuery Data

The BigQuery Python client library provides a magic command that allows you to run queries with minimal code.

The BigQuery client library provides a cell magic, `%%bigquery`, which runs a SQL query and returns the results as a pandas DataFrame. The following cell executes a query of the BigQuery Natality Public dataset and returns the total births by year.


```python
%%bigquery
SELECT
    source_year AS year,
    COUNT(is_male) AS birth_count
FROM `bigquery-public-data.samples.natality`
GROUP BY year
ORDER BY year DESC
LIMIT 15
```




<div>

<table>
<thead>
<tr>
<th></th>
<th>year</th>
<th>birth_count</th>
</tr>
</thead>
<tbody>
<tr>
<th>0</th>
<td>2008</td>
<td>4255156</td>
</tr>
<tr>
<th>1</th>
<td>2007</td>
<td>4324008</td>
</tr>
<tr>
<th>2</th>
<td>2006</td>
<td>4273225</td>
</tr>
<tr>
<th>3</th>
<td>2005</td>
<td>4145619</td>
</tr>
<tr>
<th>4</th>
<td>2004</td>
<td>4118907</td>
</tr>
<tr>
<th>5</th>
<td>2003</td>
<td>4096092</td>
</tr>
<tr>
<th>6</th>
<td>2002</td>
<td>4027376</td>
</tr>
<tr>
<th>7</th>
<td>2001</td>
<td>4031531</td>
</tr>
<tr>
<th>8</th>
<td>2000</td>
<td>4063823</td>
</tr>
<tr>
<th>9</th>
<td>1999</td>
<td>3963465</td>
</tr>
<tr>
<th>10</th>
<td>1998</td>
<td>3945192</td>
</tr>
<tr>
<th>11</th>
<td>1997</td>
<td>3884329</td>
</tr>
<tr>
<th>12</th>
<td>1996</td>
<td>3894874</td>
</tr>
<tr>
<th>13</th>
<td>1995</td>
<td>3903012</td>
</tr>
<tr>
<th>14</th>
<td>1994</td>
<td>3956925</td>
</tr>
</tbody>
</table>
</div>



The following command to runs the same query, but this time save the results to a new variable `total_births`, which is given as an argument to the `%%bigquery`. The results can then be used for further analysis and visualization.


```python
%%bigquery total_births
SELECT
    source_year AS year,
    COUNT(is_male) AS birth_count
FROM `bigquery-public-data.samples.natality`
GROUP BY year
ORDER BY year DESC
LIMIT 15
```




<div>

<table>
<thead>
<tr>
<th></th>
<th>year</th>
<th>birth_count</th>
</tr>
</thead>
<tbody>
<tr>
<th>0</th>
<td>2008</td>
<td>4255156</td>
</tr>
<tr>
<th>1</th>
<td>2007</td>
<td>4324008</td>
</tr>
<tr>
<th>2</th>
<td>2006</td>
<td>4273225</td>
</tr>
<tr>
<th>3</th>
<td>2005</td>
<td>4145619</td>
</tr>
<tr>
<th>4</th>
<td>2004</td>
<td>4118907</td>
</tr>
<tr>
<th>5</th>
<td>2003</td>
<td>4096092</td>
</tr>
<tr>
<th>6</th>
<td>2002</td>
<td>4027376</td>
</tr>
<tr>
<th>7</th>
<td>2001</td>
<td>4031531</td>
</tr>
<tr>
<th>8</th>
<td>2000</td>
<td>4063823</td>
</tr>
<tr>
<th>9</th>
<td>1999</td>
<td>3963465</td>
</tr>
<tr>
<th>10</th>
<td>1998</td>
<td>3945192</td>
</tr>
<tr>
<th>11</th>
<td>1997</td>
<td>3884329</td>
</tr>
<tr>
<th>12</th>
<td>1996</td>
<td>3894874</td>
</tr>
<tr>
<th>13</th>
<td>1995</td>
<td>3903012</td>
</tr>
<tr>
<th>14</th>
<td>1994</td>
<td>3956925</td>
</tr>
</tbody>
</table>
</div>



The next cell uses the pandas DataFrame.plot() method to visualize the query results as a bar chart. See the [pandas documentation](https://pandas.pydata.org/pandas-docs/stable/visualization.html) to learn more about data visualization with pandas.


```python
total_births.plot(kind='bar', x='year', y='birth_count');
```


![png](visualize-bigquery-public-data-resources/visualize-bigquery-public-data_6_0.png)


Run the following query to retrieve the number of births by weekday. Because the `wday` (weekday) field allows null values, the query excludes records where wday is null.


```python
%%bigquery births_by_weekday
SELECT
    wday,
    SUM(CASE WHEN is_male THEN 1 ELSE 0 END) AS male_births,
    SUM(CASE WHEN is_male THEN 0 ELSE 1 END) AS female_births
FROM `bigquery-public-data.samples.natality`
WHERE wday IS NOT NULL
GROUP BY wday
ORDER BY wday ASC
```




<div>

<table>
<thead>
<tr>
<th></th>
<th>wday</th>
<th>male_births</th>
<th>female_births</th>
</tr>
</thead>
<tbody>
<tr>
<th>0</th>
<td>1</td>
<td>4293575</td>
<td>4093357</td>
</tr>
<tr>
<th>1</th>
<td>2</td>
<td>6095840</td>
<td>5831111</td>
</tr>
<tr>
<th>2</th>
<td>3</td>
<td>6727217</td>
<td>6412155</td>
</tr>
<tr>
<th>3</th>
<td>4</td>
<td>6618729</td>
<td>6307782</td>
</tr>
<tr>
<th>4</th>
<td>5</td>
<td>6583015</td>
<td>6284434</td>
</tr>
<tr>
<th>5</th>
<td>6</td>
<td>6518636</td>
<td>6223584</td>
</tr>
<tr>
<th>6</th>
<td>7</td>
<td>4761950</td>
<td>4530052</td>
</tr>
</tbody>
</table>
</div>



Visualize the query results using a line chart.


```python
births_by_weekday.plot(x='wday');
```


![png](visualize-bigquery-public-data-resources/visualize-bigquery-public-data_10_0.png)


## Using Python to Query BigQuery Data

Magic commands allow you to use minimal syntax to interact with BigQuery. Behind the scenes, `%%bigquery` uses the BigQuery Python client library to run the given query, convert the results to a pandas Dataframe, optionally save the results to a variable, and finally display the results. Using the BigQuery Python client library directly instead of through magic commands gives you more control over your queries and allows for more complex configurations. The library's integrations with pandas enable you to combine the power of declarative SQL with imperative code (Python) to perform interesting data analysis, visualization, and transformation tasks.

To use the BigQuery Python client library, start by importing the library and initializing a client. The BigQuery client is used to send and receive messages from the BigQuery API.


```python
from google.cloud import bigquery

client = bigquery.Client()
```

Use the [`Client.query()`](https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.client.Client.html#google.cloud.bigquery.client.Client.query) method to run a query. Execute the following cell to run a query to retrieve the annual count of plural births by plurality (2 for twins, 3 for triplets, etc.).


```python
sql = """
SELECT
    plurality,
    COUNT(1) AS count,
    year
FROM
    `bigquery-public-data.samples.natality`
WHERE
    NOT IS_NAN(plurality) AND plurality &gt; 1
GROUP BY
    plurality, year
ORDER BY
    count DESC
"""
df = client.query(sql).to_dataframe()
df.head()
```




<div>

<table>
<thead>
<tr>
<th></th>
<th>plurality</th>
<th>count</th>
<th>year</th>
</tr>
</thead>
<tbody>
<tr>
<th>0</th>
<td>2</td>
<td>139209</td>
<td>2007</td>
</tr>
<tr>
<th>1</th>
<td>2</td>
<td>138866</td>
<td>2008</td>
</tr>
<tr>
<th>2</th>
<td>2</td>
<td>137239</td>
<td>2006</td>
</tr>
<tr>
<th>3</th>
<td>2</td>
<td>133285</td>
<td>2005</td>
</tr>
<tr>
<th>4</th>
<td>2</td>
<td>132344</td>
<td>2004</td>
</tr>
</tbody>
</table>
</div>



To chart the query results in your DataFrame, run the following cell to pivot the data and create a stacked bar chart of the count of plural births over time.


```python
pivot_table = df.pivot(index='year', columns='plurality', values='count')
pivot_table.plot(kind='bar', stacked=True, figsize=(15, 7));
```


![png](visualize-bigquery-public-data-resources/visualize-bigquery-public-data_16_0.png)


Run the following query to retrieve the count of births by the number of gestation weeks.


```python
sql = """
SELECT
    gestation_weeks,
    COUNT(1) AS count
FROM
    `bigquery-public-data.samples.natality`
WHERE
    NOT IS_NAN(gestation_weeks) AND gestation_weeks &lt;&gt; 99
GROUP BY
    gestation_weeks
ORDER BY
    gestation_weeks
"""
df = client.query(sql).to_dataframe()
```

Finally, chart the query results in your DataFrame.


```python
ax = df.plot(kind='bar', x='gestation_weeks', y='count', figsize=(15,7))
ax.set_title('Count of Births by Gestation Weeks')
ax.set_xlabel('Gestation Weeks')
ax.set_ylabel('Count');
```


![png](visualize-bigquery-public-data-resources/visualize-bigquery-public-data_20_0.png)


### What's Next

+ Learn more about writing queries for BigQuery — [Querying Data](https://cloud.google.com/bigquery/querying-data) in the BigQuery documentation explains how to run queries, create user-defined functions (UDFs), and more.

+ Explore BigQuery syntax — The preferred dialect for SQL queries in BigQuery is standard SQL, which is described in the [SQL Reference](https://cloud.google.com/bigquery/docs/reference/standard-sql/). BigQuery's legacy SQL-like syntax is described in the [Query Reference (legacy SQL)](https://cloud.google.com/bigquery/query-reference).
