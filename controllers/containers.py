def call():
	session.forget()
	return service()

# Functions to create, remove and modify the container boxes.
@service.run
def move_box(id,x,y):
	rcode = 0
	db_mapping = dict(c=db.container_box, i=db.image_box)
	try :
		db_id = id[0]
		box_id = int(id[1:])
		db(db_mapping[db_id].id==box_id).update(position_x=x, position_y=y, modified_on=request.now)
	except Exception, e :
		print 'oops: %s' % e
		response.headers['Status'] = '400'
		rcode = 400
	else :
		rcode = 200
	finally :
		return response.json(dict(return_code=rcode))


@service.run
def resize_box(id,w,h):
	rcode = 0
	db_mapping = dict(c=db.container_box, i=db.image_box)
	try :
		db_id = id[0]
		box_id = int(id[1:])
		db(db_mapping[db_id].id==box_id).update(width=w, height=h, modified_on=request.now)
	except Exception, e :
		print 'oops: %s' % e
		response.headers['Status'] = '400'
		rcode = 400
	else :
		rcode = 200
	finally :
		return response.json(dict(return_code=rcode))


@service.run
def new_box(page_id, x, y, w, h):
	rcode = 0
	try :
		new_id = db.container_box.insert(page_id=page_id, position_x=x, position_y=y, width=w, height=h)
	except Exception, e :
		print 'oops: %s' % e
		response.headers['Status'] = '400'
		rcode = 400
	else :
		rcode = 200
	finally :
		return response.json(dict(return_code=rcode,new_id=new_id))


@service.run
def del_box(box_id):
	rcode = 0
	try :
		container = db(db.container_box.id==box_id).select().first()
		if container.content_id is not None :
			delete_content(container.page_id, box_id, container.content_id)
		db(db.container_box.id==box_id).delete() #better way to do this without requery? pop by setting to variable?
	except Exception, e :
		print 'oops: %s' % e
		response.headers['Status'] = '400'
		rcode = 400
	else :
		rcode = 200
	finally :
		return response.json(dict(return_code=rcode))

