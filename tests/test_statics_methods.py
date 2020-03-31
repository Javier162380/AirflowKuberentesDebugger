from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.models import DAG


def test_is_a_python_module(AirflowtoYamlClient):

    python_module = 'example.py'
    python_not_valid_module = '__init__.py'
    other_format_module = 'reikiavik.csv'

    python_module_results = AirflowtoYamlClient._is_a_python_module(python_module)
    python_not_valid_module_results = AirflowtoYamlClient._is_a_python_module(python_not_valid_module)
    other_format_module_results = AirflowtoYamlClient._is_a_python_module(other_format_module)

    assert python_module_results == True
    assert python_not_valid_module_results == False
    assert other_format_module_results == False


def test_is_a_airflow_kubernetes_operator(AirflowtoYamlClient):

    string_object = str
    kubernetes_operator = KubernetesPodOperator(namespace='prod', image='prod', name='prod', task_id='prod')

    string_object_results = AirflowtoYamlClient._is_a_airflow_kubernetes_operator(string_object)
    kubernetes_operator_results = AirflowtoYamlClient._is_a_airflow_kubernetes_operator(kubernetes_operator)

    assert string_object_results == False
    assert kubernetes_operator_results == True


def test_is_a_airflow_dag_object(AirflowtoYamlClient):

    string_object = str
    dag = DAG('test', 'test dag')

    string_object_results = AirflowtoYamlClient._is_a_airflow_dag(string_object)
    dag_results = AirflowtoYamlClient._is_a_airflow_dag(dag)

    assert string_object_results == False
    assert dag_results == True
