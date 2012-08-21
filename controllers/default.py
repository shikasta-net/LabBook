from gluon.shell import exec_environment
import xmlrpclib

def index():
	pages = db().select(db.page.id, db.page.title, db.page.modified_on, orderby=db.page.modified_on)
	return dict(pages=pages)

def page():

	if get_preference('useLocalMathJax') :
		mathjax_URL = URL('static/js', 'MathJax/MathJax.js')
	else :
		mathjax_URL = 'http://cdn.mathjax.org/mathjax/latest/MathJax.js'
	this_page = db.page(request.args(0)) or redirect(URL('index'))
	db.container_box.page_id.default = this_page.id
	boxes = db(db.container_box.page_id==this_page.id).select()
	contents = {}
	server=xmlrpclib.ServerProxy('http://127.0.0.1:8000/LabBook/content/call/xmlrpc')
	for box in boxes :
		contents[box.id] = XML(server.get_content_xml(box.id))
	return dict(page=this_page, boxes=boxes, contents=contents, mathjax_URL=mathjax_URL)

#Function to return the value of the given preference correctly formatted
def get_preference(pref):
	row = db(db.preferences.preference == pref).select().first()

	return {'boolean': {'True': True, 'False': False}[row.value] }[row.type]


def call():
	session.forget()
	return service()

#All sections must be born with title and parent, the entry for the root will be created when the labbook is first set up with no parent.
@service.run
def create_section(title, parent):
	try :
		new_page = db.page.insert(title=title, parent=parent)
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
		for p in db(db.page.section==section_id).select() :
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
		this_page = db(db.page.id==page_id).select().first()

		for p in db((db.page.section==this_page.section) & (db.page.number>this_page.number)).select() :
			p.update_record(number=(p.number-1), modified_on=request.now)
		for s in db((db.section.parent==this_page.section) & (db.section.number>this_page.number)).select() :
			s.update_record(number=(s.number-1), modified_on=request.now)

		for p in db((db.page.section==section_id) & (db.page.number>=page_number)).select() :
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

			for p in db((db.page.section==this_section.parent) & (db.page.number>this_section.number)).select() :
				p.update_record(number=(p.number-1), modified_on=request.now)
			for s in db((db.section.parent==this_section.parent) & (db.section.number>this_section.number)).select() :
				s.update_record(number=(s.number-1), modified_on=request.now)

			for p in db((db.page.section==section_id) & (db.page.number>=page_number)).select() :
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
		new_page = db.page.insert(title='',section=section)
	except Exception, e :
		print 'oops: %s' % e
		response.headers['Status'] = '400'
		rcode = 400
	else :
		rcode = 200
	finally :
		return response.json(dict(return_code=rcode, page_id=new_page))


@service.run
def delete_page(page_id):
	try :
		for box in db(db.container_box.page_id==page_id).select() :
			del_box(box.id)

		page_dir = os.path.join(os.getcwd(), get_page_dir(page_id))
		if os.path.isdir(page_dir) :
			shutil.rmtree(page_dir)

		db(db.page.id==page_id).delete()
	except Exception, e :
		print 'oops: %s' % e
		response.headers['Status'] = '400'
		rcode = 400
	else :
		rcode = 200
	finally :
		return response.json(dict(return_code=rcode))


# Function to update the page title
@service.run
def update_title(page_id, title_content):
	rcode = 0
	try :
		db(db.page.id==page_id).update(title=title_content, modified_on=request.now)
	except Exception, e :
		print 'oops: %s' % e
		response.headers['Status'] = '400'
		rcode = 400
	else :
		rcode = 200
	finally :
		title_content = db(db.page.id==page_id).select().first().title
		return response.json(dict(return_code=rcode, title_content=title_content))

