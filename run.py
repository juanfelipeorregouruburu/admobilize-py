from api import get_data_audience,get_data_crowd
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

#Despues de desplegar en heroku, poner esta linea 
#en el CLI de heroku para activar el worker
#heroku ps:scale worker=1

#para desactivar esta otra
#heroku ps:scale worker=0

scheduler = BlockingScheduler()
scheduler.add_job(get_data_crowd, IntervalTrigger(seconds=600))
scheduler.add_job(get_data_audience, IntervalTrigger(seconds=600))
scheduler.start()