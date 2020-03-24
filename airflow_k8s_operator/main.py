from cli import cli
import AirflowtoYaml


def main():

    params = cli()

    AirflowtoYamlInstance = AirflowtoYaml(dag_path=params.dag_path, dag_name=params.dag_name,
                                          destination=params.destination,
                                          extra_commands=params.extra_commands)

    AirflowtoYamlInstance.generte_kubernetes_yamls()


if __name__ == "__main__":
    main()
