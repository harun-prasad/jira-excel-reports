import json
from jira import JIRA
import datetime

# Project imports
import utils.general_utils
import task_helper

task_helper_obj = task_helper.TaskHelper.get_instance()

class JiraHelper:
    def __init__(self, server, username, password):
        self.jira = JIRA({"server" : server}, basic_auth=(username, password))
        self.clear()

    def clear(self):
        self.worklogged_issues = []
        self.worklog_start_date = None
        self.worklog_end_date = None
        self.high_worklog_tasks = None
        self.worklogged_dates = []
    

    def search_issues_jql(self, worklog_users, worklog_start_date, worklog_end_date, additional_fields):
        self.clear()
        jql_string = ""
        if worklog_users and len(worklog_users) > 0:
            #TODO Add logic to verify the users in JIRA server if users not in list raise value error
            #TODO Add logic to check type of worklog_users to be list or tuple. If givne as string with user list separated with comma, then convert it to list
            if jql_string != "": jql_string+= " and "
            jql_string+= "worklogAuthor in ("+json.dumps(worklog_users)[1:-1]+")"
        if worklog_start_date:
            if jql_string != "": jql_string+= " and "
            jql_string+= 'worklogDate >= "'+datetime.datetime.strftime(worklog_start_date, "%Y-%m-%d")+'"'
        if worklog_end_date:
            if jql_string != "": jql_string+= " and "
            jql_string+= 'worklogDate <= "'+datetime.datetime.strftime(worklog_end_date, "%Y-%m-%d")+'"'
        start_at_counter = 0 # Issue start counter
        while True:
            # Returns 100 issues at a time, so looping to get rest of the issues
            issues = self.jira.search_issues(jql_string, startAt=start_at_counter, fields="summary,worklog,issuetype,parent,project,status,labels", maxResults=100)
            self.worklogged_issues += issues
            if len(issues) != 100: break
            start_at_counter += len(issues)
        self.worklog_start_date = worklog_start_date
        self.worklog_end_date = worklog_end_date
        return self.worklogged_issues

    def get_userwise_worklogs(self):
        # Format {user: {date: {task: {"worklog_hours": worklog_hours, "worklog_text": worklog_text}}}}
        if not self.worklogged_issues:
            raise Exception("Issues need to get before processing this function")
        userwise_worklog = {}
        high_worklog_tasks = []

        for issue in self.worklogged_issues:
            task_id = issue.key
            print(task_id)
            task_name = issue.fields.summary
            task_type = issue.fields.issuetype.name
            task_labels = issue.fields.labels
            if not task_helper_obj.check_task_exists(task_id):
                task_helper_obj.add_task(task_id, task_name, task_type, task_labels)
            else:
                #if task already present, then probably duplicates
                print("Duplicate task " + task_id)
                continue
            if issue.fields.worklog.total > issue.fields.worklog.maxResults:
                high_worklog_tasks.append(task_id)
                issue_worklogs = self.jira.worklogs(task_id)
            else:
                issue_worklogs = issue.fields.worklog.worklogs
            #print(task_id, len(issue_worklogs))
            for worklog in issue_worklogs:
                worklog_date = datetime.datetime.strptime(worklog.started[:10], "%Y-%m-%d")
                if worklog_date < self.worklog_start_date or worklog_date > self.worklog_end_date:
                    continue
                worklog_date_str = worklog.started[:10]
                if worklog_date_str not in self.worklogged_dates:
                    self.worklogged_dates.append(worklog_date_str)
                user = worklog.author.key
                worklog_hours = worklog.timeSpentSeconds/60.0/60.0
                worklog_text = "(" + worklog.timeSpent + ") " + getattr(worklog, "comment", "")
                worklog_id = worklog.id
                if user not in userwise_worklog: userwise_worklog[user] ={}
                if worklog_date_str not in userwise_worklog[user]: userwise_worklog[user][worklog_date_str] = {}
                if task_id not in userwise_worklog[user][worklog_date_str]: userwise_worklog[user][worklog_date_str][task_id] = {}
                if worklog_hours not in userwise_worklog[user][worklog_date_str][task_id]:
                    userwise_worklog[user][worklog_date_str][task_id] = {"worklog_hours": worklog_hours, "worklog_text": worklog_text}
                else:
                    userwise_worklog[user][worklog_date_str][task_id]["worklog_hours"] += worklog_hours
                    userwise_worklog[user][worklog_date_str][task_id]["worklog_text"] += "\n" + worklog_text
        self.userwise_worklog = userwise_worklog
        self.high_worklog_tasks = high_worklog_tasks
