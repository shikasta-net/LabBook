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
	delete_box(box_id)
