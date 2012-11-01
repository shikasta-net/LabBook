
def parent():

	current_section = request.vars['section']

	if current_section == 'null' :
		parent = None
	else :
		parent = get_parent(current_section)

	if parent :
		parent = get_parent(current_section).id

	return response.json(dict(parent=parent))
