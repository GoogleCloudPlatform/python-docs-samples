# Notebook Tutorials

This directory contains Jupyter notebook tutorials for Google Cloud Platform.
The tutorials assume you have registered the `google-cloud-bigquery` magic
commands and set `matplotlib` to render inline. You can either perform these
set up steps in a single notebook, or add the steps to your IPython
configuration file to apply to all notebooks.

Run the following commands in a notebook to register the BigQuery magic
commands and set `matplotlib` to render inline:
```python
%load_ext google.cloud.bigquery
%matplotlib inline
```

Alternatively, add the following code to your `ipython_config.py` file to
perform the set up steps for all notebooks:
```python
c = get_config()

# Register magic commands
c.InteractiveShellApp.extensions = [
    'google.cloud.bigquery',
]

# Enable matplotlib renderings to render inline in the notebook.
c.InteractiveShellApp.matplotlib = 'inline'
```
See
[IPython documentation](https://ipython.readthedocs.io/en/stable/config/intro.html)
for more information about configuration.
