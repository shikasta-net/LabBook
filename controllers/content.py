import os
import shutil

def get_content_dir(box_id):
	return get_content_reldir(box_id)

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

	save_dir = get_content_reldir(db_id)
	print "Saving " + file_name + " to " + save_dir
	if not os.path.isdir(save_dir) :
		os.makedirs(save_dir)
	content_file_path = os.path.join(save_dir, file_name)
	f = open(content_file_path, 'w')
	# TODO: better checking of content type for writing method
	shutil.copyfileobj(content_file.file, f)
	f.close()
	update_box(db_id, content_type=file_type, content_id=file_name)
	return request.vars['box_id']

@service.run
def delete(box_id):
	try:
		db_id = html_id_to_db_id(box_id)
	except Exception, e:
		raise HTTP(400, 'Malformed delete request: %s' % e)
	box = get_box(db_id)
	if box.content_type == '':
		raise HTTP(400, 'Called delete content on empty box: %s' % box_id)

	delete_content(db_id)

