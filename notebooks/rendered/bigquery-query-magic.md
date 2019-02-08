
# BigQuery query magic

Jupyter magics are notebook-specific shortcuts that allow you to run commands with minimal syntax. Jupyter notebooks come with many [built-in commands](https://ipython.readthedocs.io/en/stable/interactive/magics.html). The BigQuery client library, `google-cloud-bigquery`, provides a cell magic, `%%bigquery`. The `%%bigquery` magic runs a SQL query and returns the results as a pandas `DataFrame`.

## Run a query on a public dataset

The following example queries the BigQuery `usa_names` public dataset. `usa_names` is a Social Security Administration dataset that contains all names from Social Security card applications for births that occurred in the United States after 1879.

The following example shows how to invoke the magic (`%%bigquery`), and how to pass in a standard SQL query in the body of the code cell. The results are displayed below the input cell as a pandas [`DataFrame`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html).


```python
%%bigquery
SELECT name, SUM(number) as count
FROM `bigquery-public-data.usa_names.usa_1910_current`
GROUP BY name
ORDER BY count DESC
LIMIT 10
```

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

## Explicitly specify a project

By default, the `%%bigquery` magic command uses your default project to run the query. You may also explicitly provide a project ID using the `--project` flag. Note that your credentials must have permissions to create query jobs in the project you specify.


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

## Assign the query results to a variable

To save the results of your query to a variable, provide a variable name as a parameter to `%%bigquery`. The following example saves the results of the query to a variable named `df`. Note that when a variable is provided, the results are not displayed below the cell that invokes the magic command.


```python
%%bigquery df
SELECT name, SUM(number) as count
FROM `bigquery-public-data.usa_names.usa_1910_current`
GROUP BY name
ORDER BY count DESC
LIMIT 10
```


```python
df
```

## Run a parameterized query

Parameterized queries are useful if you need to run a query with certain parameters that are calculated at run time. Note that the value types must be JSON serializable. The following example defines a parameters dictionary and passes it to the `--params` flag. The key of the dictionary is the name of the parameter, and the value of the dictionary is the value of the parameter.


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
