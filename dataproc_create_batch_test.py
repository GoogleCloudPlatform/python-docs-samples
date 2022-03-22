import internal_unit_testing

def test_dag_import():
    """Test that the DAG file can be successfully imported.

    This tests that the DAG can be parsed, but does not run it in an Airflow
    environment. This is a recommended confidence check by the official Airflow
    docs: https://airflow.incubator.apache.org/tutorial.html#testing
    """
    from . import dataproc_create_batch as module
    internal_unit_testing.assert_has_valid_dag(module)