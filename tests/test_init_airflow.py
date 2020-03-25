import os


def test_init_airflow(mocker, AirflowtoYamlClient):
    mocker.patch.object(os, 'system')

    AirflowtoYamlClient.init_airflow()

    os.system.assert_called_once_with('airflow initdb')


def test_init_airflow_with_envvars(mocker, AirflowtoYamlClientExtraCommands):
    mocker.patch.object(os, 'system')

    AirflowtoYamlClientExtraCommands.init_airflow()

    os.system.assert_called_once_with(
        'airflow initdb && airflow variables --set KUBERNETES_NAMESPACE prod && airflow variables --set ENVIRONMENT_TAG prod')
