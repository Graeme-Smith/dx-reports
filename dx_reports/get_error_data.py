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

parser.add_argument(
    "-s",
    "--start_date",
    type=str,
    help="Start date for importing data",
)

parser.add_argument(
    "-e",
    "--end_date",
    type=str,
    help="End date for importing data",
)

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

    # Build dx toolkit command NOTE: Command defaults to returning 10 results, I've set --num-results to a arbitarily high figure to return all jobs run in time period

    dx_cmd = f"""dx find jobs --all-projects --user {args.user} --json --num-results 10000000 --created-after {args.start_date} --created-after {args.end_date}"""

    # TODO Add support for --tree and --verbose flags

    # Run dx toolkit command to return all jobs in time period and return json

    dx_data_string = subprocess.run(
        dx_cmd,
        shell=True,
        capture_output=True,
    ).stdout

    dx_data_json = json.loads(dx_data_string)

    # Parse jsons into pandas dataframe
    dx_df = pd.json_normalize(dx_data_json)

    # Lookup project IDs in project_df and populate dx_df with human readable names
    project_dict = dictionary_of_projects(df_of_projects())
    dx_df["project_name"] = dx_df["project"].map(project_dict)

    # Convert timestamps to human readable formats
    # Week number, month & year
    dx_df["startedRunningDateTime"] = pd.to_datetime(dx_df["startedRunning"], unit="ms")
    dx_df["startedRunningYear"] = pd.DatetimeIndex(dx_df["startedRunningDateTime"]).year
    dx_df["startedRunningMonth"] = pd.DatetimeIndex(
        dx_df["startedRunningDateTime"]
    ).month
    dx_df["startedRunningWeek"] = pd.DatetimeIndex(
        dx_df["startedRunningDateTime"]
    ).weekofyear
    dx_df["startedRunningMonthName"] = (
        pd.to_datetime(dx_df["startedRunningDateTime"], format="%m")
        .dt.month_name()
        .str.slice(stop=3)
    )

    # Convert month column to catergorical data type (ensures logical ordering in tables and plots)
    # TODO implement the code below in a way that doesn't cause loads of rows with no data.
    # dx_df["startedRunningMonthName"] = dx_df["startedRunningMonthName"].astype(
    #     "category"
    # )
    # dx_df["startedRunningMonthName"] = dx_df[
    #     "startedRunningMonthName"
    # ].cat.set_categories(
    #     [
    #         "Jan",
    #         "Feb",
    #         "Mar",
    #         "Apr",
    #         "May",
    #         "Jun",
    #         "Jul",
    #         "Aug",
    #         "Sep",
    #         "Oct",
    #         "Nov",
    #         "Dec",
    #     ],
    # )

    # Parse project name and classify as production run if name begins 002_ or 802_
    dx_df["productionRunFlag"] = dx_df.project_name.str.contains(
        "^002_", regex=True
    ) | dx_df.project_name.str.contains("^802_", regex=True)

    # Extract mini dataframe with relevant fields
    mini_df = dx_df[
        [
            "id",
            "project",
            "name",
            "executable",
            "executableName",
            "project",
            "productionRunFlag",
            "project_name",
            "state",
            "applet",
            "instanceType",
            "totalPrice",
            "startedRunning",
            "startedRunningYear",
            "startedRunningMonth",
            "startedRunningMonthName",
            "startedRunningWeek",
            "launchedBy",
        ]
    ]

    # Filter out non-production jobs from dataframe
    production_only_df = mini_df[mini_df["productionRunFlag"] == True]

    # Group by relevant criteria

    # General Summary for time period
    summary_groupby_object = production_only_df.groupby(
        ["executableName", "state"]
    ).size()
    summary_groupby_df = summary_groupby_object.reset_index()

    # General Summary per month
    summary_by_month_groupby_object = production_only_df.groupby(
        [
            "executableName",
            "state",
            "startedRunningYear",
            "startedRunningMonthName",
        ]
    ).size()

    summary_by_month_df = summary_by_month_groupby_object.reset_index()

    # General Summary per week
    summary_by_week_groupby_object = production_only_df.groupby(
        [
            "executableName",
            "state",
            "startedRunningYear",
            "startedRunningMonthName",
            "startedRunningWeek",
        ]
    ).size()
    summary_by_week_df = summary_by_week_groupby_object.reset_index()

    # Write dataframes to csv
    dx_df.to_csv(
        f"{args.output_file}_full_data.csv",
        index=False,
    )
    mini_df.to_csv(
        f"{args.output_file}_mini_data.csv",
        index=False,
    )
    summary_groupby_df.to_csv(
        f"{args.output_file}_summary_groupby_df.csv",
        index=False,
    )
    summary_by_month_df.to_csv(
        f"{args.output_file}_summary_by_month_df.csv",
        index=False,
    )
    summary_by_week_df.to_csv(
        f"{args.output_file}_summary_by_week_df.csv",
        index=False,
    )

    # TODO prettify output of groupby in HTML
    # Convert tables to html and save to file
    # summary_groupby_html = summary_groupby_df.to_html(index=True, classes="display")
    # text_file = open(f"{args.output_file}_summary_groupby.html", "w")
    # text_file.write(summary_groupby_html)
    # text_file.close()
    # summary_by_month_html = summary_by_month_df.to_html(index=True, classes="display")
    # text_file = open(f"{args.output_file}_summary_by_month.html", "w")
    # text_file.write(summary_by_month_html)
    # text_file.close()
    # summary_by_week_html = summary_by_week_df.to_html(index=True, classes="display")
    # text_file = open(f"{args.output_file}_summary_by_week.html", "w")
    # text_file.write(summary_by_week_html)
    # text_file.close()

    # Plot data
    # TODO Produce useful plots of data


if __name__ == "__main__":
    main()
