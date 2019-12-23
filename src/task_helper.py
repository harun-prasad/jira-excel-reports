class TaskHelper:
    __instance = None

    @staticmethod
    def get_instance():
        if TaskHelper.__instance == None:
            TaskHelper()
        return TaskHelper.__instance

    def __init__(self):
        if TaskHelper.__instance != None:
            raise Exception("TaskHelper is a singleton class")
        else:
            TaskHelper.__instance = self
        self.clear()
    
    def clear(self):
        self.tasks = {}

    def check_task_exists(self, task_id):
        return task_id in self.tasks

    def add_task(self, task_id, task_name, task_type, task_labels):
        self.tasks[task_id] = Task(task_id, task_name, task_type, task_labels)
    
    def get_task(self, task_id):
        if self.check_task_exists(task_id):
            return self.tasks[task_id]
        raise Exception(task_id + " doesn't exists")

    def get_day_total_worklog_hours(self,day_tasks_dict):
        """
        Sums the worklog hours without rounding or ceiling
        """
        day_total_worklog_hours = 0
        for task_id in day_tasks_dict:
            day_total_worklog_hours += day_tasks_dict[task_id]["worklog_hours"]
        return day_total_worklog_hours
    
    def sort_task_by_work_log_hours(self, day_tasks_dict):
        # added 1 second before rounding as because of float issue in computers (round(2.5) = 2 where as round(3.5) = 4)
        tasks = [[k, v["worklog_hours"], round((v["worklog_hours"]*60.0*60.0+1)/60.0/60.0)] for k,v in day_tasks_dict.items()]
        sorted_tasks = sorted(tasks, reverse = True, key = lambda task_tuple: task_tuple[1])
        return sorted_tasks

    def find_task_across_days(self, day1_tasks_dict, day2_tasks_dict):
        task_across_days = ""
        task_across_days_hours = 0
        for day1_task in day1_tasks_dict:
            if day1_task in day2_tasks_dict and day2_tasks_dict[day1_task]["worklog_hours"] > task_across_days_hours:
                task_across_days = day1_task
                task_across_days_hours = day2_tasks_dict[day1_task]["worklog_hours"]
        return task_across_days

class Task():
    def __init__(self, id, name, task_type, labels):
        self.id = id
        self.name = name
        self.task_type = task_type # type is an inbuild keywork hence using task_type as variale name
        self.labels = labels
