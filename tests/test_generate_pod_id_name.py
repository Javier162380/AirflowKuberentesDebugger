

def test_generate_pod_id_name(AirflowtoYamlClient):

    expected_results = 'test_debug'

    results = AirflowtoYamlClient.generate_pod_id_name(pod_name='test')

    assert expected_results == results
