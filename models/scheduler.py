from gluon.scheduler import Scheduler
db_schedule = DAL('sqlite://schedule.sqlite')

import shutil
import os.path
def clean_printjob(printjob_id):
	shutil.rmtree(os.path.join(request.folder, 'printjobs', printjob_id))
	return 0

from subprocess import Popen
def run_printjob(prince_args, printjob_id):
	print "Running printjob %s" % printjob_id
	p = Popen(prince_args)
	p.communicate()
		
myscheduler = Scheduler(db_schedule)

import gluon.contrib.simplejson as json
from datetime import datetime
import time
def add_printjob_task(prince_args, printjob_id):
	db_schedule.scheduler_task.validate_and_insert(task_name="run printjob %s" % printjob_id, function_name="run_printjob", vars=json.dumps(dict(printjob_id=printjob_id, prince_args=prince_args)))
	db_schedule.scheduler_task.validate_and_insert(task_name="clean printjob %s" % printjob_id, function_name="clean_printjob", vars="{\"printjob_id\": \"%s\"}" % printjob_id, start_time=datetime.fromtimestamp(time.time() + 5*60), next_run_time=datetime.fromtimestamp(time.time() + 5*60))
	
def get_printjob_status(printjob_id):
	task_record = db_schedule(db_schedule.scheduler_task.task_name == "run printjob %s" % printjob_id).select().first()
	if task_record == None: return 404
	elif task_record.status in ['QUEUED', 'ASSIGNED', 'RUNNING']: return 202
	elif task_record.status == 'COMPLETED': 
		clean_record = db_schedule(db_schedule.scheduler_task.task_name == "clean printjob %s" % printjob_id).select().first()
		if clean_record == None: return 500
		elif clean_record.status == 'COMPLETED': return 410
		else: return 201
	elif task_record.status == 'FAILED': return 500
	else:
		print "Error in task_record status: " + task_record.status
		return 500