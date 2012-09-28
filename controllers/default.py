from gluon.shell import exec_environment
import xmlrpclib

def index():
	pages = db().select(db.pages.id, db.pages.title, db.pages.modified_on, orderby=db.pages.modified_on)
	return dict(pages=pages)

#This should be removable
#def page():
#
#	if get_preference('useLocalMathJax') :
#		mathjax_URL = URL('static/js', 'MathJax/MathJax.js')
#		print 'using local mathjax'
#	else :
#		mathjax_URL = 'http://cdn.mathjax.org/mathjax/latest/MathJax.js'
#		print 'using remote mathjax'
#	this_page = db.pages(request.args(0)) or redirect(URL('index'))
#	db.container_box.page_id.default = this_page.id
#	boxes = db(db.container_box.page_id==this_page.id).select()
#	contents = {}
#	server=xmlrpclib.ServerProxy(URL(scheme='http', c='content', f='call/xmlrpc'))
#	for box in boxes :
#		contents[box.id] = XML(server.get_content_xml(box.id))
#	return dict(page=this_page, boxes=boxes, contents=contents, mathjax_URL=mathjax_URL)

#Function to return the value of the given preference correctly formatted
# def get_preference(pref):
	# row = db(db.preferences.preference == pref).select().first()
	# return {'boolean': {'True': True, 'False': False}[row.value] }[row.type]

#def sections():
#	#return pages in root, and first page of sections of root
#	thumbs = None
#	return dict(thumbs=thumbs)

def test():
	ordered_objects = get_branch(None)
	for object in ordered_objects :
		if object.page_id is None :
			print str(object.id)+ " section"
		else :
			print str(object.id)+ " " +str(object.page_id)+ " " +get_page(object.page_id).title


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
