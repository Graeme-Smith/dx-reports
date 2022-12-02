import argparse
import json
import pandas as pd
import subprocess
from dx_reports.helper_functions import dictionary_of_projects, df_of_projects


# Import command line arguments
parser = argparse.ArgumentParser(description="Get DNA nexus job data")

# TODO add config file to import DNA nexus token and user name (currently relies upon users to dx login as mokaguys.)

# parser.add_argument(
#     "-a",
#     "--auth_token",
#     type=str,
#     help="DNA Nexus Auth Token",
# )

# parser.add_argument(
#     "-s",
#     "--start_date",
#     type=str,
#     help="Start date for importing data",
# )

# parser.add_argument(
#     "-e",
#     "--end_date",
#     type=str,
#     help="End date for importing data",
# )

parser.add_argument(
    "-o",
    "--output_file",
    type=str,
    help="Prefix to use for output files",
)

parser.add_argument(
    "-u",
    "--user",
    type=str,
    help="DNA nexus user",
)


def main():

    args = parser.parse_args()

    project_df = df_of_projects()  # Get a

    project_df = project_df[
        [
            "id",
            "describe.name",
            "describe.created",
            "describe.dataUsage",
            "describe.createdBy.user",
            "describe.storageCost",
        ]
    ]
    project_df["describe.created"] = pd.to_datetime(
        project_df["describe.created"], unit="ms"
    )

    project_df = project_df[project_df["describe.name"].str.startswith("003_")]
    project_df = project_df.sort_values(
        by=["describe.createdBy.user", "describe.storageCost"]
    )

    project_df.to_csv(
        f"{args.output_file}_dev_projects.csv",
        index=False,
    )


if __name__ == "__main__":
    main()
