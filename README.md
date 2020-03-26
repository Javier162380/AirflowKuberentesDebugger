# AirflowtoK8S

## Introduction

Sometimes it is really hard to debug Airflow dags when you are using the KubernetesPodOperator object. This package aims to generate a real k8s pod yaml template from an Airflow Kubernetes Pod Operator task. In this way you can get a really easy interface to test if the k8s template it is been correctly generated for your task or tasks, withing your dag, and even you will be able to launch a pod in minikube or a development cluster, before uploading your dag into a production environment, just using the kubernetes apply command.

```bash
kubectl apply -f yourfile.yaml
```

## Basic Usage

To use this library you just need to create an AirflowtoYaml instance follow of these four parameters.

 * dag_path: Path location of the dag. Mandatory.
 * dag_name: Name of the dag you want to debug. If the name it is not specified, it is going to process all the dags present in the dag path. Optional.
 * destination: Path location where the yaml templates are going to be stored. If not specified it is going to store the yaml templates in the same directory where you are executing your code. Optional.
 * extra_commands: airflow commands need to be executed before processing the dags. Use this parameter as an example for setting the variables you are using in the dag. Optional.

Once you create an instance you just need to call generate_kubernetes_yamls method and all the yaml templates will be created.

```python

debug_instance = AirflowtoYaml(dag_path='tests/fixtures',
                         dag_name='example.py',
                         destination='tests/fixtures',
                         extra_commands=['airflow variables --set KUBERNETES_NAMESPACE prod',
                                         'airflow variables --set ENVIRONMENT_TAG prod'])

debug_instance.generate_kubernetes_yamls()
```

## Problem Example

As an example imagine you have this simple dag.
  
  ```python
  
import datetime
from airflow import models
from airflow.contrib.kubernetes import secret
from airflow.contrib.operators import kubernetes_pod_operator

secret_env = secret.Secret(
    deploy_target='SQL_CONN',
    secret='airflow-secrets',
    key='sql_alchemy_conn')

with models.DAG(
        dag_id='composer_sample_kubernetes_pod',
        schedule_interval=datetime.timedelta(days=1),
        start_date=YESTERDAY) as dag:
    kubernetes_secret_vars_ex = kubernetes_pod_operator.KubernetesPodOperator(
        task_id='ex-kube-secrets',
        name='ex-kube-secrets',
        namespace='default',
        image='ubuntu',
        startup_timeout_seconds=300,
        secrets=[secret_env],
        env_vars={'EXAMPLE_VAR': '/example/value'})
    kubernetes_affinity_ex = kubernetes_pod_operator.KubernetesPodOperator(
        task_id='ex-pod-affinity',
        name='ex-pod-affinity',
        namespace='default',
        image='perl',
        cmds=['perl'],
        arguments=['-Mbignum=bpi', '-wle', 'print bpi(2000)'],
        affinity={
            'nodeAffinity': {
                'requiredDuringSchedulingIgnoredDuringExecution': {
                    'nodeSelectorTerms': [{
                        'matchExpressions': [{
                            'key': 'cloud.google.com/gke-nodepool',
                            'operator': 'In',
                            'values': [
                                'pool-0',
                                'pool-1',
                            ]
                        }]
                    }]
                }
            }
        })
    kubernetes_full_pod = kubernetes_pod_operator.KubernetesPodOperator(
        task_id='ex-all-configs',
        name='pi',
        namespace='default',
        image='perl',
        cmds=['perl'],
        arguments=['-Mbignum=bpi', '-wle', 'print bpi(2000)'],
        secrets=[],
        labels={'pod-label': 'label-name'},
        startup_timeout_seconds=120,
        env_vars={'EXAMPLE_VAR': '/example/value'},
        get_logs=True,
        annotations={'key1': 'value1'},
        config_file='/home/airflow/composer_kube_config',
        volumes=[],
        volume_mounts=[],
        affinity={})
  
  ```
  
The problem here is that you are using a python object that is rendered into a python dictionary, which in the end it is going to be used to make a post request to the kubernetes api to generate a pod. It can be problematic to know if you are rendering arguments correctly or how the different k8s objects have been referenced.
  
Using AirflowtoK8s will generate the following templates from this file.
  
  ex-kube-secrets.yaml

  ```yaml
apiVersion: v1
kind: Pod
metadata:
  annotations: {}
  labels: {}
  name: ex-kube-secrets
  namespace: default
spec:
  affinity: {}
  containers:
  - args: []
    command: []
    env:
    - name: EXAMPLE_VAR
      value: /example/value
    - name: SQL_CONN
      valueFrom:
        secretKeyRef:
          key: sql_alchemy_conn
          name: airflow-secrets
    image: ubuntu
    imagePullPolicy: IfNotPresent
    name: base
    ports: []
  nodeSelector: {}
  restartPolicy: Never
  serviceAccountName: default
  volumes: []
  ```
  
  ex-pod-affinity.yaml
  
  ```yaml
apiVersion: v1
kind: Pod
metadata:
  annotations: {}
  labels: {}
  name: ex-pod-affinity
  namespace: default
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: cloud.google.com/gke-nodepool
            operator: In
            values:
            - pool-0
            - pool-1
  containers:
  - args:
    - -Mbignum=bpi
    - -wle
    - print bpi(2000)
    command:
    - perl
    image: perl
    imagePullPolicy: IfNotPresent
    name: base
    ports: []
  nodeSelector: {}
  restartPolicy: Never
  serviceAccountName: default
  volumes: []

  ```
  
  pi.yaml
  
  ```yaml
apiVersion: v1
kind: Pod
metadata:
  annotations:
    key1: value1
  labels:
    pod-label: label-name
  name: pi
  namespace: default
spec:
  affinity: {}
  containers:
  - args:
    - -Mbignum=bpi
    - -wle
    - print bpi(2000)
    command:
    - perl
    env:
    - name: EXAMPLE_VAR
      value: /example/value
    image: perl
    imagePullPolicy: Always
    name: base
    ports: []
    resources:
      limits:
        cpu: 1
        memory: 1
  nodeSelector: {}
  restartPolicy: Never
  serviceAccountName: default
  volumes: []

  ```
  
 Note that all the yaml files generated are going to have the same name as the name argument of the KubernetesPodOperator object.
  
## WARNINGS
  
* Take into account that every time your AirflowtoYaml instance called generate_kubernetes_yamls method you are going to run and airflow local instance with sqllite so a bash process with the ```ariflow initdb```  command it is going to be launch.

* By default, we are not connected to any kubernetes cluster so we are using the default service account value. If you want to run the template generated into an Airflow Cluster you need to add the cluster service account.

* Right now the library just supports Airflow version >= 1.10.9 and the extras of kubernetes and gcp. If in the dag you are using other kinds of library as boto3 probably you are going to need to install it before using it.

## Installation

The package is not yet available in py-pi so you need to install it from github , using the protocol you want.

* https:

```bash
pip install  git+https://github.com/Javier162380/AirflowKuberentesDebugger.git@<tag-name(currently0.1.0)>#egg=airflowkubernetesdebugger
```

* ssh:

``` bash
pip install git+ssh://git@github.com/coverwallet/AirflowKuberentesDebugger.git@<tag_name>#egg=airflowkubernetesdebugger
```
