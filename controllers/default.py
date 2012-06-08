def index():
    pages = db().select(db.page.id, db.page.title, db.page.modified_on, orderby=db.page.modified_on)
    return dict(pages=pages)
    
def page():
    this_page = db.page(request.args(0)) or redirect(URL('index'))
    db.container_box.page_id.default = this_page.id
    boxes = db(db.container_box.page_id==this_page.id).select()
    contents = {}
    for box in boxes :
        contents[box.id] = get_content(box.id)
    return dict(page=this_page, boxes=boxes, contents=contents)
      
def call():
    session.forget()
    return service()   
    
# Function to update the page title
@service.run
def update_title(page_id, title_content):
    rcode = 0
    try :    
        db(db.page.id==page_id).update(title=title_content, modified_on=request.now)       
    except Exception, e :
        print 'oops: %s' % e
        response.headers['Status'] = '400'
        rcode = 400
    else :     
        rcode = 200
    finally :
        title_content = db(db.page.id==page_id).select().first().title
        return response.json(dict(return_code=rcode, title_content=title_content))
    
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

# Content handling code
# Basic program flow:
# 1. JavaScript on page calls upload_content with attached data including a file and all metadata
# 2. upload_content() retrieves a FileHandler from the dictionary handlers with a key equal to the MIME type
#     - If no file handler exists, the server returns an error code
# 3. upload_content() calls the FileHandler.save_file method. This method saves the file to a location in the static folder
# 4. upload_content() inserts a new row describing the content in db.content and adds the content ID to db.container_box
# 5. When the page is refreshed, get_content(box_id) is called, which either returns "No content for this box..." or
#     gets the appropriate file handler and calls FileHandler.get_file(page_id, box_id, file_name)
# 6. the get_file method constructs an appropriate response (in this case, an IMG tag with the right src attribute)
# 7. The page is loaded with images!
#
# TODO: Handler for text/html for integration with rich text editing
# TODO: New service update_content, which handles replacing old content with new (delete old content file?)
# TODO: Might be better to shift some of this into a new controller?
import collections
handlers = collections.defaultdict(None)
class FileHandler:

    def __init__(self, save_handler, get_handler):
        self.save_file = save_handler
        self.get_file = get_handler

import os  
import shutil     
def delete_content(page_id, box_id, content_id) :
    content_dir = os.path.join(os.getcwd(), get_content_dir(page_id, box_id))
    shutil.rmtree(content_dir)
    db(db.content.id==content_id).delete()
 
def default_save_handler(page_id, box_id, file_name, file_content):
    page_upload_dir = get_content_dir(page_id, box_id)
    save_dir = os.path.join(os.getcwd(), page_upload_dir)
    print "Saving " + file_name + " to " + save_dir
    # TODO: overwrite handeled if file has the same name not otherwise
    if not os.path.isdir(save_dir) :
        os.makedirs(save_dir)
    content_file = os.path.join(save_dir, file_name)
    if os.path.isfile(content_file) :
        shutil.copy(content_file, content_file+'.old')
    f = open(content_file, 'w')
    # TODO: better checking of content type for writing method
    shutil.copyfileobj(file_content.file, f)        
    f.close()

def get_content_reldir(page_id, box_id):
    return os.path.join("static/content", str(page_id), str(box_id))
    
def get_content_dir(page_id, box_id):
    return os.path.join(request.folder, get_content_reldir(page_id, box_id))
    
def default_image_get_handler(page_id, box_id, file_name):
#    print "Get handler called for: " + file_name
    img_box = db(db.image_box.page_id==page_id and db.image_box.box_id==box_id).select().first()
    img_box_style = 'position: relative; left: %fem; top: %fem; width: %fem; height: %fem' % (img_box.position_x, img_box.position_y, img_box.width, img_box.height)
    return DIV(DIV(IMG(_src=URL('static', '%s/%s/%s/%s' % ('content', page_id, box_id, file_name)), _alt=file_name, _style='width: 100%; height: 100%'), _id='i'+str(img_box.id), _class="imgbox", _style=img_box_style), _class="clipbox")

def default_text_get_handler(page_id, box_id, file_name):
#    print "Get handler called for: " + file_name
    #return "<p src='" + file_name + "' alt='" + file_name + "' />"
    content_dir = os.path.join(os.getcwd(), get_content_dir(page_id, box_id))
    f = open(os.path.join(content_dir, file_name), 'r')    
    return DIV(XML(f.read()), _id='txt'+str(box_id), _class='textbox', _alt=file_name)

def image_save_handler(page_id, box_id, file_name, file_content):
    default_save_handler(page_id, box_id, file_name, file_content)
    db.image_box.insert(box_id=box_id, page_id=page_id, position_x=0, position_y=0, width=20, height=15)
    
# Add new handlers here   
handlers['image/svg+xml'] = FileHandler(image_save_handler, default_image_get_handler)
handlers['image/jpeg'] = FileHandler(image_save_handler, default_image_get_handler)
handlers['text/html'] = FileHandler(default_save_handler, default_text_get_handler)
  
# Described above         
@service.run
def upload_content():
    try:
        print "upload_content service called on " + request.vars['page_id'] + "/" + request.vars['box_id'] + "/" + request.vars['contentFileName']
        handler = handlers[request.vars['contentFileType']]
        if handler is not None:
            handler.save_file(request.vars['page_id'], request.vars['box_id'], request.vars['contentFileName'], request.vars['contentFile'])
            c_id = db.content.insert(file_type=request.vars['contentFileType'], file_name=request.vars['contentFileName'])
            db(db.container_box.id == request.vars['box_id']).update(content_id = c_id)
            return response.json(dict(content=str(get_content(request.vars['box_id'])), box_id=request.vars['box_id']))
        else:
            print "No file handler for " + request.vars['contentFileType']
            response.headers['Status'] = '500'
            return response.json({'error': 'Error in upload, file type ' + request.vars['contentFileType'] + ' not supported.'})
    except Exception, e:
        print "Oh no! " + str(e)

# Get content service        
@service.run
def get_content(box_id):
    c_box = db(db.container_box.id == box_id).select().first()
    if c_box.content_id is None:
        return ""
    content = db(db.content.id == c_box.content_id).select().first()
    handler = handlers[content.file_type]
    html_resp = handler.get_file(c_box.page_id, box_id, content.file_name)
    return html_resp
