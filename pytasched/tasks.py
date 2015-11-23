import json
from pytasched.tools import get_duration


class Task(object):
    """
    Container for all task specific information
    """

    def __init__(self, task, args=None, kwargs=None, id=None, wait=None,
                 recurring=False, days=0, hours=0, minutes=0, seconds=0,
                 millis=0):
        """
        Create a new task. Should be used with the configured task engine in
        mind.

        :param str task: The task to be executed
        :param list args: Arguments to pass to the task
        :param dict kwargs: Keyword arguments to pass to the task
        :param str id: Task ID
        :param float wait: Number of seconds from now until execution
        :param bool recurring: If the task should be recurring
        :param float days: Define duration in days
        :param float hours: Define duration in hours
        :param float minutes: Define duration in minutes
        :param float seconds: Define duration in seconds
        :param float millis: Define duration in milliseconds
        :return:
        """
        self.task = task
        self.args = args
        self.kwargs = kwargs
        self.id = id
        self.recurring = recurring

        if wait:
            self.wait = wait
        else:
            self.wait = get_duration(days, hours, minutes, seconds, millis)

    def get_args(self):
        """
        Get the task args to be used in function calling
        :return list:
        """
        return self.args if self.args else []

    def get_kwargs(self):
        """
        Get the task kwargs to be used in function calling
        :return dict:
        """
        return self.kwargs if self.kwargs else {}

    def __str__(self):
        return '<Task ({})>'.format(json.dumps({
            "id": self.id,
            "task": self.task,
            "args": self.args,
            "kwargs": self.kwargs,
            "wait": self.wait,
            "recurring": self.recurring
        }))