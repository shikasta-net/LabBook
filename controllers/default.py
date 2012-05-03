def index():
    pages = db().select(db.page.id, db.page.title, db.page.modified_on, orderby=db.page.modified_on)
    return dict(pages=pages)
    
def edit():
    this_page = db.page(request.args(0)) or redirect(URL('index'))
    db.container_box.page_id.default = this_page.id
    boxes = db(db.container_box.page_id==this_page.id).select()
    contents = {}
    for box in boxes :
        if box.content_id is None :
            contents[box.id] = {'file_type':'text', 'file_content':'blank text box'}
        else:
            contents[box.id] = get_contents(box.content_id)
    return dict(page=this_page, boxes=boxes, contents=contents)
    
def call():
    session.forget()
    return service()
    
def get_contents(content_id):
    content = db(db.content.id==content_id).select().first()
    return dict(file_type=content.file_type[0], file_content=content.file_name )
    
@service.run
def move_box(id,x,y):
    rcode = 0
    try :
        db(db.container_box.id==id).update(position_x=x, position_y=y, modified_on=request.now)       
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
    try :
        db(db.container_box.id==id).update(width=w, height=h, modified_on=request.now)
    except Exception, e :
        print 'oops: %s' % e
        response.headers['Status'] = '400'
        rcode = 400
    else :     
        rcode = 200
    finally :
        return response.json(dict(return_code=rcode))
        
        
@service.run
def new_box(page_id):
    rcode = 0
    try :
        new_id = db.container_box.insert(page_id=page_id)
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
        contents = db(db.content.id==db(db.container_box.id==box_id).content_id).select()
        #if exists content, delete it.
        db(db.container_box.id==box_id).delete()
    except Exception, e :
        print 'oops: %s' % e
        response.headers['Status'] = '400'
        rcode = 400
    else :     
        rcode = 200
    finally :
        return response.json(dict(return_code=rcode))
