import json
import pandas as pd
import subprocess


def df_of_projects():
    """Gets list of project IDs and Project Names from DNA nexus

    Uses the dx toolkit to get a list of all projects in DNA nexus.  Returns dict which can be used to map Project IDs to Project Names

    Returns:
        dictionary: Keys = project IDs, Values = Project Names
    """
    dx_project_string = subprocess.run(
        "dx find projects --json",
        shell=True,
        capture_output=True,
    ).stdout
    dx_project_json = json.loads(dx_project_string)
    # Parse jsons into pandas dataframe
    project_df = pd.json_normalize(dx_project_json)
    # Lookup project IDs in project_df and populate dx_df with human readable names

    return project_df


# Run dx toolkit command to get info for all projects (needed to get human readable project names)
def dictionary_of_projects(project_df):
    """Gets list of project IDs and Project Names from DNA nexus

    Uses the dx toolkit to get a list of all projects in DNA nexus.  Returns dict which can be used to map Project IDs to Project Names

    Returns:
        dictionary: Keys = project IDs, Values = Project Names
    """

    project_dict = dict(zip(project_df["id"], project_df["describe.name"]))

    return project_dict
