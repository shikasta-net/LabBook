import os

def page():

	page_order = []
	pages = {}
	boxes_on_pages	= {}
	extra_box_info = {}

	if request.vars['pages'] :

		page_order = request.vars['pages'].split(',')

		for page_id in page_order :
			check_page_id(page_id)
			pages[page_id] = get_page(page_id)
			boxes_on_pages[page_id] = pages[page_id].boxes.select()
			extra_box_info[page_id] = {}
			for box in boxes_on_pages[page_id]:
				extra_box_info[page_id][box.id] = box_content_info(box)

	elif request.vars['section'] :

		section = request.vars['section']
		if section == 'root' :
			section = None

		section_contents = get_branch(section)

		for object in section_contents :
			page_id = object.page_id
			if not page_id :
				page_id = get_branch(object.id)[0].page_id
			page_id = str(page_id)

			check_page_id(page_id)
			page_order.append(page_id)
			pages[page_id] = get_page(page_id)
			boxes_on_pages[page_id] = pages[page_id].boxes.select()
			extra_box_info[page_id] = {}
			for box in boxes_on_pages[page_id]:
				extra_box_info[page_id][box.id] = box_content_info(box)

	else :
		raise HTTP(400, 'Malformed page(s) request')

	if get_preference('useLocalMathJax') :
		mathjax_URL = URL('static/js', 'MathJax/MathJax.js')+'?config=TeX-AMS-MML_HTMLorMML'
	else :
		mathjax_URL = 'http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'

	return dict(page_order=page_order, pages=pages, boxes_on_pages=boxes_on_pages, extra_box_info=extra_box_info, mathjax_URL=mathjax_URL)

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
    box = get_box(html_id_to_db_id(request.args[0]))
    extra_box_info = {}
    extra_box_info[box.id] = box_content_info(box)
    return dict(box=box, extra_box_info=extra_box_info)

#~ def dynamic_css():
	#~ boxes_on_pages	= {}
	#~ response.headers['Content-Type']='text/css'
	#~ for page_id in request.vars['pages'].split(',') :
		#~ check_page_id(page_id)
		#~ page = get_page(page_id)
		#~ boxes_on_pages[page_id] = page.boxes.select()

	#~ return dict(boxes_on_pages=boxes_on_pages)

#~ def doc_ready():
	#~ response.headers['Content-Type']='text/javascript'
	#~ pages = {}
	#~ for page_id in request.vars['pages'].split(',') :
		#~ pages = get_page(page_id)

	#~ return dict(pages=pages)

