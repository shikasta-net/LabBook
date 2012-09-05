import os
import shutil

def get_content_reldir(page_id, box_id):
	return os.path.join("static/content", str(page_id), str(box_id))

def get_content_dir(page_id, box_id):
	return os.path.join(request.folder, get_content_reldir(page_id, box_id))
	
def call():
	session.forget()
	return service()

# POST service
@service.run
def upload():
    try:
        db_id = html_id_to_db_id(request.vars['box_id'])
        content_file = request.vars['contentFile']
        file_name = request.vars['contentFileName']
        file_type = request.vars['contentFileType']
        assert request.vars['contentFile'] != None
    except Exception, e:
        raise HTTP(400, 'Malformed upload request: %s' % e)
    
    page_id = db(db.boxes.id == db_id).select().first().page_id    
    page_upload_dir = get_content_dir(page_id, db_id)
    save_dir = os.path.join(request.folder, page_upload_dir)
    print "Saving " + file_name + " to " + save_dir
    if not os.path.isdir(save_dir) :
        os.makedirs(save_dir)
    content_file_path = os.path.join(save_dir, file_name)
    f = open(content_file_path, 'w')
    # TODO: better checking of content type for writing method
    shutil.copyfileobj(content_file.file, f)
    f.close()
    db(db.boxes.id == db_id).update(content_type=file_type, content_id=file_name)
    return request.vars['box_id']
	
@service.run
def delete(box_id):
    try:
        db_id = html_id_to_db_id(box_id)
    except Exception, e:
        raise HTTP(400, 'Malformed delete request: %s' % e)
    if db(db.boxes.id == db_id).select().first().content_type == '':
        raise HTTP(400, 'Called delete content on empty box: %s' % box_id)
    
    page_id = db(db.boxes.id == db_id).select().first().page_id     
    content_dir = os.path.join(request.folder, get_content_dir(page_id, db_id))
    shutil.rmtree(content_dir)
    db(db.boxes.id == db_id).update(content_type='', content_id='')

