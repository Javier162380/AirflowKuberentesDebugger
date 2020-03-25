import os


def test_store_airflow_pod_template_in_yaml_file(mocker, AirflowtoYamlClient):

    template = {'apiVersion': 'v1', 'kind': 'Pod', 'metadata': {'name': 'pod-ex-minimum', 'labels': {},
                                                                'annotations': {}},
                'spec':
                    {
        'containers':
                [{'name': 'base', 'image': 'gcr.io/gcp-runtimes/ubuntu_18_0_4', 'command': ['echo'],
                  'imagePullPolicy': 'IfNotPresent', 'args': [],
                  'ports': []}],
                'restartPolicy': 'Never', 'nodeSelector': {},
                'volumes': [],
                'serviceAccountName': 'default', 'affinity': {}}}

    AirflowtoYamlClient.store_airflow_pod_template_in_yaml_file(data=template)

    execution_file = os.path.dirname(__file__)
    assert os.path.isfile(f"{execution_file}/outputs/pod-ex-minimum.yaml") == True
