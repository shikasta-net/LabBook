import os

def page():
	page_id = request.args[0]
	check_page_id(page_id)
	page = get_page(page_id)
	boxes_on_pages = page.boxes.select()
	extra_box_info = {}
	child_boxes = []
	for box in boxes_on_pages:
		extra_box_info[box.id] = box_content_info(box)
		if box.content_type == 'box':
			child_boxes.append(box.content_id)

	if get_preference('useLocalMathJax') :
		mathjax_URL = URL('static/js', 'MathJax/MathJax.js')+'?config=TeX-AMS-MML_HTMLorMML'
	else :
		mathjax_URL = 'http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'

	return dict(page=page, boxes_on_pages=boxes_on_pages, child_boxes=child_boxes, extra_box_info=extra_box_info, mathjax_URL=mathjax_URL)

def box():
    box_id = request.args[0]
    box = get_box(box_id)
    return dict(box=box, box_info=box_content_info(box))

from xml.dom import minidom
def box_content_info(box):
	extra_info = {}
	extra_info = {'file_url': get_file_url(box.page_id, box.id, box.content_id)}
	if box.content_type == 'box':
		childbox = db.boxes[box.content_id]
		childbox_info = box_content_info(childbox)
		extra_info = {'child_box': childbox, 'child_box_info': childbox_info}
	elif box.content_type == 'text/html':
		file_content = get_file_contents(box.page_id, box.id, box.content_id)
		extra_info = {'file_contents': file_content}
	elif box.content_type in ['image/png', 'image/jpeg', 'image/svg+xml', 'application/pdf']:
		extra_info = {'file_url': get_file_url(box.page_id, box.id, box.content_id)}
	return extra_info

def box_content():
    box = get_box(html_id_to_db_id(request.args[0]))
    return dict(box=box, box_info=box_content_info(box))
		
#Function to return the value of the given preference correctly formatted
def get_preference(pref):
	row = db(db.preferences.preference == pref).select().first()

def dynamic_css():
	response.headers['Content-Type']='text/css'
	page_id = request.vars['page']
	check_page_id(page_id)
	page = get_page(page_id)
	boxes_on_pages = page.boxes.select()
	return dict(boxes_on_pages=boxes_on_pages)

def doc_ready():
	response.headers['Content-Type']='text/javascript'
	page_id = request.vars['page']
	page = get_page(page_id)
	return dict(page=page)

def get_content_dir(page_id, box_id):
	return os.path.join(request.folder, get_content_reldir(box_id))

def get_file_contents(page_id, box_id, content_id):
	content_dir = os.path.join(os.getcwd(), get_content_dir(page_id, box_id))
	f = open(os.path.join(content_dir, content_id), 'r')
	return XML(f.read())

def get_file_url(page_id, box_id, content_id):
	return URL('static', '%s/%s/%s/%s' % ('content', page_id, box_id, content_id))

from subprocess import Popen
from gluon.contenttype import contenttype
import uuid
@request.restful()
def print_pdf():

	def GET(printid, fetch=None):
		status = get_printjob_status(printid)
		if status == 201 and fetch:
			f = open(os.path.join(request.folder, 'printjobs', printid, 'download.pdf'))
			response.headers['Content-Type'] = contenttype('.pdf')
			response.headers['Content-disposition'] = 'attachment; filename=download.pdf'
			return response.stream(f, chunk_size=64*1024)
		else: raise HTTP(status)
		
	def POST(**kwargs):
		try:
			# Read the current path
			current_path = kwargs['current_path']
			# Read the MathJax specific CSS
			mj_css = kwargs['mj_css']
			# Read the MathJax specific HTML
			maths = kwargs['maths[]']
			# Read the PDF.JS specific HTML
			pdfs = kwargs['pdfs[]']
		except:
			raise HTTP(400, 'Invalid arguments')
		
		# Make the printjob directory
		printid = str(uuid.uuid4())
		printjobdir = os.path.join(request.folder, 'printjobs', printid)
		os.mkdir(printjobdir)
		
		# Write MathJax CSS file
		css_path = os.path.join(printjobdir, 'temp.css')
		f_css = open(css_path, 'w')
		f_css.write(mj_css)
		f_css.close()
	
		# Write JavaScript processing file
		script_path = os.path.join(printjobdir, 'temp.js')
		f = open(script_path, 'w')
				
		f.write('var maths = [];\n\n')
				
		if type(maths) is str:
			f.write('maths.push(\'' + maths + '\');\n\n')
		else:
			for m in maths:
				f.write('maths.push(\'' + m + '\');\n\n')

		f.write('var pdfs = [];\n\n')
	
		if type(pdfs) is str:
			f.write('pdfs.push(\'' + pdfs + '\');\n\n')
		else:
			for pdf in pdfs:
				f.write('pdfs.push(\'' + pdf + '\');\n\n')
		
		f.write('var scripts = $(\'script[type^="math/tex"]\');\n')
		f.write('scripts.each(function(index) {\n')
		f.write('   $(maths[index]).insertBefore($(this));\n')
		f.write('});\n\n')

		f.write('var pdfCanvases = $(\'canvas.pdf_canvas_box\');\n\n')
		f.write('pdfCanvases.each(function(index) {\n')
		f.write('    var pdfCanvas = $(pdfCanvases[index]);\n')
		f.write('    pdfCanvas.siblings(\'script\').remove();\n')
		f.write(('    pdfCanvas.replaceWith($(\'<img '
				 + 'id="pdfCanvas\' + index + \'" '
				 + 'width="\' + pdfCanvas[index].width + \'" '
				 + 'height="\' + pdfCanvas[index].height + \'" '
				 + 'style="\' + $(pdfCanvas[index]).attr(\'style\') + \'" '
				 + 'src="\' + pdfs[index] + \'" '
				 + '/>\'));\n'))
		f.write('});')
		
		f.close()
	
		# Run PrinceXML
		prince_path = os.path.join(request.folder, 'prince/bin/prince')
		prince_args = [prince_path]
		prince_args.append(current_path) # function output to print from
		prince_args.append('-o %s' % os.path.join(printjobdir, 'download.pdf')) # output filename
		prince_args.append('--script=%s' % URL('static', 'js/jquery.js', host=True)) # import jquery
		prince_args.append('--script=http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js') # import jquery
		prince_args.append('--script=%s' % script_path) # Script to insert math elements
		prince_args.append('--style=%s' % css_path) # CSS to style math elements
		prince_args.append('--media=print') # Ensure we're using the print stylesheet
		add_printjob_task(prince_args, printid)
		return response.json(dict(printid=printid))
		
	return locals()
	
