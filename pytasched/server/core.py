from pytasched.tools import TickManager
from pytasched.engines import get_storage_engine, get_task_engine


class PytaschedServer(object):
    """
    Main server process that monitors for tasks to run and runs them
    """

    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger
        self.storageEngine = None
        self.taskEngine = None

    def _setup(self):
        """
        Setup the server components
        """

        self.logger.debug("Setting up storage engine {engine}".format(
            engine=self.settings.STORAGE["engine"]
        ))

        self.storageEngine = get_storage_engine()

        self.logger.debug("Setting up task engine {engine}".format(
            engine=self.settings.TASKS["engine"]
        ))

        self.taskEngine = get_task_engine()

        self.storageEngine.set_logger(self.logger)
        self.taskEngine.set_logger(self.logger)

    def run(self):
        """
        Run the monitor
        """

        self._setup()

        tm = TickManager(self.settings.SECONDS_PER_TICK)

        while tm.tick():
            tasks = self.storageEngine.get_task_list()

            self.logger.debug("Found {} task(s) to process".format(
                len(tasks)
            ))

            for task in tasks:
                self.logger.info("Running task {} for {}".format(
                    task.id,
                    task.task
                ))

                self.taskEngine.run(task)

                if task.recurring:
                    self.storageEngine.reschedule(task)
                else:
                    self.storageEngine.remove_task(task.id)