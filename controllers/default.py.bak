def index():
    pages = db().select(db.page.id, db.page.title, db.page.modified_on, orderby=db.page.modified_on)
    return dict(pages=pages)
    
def edit():
    this_page = db.page(request.args(0)) or redirect(URL('index'))
    db.text_box.page_id.default = this_page.id
    form = crud.create(db.text_box)
    t_boxes = db(db.text_box.page_id==this_page.id).select()
    return dict(page=this_page, form=form, boxes=t_boxes)
    
def call():
    session.forget()
    return service()
    
@service.run
def move_box(id,x,y):
    rcode = 0
    try :
        db(db.text_box.id==id).update(position_x=x, position_y=y)       
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
        db(db.text_box.id==id).update(width=w, height=h)
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
        new_id = db.text_box.insert(body='some test text for a new record', page_id=page_id)
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
        db(db.text_box.id==box_id).delete()
    except Exception, e :
        print 'oops: %s' % e
        response.headers['Status'] = '400'
        rcode = 400
    else :     
        rcode = 200
    finally :
        return response.json(dict(return_code=rcode))
