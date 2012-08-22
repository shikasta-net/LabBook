from gluon.shell import exec_environment
import xmlrpclib

def index():
	pages = db().select(db.page.id, db.page.title, db.page.modified_on, orderby=db.page.modified_on)
	return dict(pages=pages)

def page():

	if get_preference('useLocalMathJax') :
		mathjax_URL = URL('static/js', 'MathJax/MathJax.js')+'?config=TeX-AMS-MML_HTMLorMML'
	else :
		mathjax_URL = 'http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'
	this_page = db.page(request.args(0)) or redirect(URL('index'))
	db.container_box.page_id.default = this_page.id
	boxes = db(db.container_box.page_id==this_page.id).select()
	contents = {}
	server=xmlrpclib.ServerProxy(URL(scheme='http', c='content', f='call/xmlrpc'))
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
