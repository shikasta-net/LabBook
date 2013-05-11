from gluon.shell import exec_environment
import xmlrpclib

def index():
    statusList = []
    useLocalMathJax1 = db(db.preferences.preference == 'useLocalMathJax').select().first()
    if useLocalMathJax1 == None:
        errorMsg = LI('Setting "Use local MathJax1?" not set.')
        errorActions = UL(FORM('Set now:', SELECT(OPTION('', _selected='1'), 'True', 'False', _name='value'), INPUT(_value='boolean', _type='hidden', _name='type'), SPAN('', _id='target', _class='status'), _onchange=XML("ajax('%s', ['value', 'type'], 'target');" % URL('preferences/useLocalMathJax'))))
        errorMsg.append(errorActions)
        statusList.append(errorMsg)

    wrk = db_schedule(db_schedule.scheduler_worker.id>0).select().first()
    if (myscheduler.now() - wrk.last_heartbeat > datetime.timedelta(seconds=myscheduler.heartbeat)):
        errorMsg = LI('web2py scheduler not started - printing not available')
        errorActions = UL(FORM('Start now:', INPUT(_value='Start', _type='button', _name='start_scheduler', _onclick=XML("ajax('%s', [], 'target');" % URL('start_scheduler'))), SPAN('', _id='target', _class='status')))
        errorMsg.append(errorActions)
        statusList.append(errorMsg)

    if len(statusList) == 0:
        statusList.append(LI('No installation errors detected!'))
        
	return dict(statusList=statusList)

@request.restful()
def preferences():
    response.view = 'generic.json'
    def GET(preferenceName):
        record = db(db.preferences.preference == preferenceName).select().first()
        return dict(preference=record)
    def POST(preferenceName, **values):
        update = db(db.preferences.preference == preferenceName).validate_and_update(**values)
        if update.updated == 0:
            full_record = dict([('preference', preferenceName)] + values.items())
            update = db.preferences.validate_and_insert(**full_record)
            if update.errors:
                return SPAN("Error: %s" % update.errors.join(', '), _class="error")
            else:
                return SPAN("OK - Created preference", _class="ok")
        elif update.errors:
            return SPAN("Error: %s" % update.errors.join(', '), _class="error")
        else:
            return SPAN("OK - Updated preference", _class="ok")
    return locals()

@request.restful()
def start_scheduler():
    response.view = 'generic.json'
    def POST():
        try:
            from multiprocessing import Process
            from shell import run
            code = "from gluon import current;current._scheduler.loop()"
            print 'Starting scheduler...'
            args = {'appname': 'LabBook', 'plain': False, 'import_models': False, 'startfile': None, 'bpython': False, 'python_code': code}
            args_tuple = ('LabBook', False, False, None, False, code)
            print args
            p = Process(target=run, args=args_tuple)
            p.start()
            print "Scheduler process started"
            return SPAN("OK - Scheduler process started", _class="ok")
        except Exception, e:
            print e
            return SPAN("Error - Scheduler process failed to start", _class="error")

    return locals()

@request.restful()
def test():
    def GET():
        return 'Hello World'
    return locals()


#Function to return the value of the given preference correctly formatted
# def get_preference(pref):
	# row = db(db.preferences.preference == pref).select().first()
	# return {'boolean': {'True': True, 'False': False}[row.value] }[row.type]

#def sections():
#	#return pages in root, and first page of sections of root
#	thumbs = None
#	return dict(thumbs=thumbs)


def call():
	session.forget()
	return service()

#All sections must be born with title and parent, the entry for the root will be created when the labbook is first set up with no parent.
@service.run
def create_section(title, parent):
	try :
		new_page = db.pages.insert(title=title, parent=parent)
	except Exception, e :
		print 'oops: %s' % e
		response.headers['Status'] = '400'
		rcode = 400
	else :
		rcode = 200
	finally :
		return response.json(dict(return_code=rcode))

@service.run
def delete_section(section_id):
	try :
		for s in db(db.section.parent==section_id).select() :
			delete_section(s.id)
		for p in db(db.pages.section==section_id).select() :
			delete_page(p.id)

		db(db.section.id==section_id).delete()
	except Exception, e :
		print 'oops: %s' % e
		response.headers['Status'] = '400'
		rcode = 400
	else :
		rcode = 200
	finally :
		return response.json(dict(return_code=rcode))

# A pair of methods to move a page (or section) into a specific position (page_number) within a section.
# This back shifts all page numbers of the elements of the original section to fill the gap left by the removed element
# and also down shifts all the page numbers in the target section to accomodate the move.
@service.run
def move_to_section(page_id, section_id, page_number):
	try :
		this_page = db(db.pages.id==page_id).select().first()

		for p in db((db.pages.section==this_page.section) & (db.pages.number>this_page.number)).select() :
			p.update_record(number=(p.number-1), modified_on=request.now)
		for s in db((db.section.parent==this_page.section) & (db.section.number>this_page.number)).select() :
			s.update_record(number=(s.number-1), modified_on=request.now)

		for p in db((db.pages.section==section_id) & (db.pages.number>=page_number)).select() :
			p.update_record(number=(p.number+1), modified_on=request.now)
		for s in db((db.section.parent==section_id) & (db.section.number>=page_number)).select() :
			s.update_record(number=(s.number+1), modified_on=request.now)

		this_page.update_record(section=section_id, number=page_number, modified_on=request.now)

	except Exception, e :
		print 'oops: %s' % e
		response.headers['Status'] = '400'
		rcode = 400
	else :
		rcode = 200
	finally :
		return response.json(dict(return_code=rcode))

@service.run
def move_to_section(child_section_id, parent_section_id, page_number):
	try :
		if child_section_id == parent_section_id :
			raise Exception('Cyclically deffined sectioning attempted.')
		else :
			this_section = db(db.section.id==child_section_id).select().first()

			for p in db((db.pages.section==this_section.parent) & (db.pages.number>this_section.number)).select() :
				p.update_record(number=(p.number-1), modified_on=request.now)
			for s in db((db.section.parent==this_section.parent) & (db.section.number>this_section.number)).select() :
				s.update_record(number=(s.number-1), modified_on=request.now)

			for p in db((db.pages.section==section_id) & (db.pages.number>=page_number)).select() :
				p.update_record(number=(p.number+1), modified_on=request.now)
			for s in db((db.section.parent==section_id) & (db.section.number>=page_number)).select() :
				s.update_record(number=(s.number+1), modified_on=request.now)

			this_section.update_record(parent=parent_section_id, number=page_number, modified_on=request.now)

	except Exception, e :
		print 'oops: %s' % e
		response.headers['Status'] = '400'
		rcode = 400
	else :
		rcode = 200
	finally :
		return response.json(dict(return_code=rcode))

#Page can be created as part of a section, or not
@service.run
def create_page(section=None):
	try :
		new_page = insert_new_page(section)
	except Exception, e :
		print 'oops: %s' % e
		response.headers['Status'] = '400'
		rcode = 400
	else :
		rcode = 200
	finally :
		return response.json(dict(return_code=rcode, page_id=new_page))


@service.run
def page_delete(page_id):
	check_page_id(page_id)
	for box in get_boxes_on_page(page_id) :
		db_id = box.id
		delete_content(db_id)
		delete_box(db_id)

	page_dir = get_page_dir(page_id)
	if os.path.isdir(page_dir) :
		shutil.rmtree(page_dir)

	delete_page(page_id)

	return response.json(dict(return_code=200))


# Function to update the page title
@service.run
def update_title(page_id, title_content):
	check_page_id(page_id)
	update_page(page_id, title=title_content)
	#~ try :
		#~ db(db.pages.id==page_id).update(title=title_content, modified_on=request.now)
	#~ except Exception, e :
		#~ print 'oops: %s' % e
		#~ response.headers['Status'] = '400'
		#~ rcode = 400
	#~ else :
		#~ rcode = 200
	#~ finally :
		#~ title_content = db(db.pages.id==page_id).select().first().title
	return response.json(dict(return_code=200, title_content=get_page_title(page_id)))
