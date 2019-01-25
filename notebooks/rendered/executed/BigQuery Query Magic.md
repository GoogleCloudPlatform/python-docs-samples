
# BigQuery Query Magic

Jupyter magics are notebook-specific shortcuts that allow you to run commands with minimal syntax. Jupyter notebooks come pre-loaded with many [built-in commands](https://ipython.readthedocs.io/en/stable/interactive/magics.html). The BigQuery client library, `google-cloud-bigquery`, provides a cell magic, `%%bigquery`, which runs a SQL query and returns the results as a pandas DataFrame.

## Run a query on a public dataset

The following example queries the BigQuery `usa_names` public dataset, which is a Social Security Administration dataset that contains all names from Social Security card applications for births that occurred in the United States after 1879.

The example below shows how to invoke the magic (`%%bigquery`) and pass in a Standard SQL query in the body of the code cell. The results are displayed below the input cell as a [pandas DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html).


```python
%%bigquery
SELECT name, SUM(number) as count
FROM `bigquery-public-data.usa_names.usa_1910_current`
GROUP BY name
ORDER BY count DESC
LIMIT 10
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>James</td>
      <td>5001762</td>
    </tr>
    <tr>
      <th>1</th>
      <td>John</td>
      <td>4875934</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Robert</td>
      <td>4743843</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Michael</td>
      <td>4354622</td>
    </tr>
    <tr>
      <th>4</th>
      <td>William</td>
      <td>3886371</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Mary</td>
      <td>3748377</td>
    </tr>
    <tr>
      <th>6</th>
      <td>David</td>
      <td>3595923</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Richard</td>
      <td>2542659</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Joseph</td>
      <td>2518578</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Charles</td>
      <td>2273860</td>
    </tr>
  </tbody>
</table>
</div>



## Display verbose output

As the query job is running, status messages below the cell update with the query job ID and the amount of time the query has been running. By default, this output is erased and replaced with the results of the query. If you pass the `--verbose` flag, the output will remain below the cell after query completion.


```python
%%bigquery --verbose
SELECT name, SUM(number) as count
FROM `bigquery-public-data.usa_names.usa_1910_current`
GROUP BY name
ORDER BY count DESC
LIMIT 10
```

    Executing query with job ID: 77a52d0b-6a50-409c-a4dc-cc0cb4f4317a
    Query executing: 0.78s
    Query complete after 1.30s





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>James</td>
      <td>5001762</td>
    </tr>
    <tr>
      <th>1</th>
      <td>John</td>
      <td>4875934</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Robert</td>
      <td>4743843</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Michael</td>
      <td>4354622</td>
    </tr>
    <tr>
      <th>4</th>
      <td>William</td>
      <td>3886371</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Mary</td>
      <td>3748377</td>
    </tr>
    <tr>
      <th>6</th>
      <td>David</td>
      <td>3595923</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Richard</td>
      <td>2542659</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Joseph</td>
      <td>2518578</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Charles</td>
      <td>2273860</td>
    </tr>
  </tbody>
</table>
</div>



## Explicitly specify a project

By default, the `%%bigquery` magic command uses the project associated with your credentials to run the query. You may also explicitly provide a project ID using the `--project` flag. Note that your credentials must have permissions to create query jobs in the project you specify.


```python
project_id = 'your-project-id'
```


```python
%%bigquery --project $project_id
SELECT name, SUM(number) as count
FROM `bigquery-public-data.usa_names.usa_1910_current`
GROUP BY name
ORDER BY count DESC
LIMIT 10
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>James</td>
      <td>5001762</td>
    </tr>
    <tr>
      <th>1</th>
      <td>John</td>
      <td>4875934</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Robert</td>
      <td>4743843</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Michael</td>
      <td>4354622</td>
    </tr>
    <tr>
      <th>4</th>
      <td>William</td>
      <td>3886371</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Mary</td>
      <td>3748377</td>
    </tr>
    <tr>
      <th>6</th>
      <td>David</td>
      <td>3595923</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Richard</td>
      <td>2542659</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Joseph</td>
      <td>2518578</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Charles</td>
      <td>2273860</td>
    </tr>
  </tbody>
</table>
</div>



## Assign the query results to a variable

If you would like to save the results of your query to a variable, provide a variable name as a parameter to `%%bigquery`. The example below saves the results of the query to a variable named `df`. Note that when a variable is provided, the results are not displayed below the cell invoking the magic command.


```python
%%bigquery df
SELECT name, SUM(number) as count
FROM `bigquery-public-data.usa_names.usa_1910_current`
GROUP BY name
ORDER BY count DESC
LIMIT 10
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>James</td>
      <td>5001762</td>
    </tr>
    <tr>
      <th>1</th>
      <td>John</td>
      <td>4875934</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Robert</td>
      <td>4743843</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Michael</td>
      <td>4354622</td>
    </tr>
    <tr>
      <th>4</th>
      <td>William</td>
      <td>3886371</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Mary</td>
      <td>3748377</td>
    </tr>
    <tr>
      <th>6</th>
      <td>David</td>
      <td>3595923</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Richard</td>
      <td>2542659</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Joseph</td>
      <td>2518578</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Charles</td>
      <td>2273860</td>
    </tr>
  </tbody>
</table>
</div>




```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>James</td>
      <td>5001762</td>
    </tr>
    <tr>
      <th>1</th>
      <td>John</td>
      <td>4875934</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Robert</td>
      <td>4743843</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Michael</td>
      <td>4354622</td>
    </tr>
    <tr>
      <th>4</th>
      <td>William</td>
      <td>3886371</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Mary</td>
      <td>3748377</td>
    </tr>
    <tr>
      <th>6</th>
      <td>David</td>
      <td>3595923</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Richard</td>
      <td>2542659</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Joseph</td>
      <td>2518578</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Charles</td>
      <td>2273860</td>
    </tr>
  </tbody>
</table>
</div>



## Run a parameterized query

Parameterized queries are useful if you need to run a query with certain parameters calculated at run time. Note that the value types must be JSON serializable. The example below defines a parameters dictionary and passes it to the `--params` flag. The key of the dictionary is the name of the parameter, and the value of the dictionary is the value of the parameter.


```python
params = {"limit": 10}
```


```python
%%bigquery --params $params
SELECT name, SUM(number) as count
FROM `bigquery-public-data.usa_names.usa_1910_current`
GROUP BY name
ORDER BY count DESC
LIMIT @limit
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>James</td>
      <td>5001762</td>
    </tr>
    <tr>
      <th>1</th>
      <td>John</td>
      <td>4875934</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Robert</td>
      <td>4743843</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Michael</td>
      <td>4354622</td>
    </tr>
    <tr>
      <th>4</th>
      <td>William</td>
      <td>3886371</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Mary</td>
      <td>3748377</td>
    </tr>
    <tr>
      <th>6</th>
      <td>David</td>
      <td>3595923</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Richard</td>
      <td>2542659</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Joseph</td>
      <td>2518578</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Charles</td>
      <td>2273860</td>
    </tr>
  </tbody>
</table>
</div>


