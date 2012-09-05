def call():
	session.forget()
	return service()

# HTML id is 'box' + db id number - ignore the 'box' bit
def html_id_to_db_id(html_id):
    try:
       db_id = int(html_id[3:])
       box = db(db.boxes.id==db_id).select()
       assert box != None
    except Exception, e:
	   raise HTTP(400, 'Malformed box ID: %s' % e)
    return db_id
    
# Raise exception on malformed page_id
def check_page_id(page_id):
    try:
        assert db(db.pages.id == page_id).select() != None
    except Exception, e:
        raise HTTP(400, 'Malformed page ID: %s' % e)
        
# Functions to create, remove and modify the container boxes.
@service.run
def move_box(id,x,y):
    db_id = html_id_to_db_id(id)
    db(db.boxes.id == db_id).update(position_x=x, position_y=y)

@service.run
def resize_box(id,w,h):
	db(db.boxes.id == html_id_to_db_id(id)).update(width=w, height=h)

@service.run
def new_box(page_id, x, y, w, h):
    check_page_id(page_id)
    new_id = db.boxes.insert(page_id=page_id, position_x=x, position_y=y, width=w, height=h)
    return response.json(dict(new_id=new_id))

@service.run
def del_box(box_id):
    db_id = html_id_to_db_id(box_id)
    box = db(db.boxes.id == db_id).select().first()
    if box.content_type != '':
        raise HTTP(400, 'Attempted to delete non-empty content box: %s' % box_id)
    db(db.boxes.id == db_id).delete()
        