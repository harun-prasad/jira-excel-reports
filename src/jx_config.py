jira_server = "https://jadeonegroup.atlassian.net"
jira_username = "harun.paramasivam@tappit.com"
jira_password = "73sgQQ13TSLbmJoyKTzGC954" # Token

jira_worklog_users = ["chitra.pachayappan","gopi.kirupanithi","harun.paramasivam","malarmannan.polappan","rajapallavan.jayabalan","sakthivel.gunasekaran"] 
work_log_start_date = '2019-12-09' 
work_log_end_date = '2019-12-16'


import utils.general_utils
work_log_start_date = utils.general_utils.date_from_string(work_log_start_date)
work_log_end_date = utils.general_utils.date_from_string(work_log_end_date)
