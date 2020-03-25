import pytest

from airflow_k8s_operator import AirflowtoYaml
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator


@pytest.fixture()
def AirflowtoYamlClient():

    return AirflowtoYaml(dag_path='tests/fixtures',
                         dag_name='example.py',
                         destination='tests/outputs')


@pytest.fixture()
def AirflowtoYamlClientExtraCommands():

    return AirflowtoYaml(dag_path='tests/fixtures',
                         dag_name='example.py',
                         destination='tests/fixtures',
                         extra_commands=['airflow variables --set KUBERNETES_NAMESPACE prod',
                                         'airflow variables --set ENVIRONMENT_TAG prod'])


@pytest.fixture()
def AirflowtoYamlWithoutDefaultArguments():

    return AirflowtoYaml(dag_path='tests/fixtures')
