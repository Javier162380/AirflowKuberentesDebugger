import inspect
import os
import sys
from typing import Dict, List, Tuple
import yaml

from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.contrib.kubernetes.pod import Pod
from airflow.contrib.kubernetes.kubernetes_request_factory.pod_request_factory import SimplePodRequestFactory
from airflow.contrib.kubernetes.pod_generator import PodGenerator


class AirflowtoYaml:

    POD_GENERATOR_ATTRIBUTES = inspect.getfullargspec(PodGenerator().make_pod).args
    POD_ATTRIBUTES = tuple(inspect.signature(Pod.__init__).parameters.keys())
    POD_REQUEST_FACTORY = SimplePodRequestFactory()
    POD_ID_SUFFIX = 'debug'
    AIRFLOW_INIT_COMMAND = 'airflow initdb'

    def __init__(self,
                 dag_path: str,
                 dag_name: str = None,
                 destination: str = None,
                 extra_commands: List[str] = []):
        """Instance to generate an AirflowtoYaml object. The instance it is created by
           four parameters, but just one is mandatory. We are going to generate one kubernetes yaml template per
           kubernetes pod operator task present in a Dag.

        Parameters
        ----------
        dag_path : str
            Path where the target dag or dags are place.
        dag_name : str
            Name of the dag we want to analyze.If not specified AirflowtoYaml object it
            is going to generate a template per kubernetes pod operator task
            for each dag persent in the dag_path.
            Default None
        destination : str
           Path where we want to store the yaml files generated.If not specified the yaml
           files are going to be created where the object it is invoked.
           Default None
        extra_commands: list
           Extra variables needed to start a local instance of Airflow. As an example
           if your dag is using custom variables you should set them to be able to
           generate the templating otherwise, the execution it is going to failed.
           Example ['airflow variables --set KUBERNETES_NAMESPACE prod',
                    'airflow variables --set ENVIRONMENT_TAG prod'].
           Default None

        **WARNING
          You should take into account that not when an instance of AirflowtoYaml it is
          created but when the method ```generate_kubernetes_yamls()``` it is trigger
          we are going to start an instance of sqlite with the ```airflow initdb``` command.
          So we can replicate an Airflow enviroment locally.
        """

        self.dag_path = dag_path
        self.dag_name = dag_name
        self.destination = destination
        self.airflow_init_extra_commands = extra_commands

    @property
    def format_dag_name(self):
        if self.dag_name:
            return self.dag_name[:-3] if self.dag_name.endswith('.py') else self.dag_name

    @property
    def airflow_init_commands(self):
        init_commands = [self.AIRFLOW_INIT_COMMAND]
        init_commands.extend(self.airflow_init_extra_commands)

        return ' && '.join(filter(None, init_commands))

    @staticmethod
    def _is_a_python_module(module: str) -> bool:

        return module.endswith('.py') and not module.endswith('__.py')

    @staticmethod
    def _is_a_airflow_kubernetes_operator(operator: object) -> bool:

        return isinstance(operator, KubernetesPodOperator)

    def generate_pod_id_name(self, pod_name: str) -> str:

        return f"{pod_name[:10]}_{self.POD_ID_SUFFIX}"

    def store_airflow_pod_template_in_yaml_file(self, data):

        pod_name = data['metadata']['name']
        pod_abs_path = f"{self.destination}/{pod_name}" if self.destination else pod_name
        with open(f'{pod_abs_path}.yaml', 'w') as outupfile:
            yaml.dump(data, stream=outupfile)

    def init_airflow(self):

        os.system(self.airflow_init_commands)

    def load_airflow_modules(self) -> Tuple[List[Dict]]:

        self.init_airflow()
        sys.path.append(self.dag_path)

        if self.dag_name:
            return ([vars(__import__(self.format_dag_name, locals(), globals()))])

        results = ()

        for module in os.listdir(self.dag_path):
            if self._is_a_python_module(module):
                results = (*results, [vars(__import__(module[:-3], locals(), globals()))])

        return results

    def generate_pod_template(self, operator: KubernetesPodOperator) -> Dict:

        operator_attrs = operator.__dict__
        pod_generator_attrs = {attr: values for attr, values in operator_attrs.items()
                               if attr in self.POD_GENERATOR_ATTRIBUTES}

        pod_generator_attrs['pod_id'] = self.generate_pod_id_name(operator_attrs['name'])

        pod_instance = PodGenerator().make_pod(**pod_generator_attrs)

        pod_attrs = {attr: values for attr, values in operator_attrs.items() if attr in self.POD_ATTRIBUTES}
        for attr in pod_attrs:
            setattr(pod_instance, attr, pod_attrs[attr])

        # TODO. Posible Airflow inconsistency as in the KubernetesPodOperator use the parameter env_Vars and later
        # when the pod is created it is used the convention env.
        if 'env_vars' in operator_attrs:
            setattr(pod_instance, 'envs', operator_attrs['env_vars'])

        return self.POD_REQUEST_FACTORY.create(pod_instance)

    def generate_kubernetes_yamls(self):

        airflow_modules = self.load_airflow_modules()

        for module in airflow_modules:
            for var in module:
                obj = module[var]
                if self._is_a_airflow_kubernetes_operator(obj):
                    pod_template = self.generate_pod_template(obj)
                    self.store_airflow_pod_template_in_yaml_file(pod_template)
