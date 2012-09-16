import os

def page():
	page_id = request.vars['p']
	check_page_id(page_id)
	page = db(db.pages.id == page_id).select().first()
	if request.extension == 'pdf': return render_pdf(page_id)
	boxes_on_pages = page.boxes.select()
	extra_box_info = {}
	for box in boxes_on_pages:
		extra_box_info[box.id] = box_content_info(box)

	if get_preference('useLocalMathJax') :
		mathjax_URL = URL('static/js', 'MathJax/MathJax.js')+'?config=TeX-AMS-MML_SVG'
	else :
		mathjax_URL = 'http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_SVG'
		
	return dict(page=page, boxes_on_pages=boxes_on_pages, extra_box_info=extra_box_info, mathjax_URL=mathjax_URL)

import urllib
import urllib2
def render_pdf(page_id):
	print URL(c='render', f='page', extension='', args=page_id, host=True)
	req = urllib2.Request(URL(c='render', f='page', args=page_id, extension='', host=True))
	print urllib2.urlopen(req).read()

def box_content_info(box):
    extra_info = {}
    if box.content_type == 'box':
        extra_info = {'child_box': box.content_id}
    elif box.content_type == 'text/html':
        extra_info = {'file_contents': get_file_contents(box.page_id, box.id, box.content_id)}
    elif box.content_type in ['image/jpeg', 'image/svg+xml']:
        extra_info = {'file_url': get_file_url(box.page_id, box.id, box.content_id)}
    return extra_info

def box_content():
    box = db(db.boxes.id == html_id_to_db_id(request.args[0])).select().first()
    extra_box_info = {}
    extra_box_info[box.id] = box_content_info(box)
    return dict(box=box, extra_box_info=extra_box_info)
        
#Function to return the value of the given preference correctly formatted
def get_preference(pref):
	row = db(db.preferences.preference == pref).select().first()

	return {'boolean': {'True': True, 'False': False}[row.value] }[row.type]

def dynamic_css():
	response.headers['Content-Type']='text/css'
	page_id = request.vars['page']
	check_page_id(page_id)
	page = db(db.pages.id == page_id).select().first()
	boxes_on_pages = page.boxes.select()
	return dict(boxes_on_pages=boxes_on_pages)

def doc_ready():	
	response.headers['Content-Type']='text/javascript'
	page_id = request.vars['page']
	page = db(db.pages.id == page_id).select().first()
	return dict(page=page)
	
def get_content_reldir(page_id, box_id):
	return os.path.join("static/content", str(page_id), str(box_id))

def get_content_dir(page_id, box_id):
	return os.path.join(request.folder, get_content_reldir(page_id, box_id))

def get_file_contents(page_id, box_id, content_id):
	content_dir = os.path.join(os.getcwd(), get_content_dir(page_id, box_id))
	f = open(os.path.join(content_dir, content_id), 'r')
	return XML(f.read())

def get_file_url(page_id, box_id, content_id):
	return URL('static', '%s/%s/%s/%s' % ('content', page_id, box_id, content_id))
