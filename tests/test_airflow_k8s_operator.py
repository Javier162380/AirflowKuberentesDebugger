from airflow_k8s_operator import __version__


def test_version():
    assert __version__ == '0.1.0'


def test_airflow_k8s_operator_instance(AirflowtoYamlClient):

    assert AirflowtoYamlClient.dag_path == 'tests/fixtures'
    assert AirflowtoYamlClient.dag_name == 'example.py'
    assert AirflowtoYamlClient.destination == 'tests/fixtures'
    assert AirflowtoYamlClient.format_dag_name == 'example'
    assert AirflowtoYamlClient.airflow_init_extra_commands == []
    assert AirflowtoYamlClient.airflow_init_commands == 'airflow initdb'


def test_airflow_k8s_operator_instance_with_extra_commands(AirflowtoYamlClientExtraCommands):

    assert AirflowtoYamlClientExtraCommands.dag_path == 'tests/fixtures'
    assert AirflowtoYamlClientExtraCommands.dag_name == 'example.py'
    assert AirflowtoYamlClientExtraCommands.destination == 'tests/fixtures'
    assert AirflowtoYamlClientExtraCommands.format_dag_name == 'example'
    assert AirflowtoYamlClientExtraCommands.airflow_init_extra_commands == [
        'airflow variables --set KUBERNETES_NAMESPACE prod', 'airflow variables --set ENVIRONMENT_TAG prod']
    assert AirflowtoYamlClientExtraCommands.airflow_init_commands == 'airflow initdb && airflow variables --set KUBERNETES_NAMESPACE prod && airflow variables --set ENVIRONMENT_TAG prod'


def test_airflow_k8s_operator_instance_without_default_arguments(AirflowtoYamlWithoutDefaultArguments):
    assert AirflowtoYamlWithoutDefaultArguments.dag_path == 'tests/fixtures'
    assert AirflowtoYamlWithoutDefaultArguments.dag_name == None
    assert AirflowtoYamlWithoutDefaultArguments.destination == None
    assert AirflowtoYamlWithoutDefaultArguments.format_dag_name == None
    assert AirflowtoYamlWithoutDefaultArguments.airflow_init_commands == 'airflow initdb'
