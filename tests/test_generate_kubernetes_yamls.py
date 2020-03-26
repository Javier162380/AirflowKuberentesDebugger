from unittest.mock import call
from airflow_k8s_operator import AirflowtoYaml


def test_generate_pod_template_integration(mocker, AirflowtoYamlClient):
    mocker.patch.object(AirflowtoYaml, 'store_airflow_pod_template_in_yaml_file')
    expected_calls = [
        {'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': 'pod-ex-minimum', 'labels': {},
                                                         'annotations': {}},
         'spec':
         {
            'containers':
            [{'name': 'base', 'image': 'gcr.io/gcp-runtimes/ubuntu_18_0_4', 'command': ['echo'],
              'imagePullPolicy': 'IfNotPresent', 'args': [],
              'ports': []}],
            'restartPolicy': 'Never', 'nodeSelector': {},
            'volumes': [],
            'serviceAccountName': 'default', 'affinity': {}}},
        {'apiVersion': 'v1', 'kind': 'Pod', 'metadata':
         {'name': 'ex-kube-templates', 'labels': {},
          'annotations': {}},
         'spec':
         {
             'containers':
             [{'name': 'base', 'image': 'bash', 'command': ['echo'],
               'imagePullPolicy': 'IfNotPresent', 'args': ['{{ ds }}'],
               'env': [{'name': 'MY_VALUE', 'value': '{{ var.value.my_value }}'}],
               'ports': []}],
             'restartPolicy': 'Never', 'nodeSelector': {},
             'volumes': [],
             'serviceAccountName': 'default', 'affinity': {}}},
        {'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': 'ex-kube-secrets', 'labels': {},
                                                         'annotations': {}},
         'spec':
         {
            'containers':
            [{'name': 'base', 'image': 'ubuntu', 'command': [],
              'imagePullPolicy': 'IfNotPresent', 'args': [],
              'env':
              [{'name': 'EXAMPLE_VAR', 'value': '/example/value'},
               {'name': 'SQL_CONN', 'valueFrom':
                  {'secretKeyRef': {'name': 'airflow-secrets', 'key': 'sql_alchemy_conn'}}}],
                'ports': []}],
            'restartPolicy': 'Never', 'nodeSelector': {},
            'volumes': [],
            'serviceAccountName': 'default', 'affinity': {}}},
        {'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': 'ex-pod-affinity', 'labels': {},
                                                         'annotations': {}},
         'spec':
         {
            'containers':
            [{'name': 'base', 'image': 'perl', 'command': ['perl'],
              'imagePullPolicy': 'IfNotPresent', 'args': ['-Mbignum=bpi', '-wle', 'print bpi(2000)'],
              'ports': []}],
            'restartPolicy': 'Never', 'nodeSelector': {},
            'volumes': [],
            'serviceAccountName': 'default',
            'affinity':
            {
                'nodeAffinity':
                {
                    'requiredDuringSchedulingIgnoredDuringExecution':
                    {
                        'nodeSelectorTerms':
                        [{
                            'matchExpressions':
                            [{'key': 'cloud.google.com/gke-nodepool', 'operator': 'In', 'values': ['pool-0', 'pool-1']}]}]}}}}},
        {'apiVersion': 'v1', 'kind': 'Pod',
         'metadata': {'name': 'pi', 'labels': {'pod-label': 'label-name'},
                      'annotations': {'key1': 'value1'}},
         'spec':
         {
             'containers':
             [{'name': 'base', 'image': 'perl', 'command': ['perl'],
               'imagePullPolicy': 'Always', 'args': ['-Mbignum=bpi', '-wle', 'print bpi(2000)'],
               'env': [{'name': 'EXAMPLE_VAR', 'value': '/example/value'}],
               'ports': [],
               'resources': {'limits': {'memory': 1, 'cpu': 1}}}],
             'restartPolicy': 'Never', 'nodeSelector': {},
             'volumes': [],
             'serviceAccountName': 'default', 'affinity': {}}}]

    AirflowtoYamlClient.generate_kubernetes_yamls()

    expected_calls = [call(expected_call) for expected_call in expected_calls]
    AirflowtoYaml.store_airflow_pod_template_in_yaml_file.assert_has_calls(expected_calls)
