import os

def page():
	page_id = request.args[0]
	check_page_id(page_id)
	page = get_page(page_id)
	boxes_on_pages = page.boxes.select()
	extra_box_info = {}
	for box in boxes_on_pages:
		extra_box_info[box.id] = box_content_info(box)

	if get_preference('useLocalMathJax') :
		mathjax_URL = URL('static/js', 'MathJax/MathJax.js')+'?config=TeX-AMS-MML_HTMLorMML'
	else :
		mathjax_URL = 'http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'

	return dict(page=page, boxes_on_pages=boxes_on_pages, extra_box_info=extra_box_info, mathjax_URL=mathjax_URL)

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

