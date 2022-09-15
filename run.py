from api import get_data_audience,get_data_crowd
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

scheduler = BlockingScheduler()
scheduler.add_job(get_data_crowd, IntervalTrigger(seconds=600))
scheduler.add_job(get_data_audience, IntervalTrigger(seconds=600))
scheduler.start()