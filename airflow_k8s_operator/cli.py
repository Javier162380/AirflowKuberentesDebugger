import ast
import argparse


def cli():

    parser = argparse.ArgumentParser(description=f"AirflowtoYaml default tool to generate k8s"
                                                 f"templates from an Airflow dag")

    parser.add_argument("--dag-path",
                        help="Path where we can find different airflow dags",
                        required=True)

    parser.add_argument("--dag-name",
                        help="Name of the dag we want to extract data into a yaml file."
                        "If not specified we will generate k8s templates for all the dags "
                        "in the path. Default: None",
                        required=False,
                        default=None)

    parser.add_argument("--destination",
                        help="Path where we want to locate the yamls generated"
                        "If not specified we are going to use the current directory,"
                        "Default: None",
                        required=False,
                        default=None)

    parser.add_argument("--extra-commands",
                        help="Extra commands that need to be executed before loading airflow modules."
                        "Use this command to load the specific configuration needed for the dag,"
                        "As an example set variables.",
                        required=False,
                        type=ast.literal_eval,
                        default=None)

    return parser.parse_args()
