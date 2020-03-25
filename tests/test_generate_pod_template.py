from airflow.contrib.kubernetes.kubernetes_request_factory.pod_request_factory import SimplePodRequestFactory
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator


def test_generate_pod_template_integration(AirflowtoYamlClient):

    expected_results = {'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': 'prod', 'labels': {}, 'annotations': {}}, 'spec': {'containers': [{'name': 'base', 'image': 'prod', 'command': [
    ], 'imagePullPolicy': 'IfNotPresent', 'args': [], 'ports': []}], 'restartPolicy': 'Never', 'nodeSelector': {}, 'volumes': [], 'serviceAccountName': 'default', 'affinity': {}}}

    operator = KubernetesPodOperator(namespace='prod', image='prod', name='prod', task_id='prod')

    results = AirflowtoYamlClient.generate_pod_template(operator=operator)

    results == expected_results
