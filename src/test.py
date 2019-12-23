import openpyxl
import re
import requests

#project libraries
import jx_config
import jira_helper
import xlsx_helper
import utils.general_utils
import utils.requests_logging

#Code Starts Here
#utils.requests_logging.debug_requests_on()

jira = jira_helper.JiraHelper(jx_config.jira_server, jx_config.jira_username, jx_config.jira_password)

workloged_issues = jira.search_issues_jql(jx_config.jira_worklog_users, jx_config.work_log_start_date, jx_config.work_log_end_date, additional_fields="summary,worklog,issuetype,parent,project,status")

jira.get_userwise_worklogs()

xlsx = xlsx_helper.XlsxHelper()
xlsx.create_report_template(jx_config.jira_worklog_users, jx_config.work_log_start_date, jx_config.work_log_end_date, jira.worklogged_dates)
xlsx.populate_report(jira.userwise_worklog, jira.worklogged_dates)
xlsx.save()


print(workloged_issues.__len__(), type(workloged_issues))