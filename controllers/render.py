import os

def page():
	page_id = request.args[0]
	check_page_id(page_id)
	page = db(db.pages.id == page_id).select().first()
	boxes_on_pages = page.boxes.select()
	extra_box_info = {}
	for box in boxes_on_pages:
		extra_box_info[box.id] = box_content_info(box)

	if get_preference('useLocalMathJax') :
		mathjax_URL = URL('static/js', 'MathJax/MathJax.js')+'?config=TeX-AMS-MML_HTMLorMML'
	else :
		mathjax_URL = 'http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'
		
	return dict(page=page, boxes_on_pages=boxes_on_pages, extra_box_info=extra_box_info, mathjax_URL=mathjax_URL)

from xml.dom import minidom
def box_content_info(box):
    extra_info = {}
    if box.content_type == 'box':
        extra_info = {'child_box': box.content_id}
    elif box.content_type == 'text/html':
        file_content = get_file_contents(box.page_id, box.id, box.content_id)
        extra_info = {'file_contents': file_content}
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

from subprocess import Popen
from gluon.contenttype import contenttype
@service.run
def print_pdf():
    # Read the MathJax specific CSS
    mj_css = request.post_vars['mj_css']
    # Read the MathJax specific HTML
    maths = request.post_vars['maths[]']

    # Write MathJax CSS file
    f_css = open('temp.css', 'w')
    f_css.write(mj_css)
    f_css.close()

    # Write JavaScript processing file
    f = open('temp.js', 'w')
    f.write('var maths = [];\n\n')
    for m in maths:
        f.write('maths.push(\'' + m + '\');\n\n');
    f.write('var scripts = $(\'script[type^="math/tex"]\');\n')
    f.write('scripts.each(function(index) {\n')
    f.write('   $(maths[index]).insertBefore($(this));\n')
    f.write('});')
    f.close()

    # Run PrinceXML
    #bin/prince http://127.0.0.1:8000/LabBook/print/page?p=1 test.pdf --script=http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js --script=/Users/agm/web2py/temp.js -v --style=/Users/agm/web2py/temp.css --media=print
    prince_path = os.path.join(request.folder, 'prince/bin/prince')
    p = Popen([prince_path, URL('print', 'page?p=1', host=True), '-o temp_new.pdf', '--script=http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js', '--script=/Users/agm/web2py/temp.js', '-v', '--style=/Users/agm/web2py/temp.css', '--media=print'])
    print "BOOM!"
    p.communicate()
    return response.json(dict(printurl=URL('render', 'printjob')))

def printjob():
    f = open('temp_new.pdf')
    response.headers['Content-Type'] = contenttype('.pdf')
    response.headers['Content-disposition'] = 'attachment; filename=download.pdf'
    return response.stream(f, chunk_size=64*1024)