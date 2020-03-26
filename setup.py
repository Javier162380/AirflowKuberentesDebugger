from setuptools import setup

meta = {}
exec(open('./airflow_k8s_operator/version.py').read(), meta)

setup(name='airflow_k8s_operator',
      description='Package to debug Airflow Kuberentes Pod Operator generating a Yaml file',
      version=meta['__version__'],
      author='@javier162380',
      license='MIT',
      packages=['airflow_k8s_operator'],
      install_requires=[
          'apache-airflow==1.10.9',

      ])
