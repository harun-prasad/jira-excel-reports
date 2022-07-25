jira_server = "https://bzpay-platform.atlassian.net"
jira_username = "harun.paramasivam@bztrack.com"
jira_password = "j2rr5vEF55aHC60RAf4x8701" # Token

work_log_start_date = '2022-07-01' 
work_log_end_date = '2022-07-30'

jira_worklog_users = ["harun.paramasivam@bztrack.com", "anbarasan.m@bztrack.com", 
                        "rajasingh.selvakumar@bztrack.com", "jebasingh.dharmaraj@bztrack.com", 
                        "pradeep.rajkumar@bztrack.com", "kasirajan.venkatesan@bztrack.com"] #, 
                        # "dhakshinamoorthy.alagu@bztrack.com", "kirubhaharan.murugesan@bztrack.com"] 


# Settings for Email
EMAIL_WORKLOG = True
SENDGRID_KEY = "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"
EMAIL_TO = "harun@bztrack.com"


import utils.general_utils
work_log_start_date = utils.general_utils.date_from_string(work_log_start_date)
work_log_end_date = utils.general_utils.date_from_string(work_log_end_date)
