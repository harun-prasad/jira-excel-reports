import datetime

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)+1):
        yield start_date + datetime.timedelta(n)

def validate_datestring(date_string, dateformat="%Y-%m-%d"):
    try:
        datetime.datetime.strptime(date_string, dateformat)
    except ValueError:
        raise ValueError(date_string + " not in required date format 'YYYY-MM-DD'")

def date_from_string(date_string, dateformat="%Y-%m-%d"):
    try:
        return datetime.datetime.strptime(date_string, dateformat)
    except ValueError:
        raise ValueError(date_string + " not in required date format 'YYYY-MM-DD'")

