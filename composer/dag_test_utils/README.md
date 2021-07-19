# Cloud Composer DAG Testing Utility

This package is used internally to unit test the validity of all Cloud Composer sample DAGs. It is not supported for external production use. The [latest release can be found on PyPI](https://pypi.org/project/cloud-composer-dag-test-utils/).

## Instructions

Add the following to your `requirements-test.txt` file:

`cloud_composer_dag_test_utils`

Import the internal unit testing module

```python
import internal_unit_testing
```

Test your DAG

```python
def test_dag_import():
    # Set any variables if your DAG requires them
    models.Variable.set('gcs_bucket', 'example_bucket')
    from . import my_dag as module
    # Check for DAG validity
    internal_unit_testing.assert_has_valid_dag(module)
```

For more examples, refer to the [`workflows`](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/composer/workflows) directory.


