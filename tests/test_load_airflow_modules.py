import sys


def test_load_airflow_modules(AirflowtoYamlClient):

    AirflowtoYamlClient.load_airflow_modules()

    assert 'example' in sys.modules


def test_load_multiple_airflow_modules(AirflowtoYamlWithoutDefaultArguments):

    AirflowtoYamlWithoutDefaultArguments.load_airflow_modules()

    assert 'example' in sys.modules
    assert 'example_with_airflow_vars' in sys.modules
