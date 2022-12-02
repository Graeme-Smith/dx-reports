# Script Instructions

## About DX error reporting

This script will return a summary of all completed and failed jobs for the given period

### get_error_data.py Usage

User must have the dx-toolkit installed and be logged in as mokaguys using dx login.

'''bash
python3 get_error_data.py --output_file testResultsNov2022 --user mokaguys --start_date 2022-10-1 --end_date 2022-11-1
'''

### get_error_data.py Output

*_full_data.csv - full data set exported for time period
*_mini_data.csv - pertinent columns from full dataframe

*_summary_by_week_df.csv - summary by week for time frame specified
*_summary_by_month_df.csv - summary by month for time frame specified

### get_error_data.py Limitations

* dx find jobs flags --tree and --verbose are not currently supported
* script currently requires user to login to dx login.  This would be better inplemented by providing the user name and auth key in a config file.
* dx find jobs only returns 10 jobs as default - hacky work around is to set --num-results to arbitarily high number
* script currently does not plot results
* script does not currently support prettified html tables of groupby objects
* script does not currently support linking failed jobs to when they have been rerun - this would allow the delay caused by the result to be automatically calculated.
* The month column "Jan", "Feb", "Mar" etc would benefit from being categorigal data type - this ensures it is sorted correctly in tables and plots.  Unfortunately my code for this adds lines for each of these 12 months even when they are not included in the time period looked at.  This means lots of lines in the tables with 0 jobs for those months with no data imported.  Have currently disabled this feature while I think of a workaround.

## About getting list of Dev Projects

This script will return a summary of all development projects

### get_dev_projects.py Usage

User must have the dx-toolkit installed and be logged in as mokaguys using dx login.

'''bash
python3 get_dev_projects.py --output_file testResultsNov2022 --user mokaguys
'''

### get_dev_projects.py Output

*_dev_project.csv

### get_dev_projects.py Limitations

Only returns projects which have given mokaguys access
