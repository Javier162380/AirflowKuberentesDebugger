import inspect
import os
import sys
from typing import List, Dict, Tuple
import yaml

from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.contrib.kubernetes.pod import Pod
from airflow.contrib.kubernetes.kubernetes_request_factory.pod_request_factory import SimplePodRequestFactory


class AirflowtoYaml:

    POD_ATTRIBUTES = tuple(inspect.signature(Pod.__init__).parameters.keys())
    POD_REQUEST_FACTORY = SimplePodRequestFactory()

    def __init__(self,
                 dag_path: str,
                 dag_name: str = None,
                 destination: str = None,
                 extra_commands: List[str] = None):

        self.dag_path = dag_path
        self.dag_name = dag_name
        self.destination = destination
        self.airflow_init_extra_commands = extra_commands

    @property
    def format_dag_name(self):

        return self.dag_name[:-3] if self.dag_name.endswith('.py') else self.dag_name

    @staticmethod
    def _is_a_python_module(module: str) -> bool:

        return module.endswith('.py') and not module.endswith('__.py')

    @staticmethod
    def _is_a_airflow_kubernetes_operator(operator: object) -> bool:

        return isinstance(operator, KubernetesPodOperator)

    def store_airflow_pod_template_in_yaml_file(self, data):

        pod_name = data['metadata']['name']
        pod_abs_path = f"{self.destination}/{pod_name}" if self.destination else pod_name
        with open(f'{pod_abs_path}.yaml', 'w') as outupfile:
            yaml.dump(data, stream=outupfile)

    def init_airflow(self):

        os.system('airflow initdb')

        if self.airflow_init_extra_commands:
            for command in self.airflow_init_extra_commands:
                os.system(command)

    def load_airflow_modules(self) -> Tuple[List[Dict]]:

        self.init_airflow()
        sys.path.append(self.dag_path)

        if self.dag_name:
            return ([vars(__import__(self.format_dag_name, locals(), globals()))])

        results = ()

        for module in os.listdir(self.dag_path):
            if self._is_a_python_module(module):
                results += ((vars(__import__(module[:-3], locals(), globals()))))

        return results

    def generate_pod_template(self, operator: KubernetesPodOperator) -> Dict:

        operator_attrs = operator.__dict__
        pod_attrs = {attr: values for attr, values in operator_attrs.items() if attr in self.POD_ATTRIBUTES}

        # TODO: possible bug in airflow.
        if not 'envs' in pod_attrs:
            pod_attrs['envs'] = {}

        pod_instance = Pod(**(pod_attrs))
        return self.POD_REQUEST_FACTORY.create(pod_instance)

    def generte_kubernetes_yamls(self):

        airflow_modules = self.load_airflow_modules()

        for module in airflow_modules:
            for var in module:
                obj = module[var]
                if self._is_a_airflow_kubernetes_operator(obj):
                    pod_template = self.generate_pod_template(obj)
                    self.store_airflow_pod_template_in_yaml_file(pod_template)
