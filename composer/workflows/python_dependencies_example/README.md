# Python dependencies example
 
In this example DAG (`dag.py`), we need to use two Python packages:

1. `scipy`, a PyPI package.
1. `coin_package`, a custom Python package.

First, install `scipy` in your current environment using the installation instructions [here](https://cloud.google.com/composer/docs/how-to/using/installing-python-dependencies). The version is not important.

Then, upload the `dependencies/` directory into your `dags/` GCS bucket. The blank `__init__.py` file within this directory is necessary.

