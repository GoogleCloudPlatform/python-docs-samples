# Notebook Tutorials

This directory contains Jupyter notebook tutorials for Google Cloud Platform.
The tutorials assume you have performed the following steps:

1. Install Jupyter notebooks ([instructions](https://jupyter.org/install))
1. Install the dependencies in the [requirements.txt](./requirements.txt) file ([instructions below](#install-the-dependencies))
1. Registered the `google-cloud-bigquery` magic commands ([instructions below](#register-magics-and-configure-matplotlib))
1. Set `matplotlib` to render inline ([instructions below](#register-magics-and-configure-matplotlib))

## Install the dependencies

Install the dependencies with the following command:

        pip install --upgrade -r requirements.txt

## Register magics and configure matplotlib

You can either perform these set up steps in a single notebook, or add the
steps to your IPython configuration file to apply to all notebooks.

### Perform set up steps within a notebook

To perform the set up steps for a single notebook, run the following commands
in your notebook to register the BigQuery magic commands and set `matplotlib`
to render inline:
```python
%load_ext google.cloud.bigquery
%matplotlib inline
```

### Perform set up steps in your IPython configuration file

To perform the set up steps implicitly for all of your notebooks, add the
following code to your `ipython_config.py` file to register the BigQuery magic
commands and set `matplotlib` to render inline:
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
for more information about IPython configuration.
