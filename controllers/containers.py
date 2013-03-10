def call():
	session.forget()
	return service()

# Services to create, remove and modify the container boxes.
@service.run
def move_box(id,x,y):
	db_id = html_id_to_db_id(id)
	update_box(db_id, position_x=x, position_y=y)

@service.run
def resize_box(id,w,h):
	db_id = html_id_to_db_id(id)
	update_box(db_id, width=w, height=h)

@service.run
def new_box(page_id, x, y, w, h):
	new_id = insert_new_box(page_id, x, y, w, h)
	return response.json(dict(new_id=new_id))

@service.run
def del_box(box_id):
	db_id = html_id_to_db_id(box_id)
	delete_box(db_id)

@service.run
def wrap_box(box_id):
    print 'Wrap box request: ' + box_id
    db_id = html_id_to_db_id(box_id)
    child_box = get_box(db_id)
    if child_box['content_type'] == 'box':
        print 'Attempted to wrap a box containing a box (id: %s)' % child_box['id']
        raise HTTP(400, 'Attempted to wrap a box containing a box (id: %s)' % child_box['id'])
    new_parent_box_id = insert_new_box(child_box['page_id'], child_box['position_x'], child_box['position_y'], child_box['width'], child_box['height'])
    new_parent_box = get_box(new_parent_box_id)
    update_box(new_parent_box['id'], content_type='box', content_id=child_box['id'])
    update_box(child_box['id'], position_x=0, position_y=0, width=100, height=100)
    return response.json(dict(new_id=new_parent_box_id))

@service.run
def unwrap_box(box_id):
    print 'Unwrap box request: ' + box_id
    db_id = html_id_to_db_id(box_id)
    parent_box = get_box(db_id)
    if parent_box['content_type'] != 'box':
        print 'Attempted to unwrap a box not containing a box (id: %s)' % parent_box['id']
        raise HTTP(400, 'Attempted to unwrap a box not containing a box (id: %s)' % parent_box['id'])
    child_box = get_box(parent_box['content_id'])
    update_box(child_box['id'], position_x=parent_box['position_x'], position_y=parent_box['position_y'], width=parent_box['width'], height=parent_box['height'])
    update_box(parent_box['id'], content_type='', content_id='')
    delete_box(parent_box['id'])
    return response.json(dict(child_id=child_box['id']))
