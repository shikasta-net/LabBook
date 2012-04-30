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
def move(id,x,y):
    rcode = 0
    try :
        row = db(db.text_box.id==id).select().first()
        row.update_record(position_x=x, position_y=y)
    except Exception, e :
        print 'oops: %s' % e
        response.headers['Status'] = '400'
        rcode = 400
    else :     
        rcode = 200
    finally :
        return rcode
        
        
@service.run
def resize(id,w,h):
    rcode = 0
    try :
        row = db(db.text_box.id==id).select().first()
        row.update_record(width=w, height=h)
    except Exception, e :
        print 'oops: %s' % e
        response.headers['Status'] = '400'
        rcode = 400
    else :     
        rcode = 200
    finally :
        return rcode
