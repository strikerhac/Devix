from apscheduler.schedulers.background import BackgroundScheduler
from datetime import  datetime
from apscheduler.triggers.cron import CronTrigger

class Scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def add_job(self, func, trigger, **kwargs):
        self.scheduler.add_job(func, trigger=trigger, **kwargs)