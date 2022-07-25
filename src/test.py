import openpyxl
import re
import requests
import datetime

#project libraries
import jx_config
import jira_helper
import xlsx_helper
import utils.general_utils
import utils.requests_logging
import sendgrid_email

#Code Starts Here
#utils.requests_logging.debug_requests_on()

jira = jira_helper.JiraHelper(jx_config.jira_server, jx_config.jira_username, jx_config.jira_password)

workloged_issues = jira.search_issues_jql(jx_config.jira_worklog_users, jx_config.work_log_start_date, jx_config.work_log_end_date, additional_fields="summary,worklog,issuetype,parent,project,status")

jira.get_userwise_worklogs()
xls_file_name = "jira_worklog"+ datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".xlsx"
xlsx = xlsx_helper.XlsxHelper(xls_file_name)
xlsx.create_report_template(jx_config.jira_worklog_users, jx_config.work_log_start_date, jx_config.work_log_end_date, jira.worklogged_dates)
xlsx.populate_report(jira.userwise_worklog, jira.worklogged_dates)
xlsx.save()

if jx_config.EMAIL_WORKLOG:
    sendgrid = sendgrid_email.Sendgrid_Email(jx_config.SENDGRID_KEY)
    result = sendgrid.send_email(jx_config.EMAIL_TO, "support@bztrack.com", xls_file_name)
    print (result)
    
print(workloged_issues.__len__(), type(workloged_issues))