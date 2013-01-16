db = DAL('sqlite://storage.sqlite')
from gluon.custom_import import track_changes; track_changes(True)
from gluon.tools import *
from gluon import current
import os, shutil

service = Service()
crud = Crud(db)

db.define_table('pages',
				Field('title', 'string'),
				Field('created_on', 'datetime', default=request.now),
				Field('modified_on', 'datetime', default=request.now))

# Raise exception on malformed page_id - can possibly be included with other page operations?
def check_page_id(page_id):
	try:
		assert db(db.pages.id == page_id).count() != 0
	except Exception, e:
		raise HTTP(400, 'Malformed page ID: %s' % e)

# Add a new entry to the box table
def insert_new_page(section):
	new_id = db.pages.insert(title='')
	return new_id

# Return the page row object
def get_page(page_id):
	return db(db.pages.id == page_id).select().first()

def get_page_dir(page_id):
	return os.path.join(request.folder, "static/content", str(page_id))

# get page title
def get_page_title(page_id):
	return get_page(page_id).title

# Generic method to update aspects of a page
def update_page(page_id, **field_dict):
	field_dict['modified_on'] = request.now
	db(db.pages.id==page_id).update(**field_dict)

def delete_page(page_id) :
	#~ page = db(db.pages.id == page_id).select().first()
	db(db.pages.id == page_id).delete()



# Defines an abstract box model. Fields are self-explanatory and in units of em.
# ondelete='CASCADE' by default, which causes all referring records to be deleted on a delete
db.define_table('boxes',
				Field('page_id', 'reference pages'),
				Field('position_x', 'double', default='1'),
				Field('position_y', 'double', default='1'),
				Field('width', 'double', default='1'),
				Field('height', 'double', default='1'),
				Field('content_type', 'string', default=''),
				Field('content_id', 'string', default=''),
				Field('created_on', 'datetime', default=request.now),
				Field('modified_on', 'datetime', default=request.now))

# HTML id is 'box' + db id number - ignore the 'box' bit
def html_id_to_db_id(html_id):
	try:
	   db_id = int(html_id[3:])
	   box = db(db.boxes.id==db_id).select()
	   assert box != None
	except Exception, e:
	   raise HTTP(400, 'Malformed box ID: %s' % e)
	return db_id

# Return a record for a given box id
def get_box(box_db_id):
	return db(db.boxes.id == box_db_id).select().first()

# Return all box records for a given page_id
def get_boxes_on_page(page_id):
	return db(db.boxes.page_id == page_id).select()

# Update a specific box entry
def update_box(box_db_id, **field_dict):
	field_dict['modified_on'] = request.now
	db(db.boxes.id == box_db_id).update(**field_dict)

# Add a new entry to the box table
def insert_new_box(page_id, x, y, w, h):
	check_page_id(page_id)
	new_id = db.boxes.insert(page_id=page_id, position_x=x, position_y=y, width=w, height=h)
	return new_id

# Delete an entry from the box table
def delete_box(db_id):
	box = db(db.boxes.id == db_id).select().first()
	if box.content_type != '':
		raise HTTP(400, 'Attempted to delete non-empty content box: %s' % db_id)
	db(db.boxes.id == db_id).delete()

# Delete content from a container and return the container to empty
def delete_content(container_id):
	content_dir = get_content_reldir(container_id)
	if os.path.isdir(content_dir) :
		shutil.rmtree(content_dir)
	update_box(container_id, content_type='', content_id='')

# Get the (application relative) path to a content directory for a box
def get_content_reldir(box_id):
	box = get_box(box_id)
	if not (box): raise KeyError('Box id %s does not exist in database' % box_id)
	return os.path.join(request.folder, "static/content", str(box.page_id), str(box_id))

# Get relative path to a particular content file
def get_content_relpath(box_id):
	box = get_box(box_id)
	if not (box):
		raise KeyError('Box id %s does not exist in database' % box_id)
	if (box.content_type == "box") or (box.content_type == None):
		raise KeyError('Box id %s has no associated file content' % box_id)
	return os.path.join(get_content_reldir(box_id), box.content_id)

#~ def get_content_dir(page_id, box_id):
	#~ return os.path.join(request.folder, get_content_reldir(page_id, box_id))

#~ def get_file_contents(page_id, box_id, content_id):
	#~ content_dir = os.path.join(os.getcwd(), get_content_dir(page_id, box_id))
	#~ f = open(os.path.join(content_dir, content_id), 'r')
	#~ return XML(f.read())

def get_file_url(page_id, box_id, content_id):
	return URL('static', '%s/%s/%s/%s' % ('content', page_id, box_id, content_id))

db.define_table('preferences',
				Field('preference', unique=True),
				Field('value', 'string'),
				Field('type', 'string'),
				format='%(preference)s')

#Function to return the value of the given preference correctly formatted
def get_preference(pref):
	row = db(db.preferences.preference == pref).select().first()

	return {'boolean': {'True': True, 'False': False}[row.value] }[row.type]
